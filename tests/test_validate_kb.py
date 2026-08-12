from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate_kb.py"
SPEC = importlib.util.spec_from_file_location("validate_kb", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import guard
    raise RuntimeError("Unable to load scripts/validate_kb.py")
validate_kb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_kb)


def note_type_for(path: Path) -> str:
    parts = path.parts
    if parts[0] == "90 Templates":
        return path.stem.casefold()
    if parts[0] == "10 Concepts":
        return "concept"
    if parts[0] == "20 Techniques":
        return "technique"
    if parts[0] == "30 Tools":
        return "tool"
    if parts[0] == "40 Labs":
        return "lab"
    if parts[0] == "50 Cheatsheets":
        return "cheatsheet"
    raise ValueError(f"Not a knowledge note: {path}")


def minimal_note(note_type: str, title: str) -> str:
    return f"""---
type: {note_type}
domain:
  - general
techniques: []
status: new
confidence: 1
source:
  - other
---

# {title}
"""


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self._create_valid_kb()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _create_valid_kb(self) -> None:
        for directory in validate_kb.REQUIRED_DIRECTORIES:
            (self.root / directory).mkdir(parents=True, exist_ok=True)

        for filename in validate_kb.REQUIRED_FILES:
            relative_path = Path(filename)
            path = self.root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)

            if relative_path.parts[0] in validate_kb.KNOWLEDGE_DIRECTORIES or (
                relative_path.parts[0] == "90 Templates"
            ):
                path.write_text(
                    minimal_note(note_type_for(relative_path), relative_path.stem),
                    encoding="utf-8",
                )
            elif path.suffix == ".md":
                path.write_text(f"# {path.stem}\n", encoding="utf-8")
            else:
                path.write_text("", encoding="utf-8")

    def _replace_in_http(self, old: str, new: str) -> None:
        path = self.root / "10 Concepts" / "HTTP.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assert_has_error(self, fragment: str) -> None:
        errors = validate_kb.validate(self.root)
        self.assertTrue(
            any(fragment in error for error in errors),
            msg=f"Expected error containing {fragment!r}, got: {errors}",
        )

    def test_valid_kb_passes(self) -> None:
        self.assertEqual(validate_kb.validate(self.root), [])

    def test_invalid_type_fails(self) -> None:
        self._replace_in_http("type: concept", "type: something-random")
        self.assert_has_error("invalid type")

    def test_invalid_status_fails(self) -> None:
        self._replace_in_http("status: new", "status: archived")
        self.assert_has_error("invalid status")

    def test_invalid_confidence_fails(self) -> None:
        self._replace_in_http("confidence: 1", "confidence: 8")
        self.assert_has_error("confidence must be from 1 to 5")

    def test_broken_wikilink_fails(self) -> None:
        path = self.root / "10 Concepts" / "HTTP.md"
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n- [[Definitely Missing Note]]\n")
        self.assert_has_error("broken wikilink [[Definitely Missing Note]]")

    def test_missing_required_template_fails(self) -> None:
        (self.root / "90 Templates" / "Lab.md").unlink()
        self.assert_has_error("missing required file: 90 Templates/Lab.md")

    def test_broken_frontmatter_fails(self) -> None:
        self._replace_in_http("---\n", "")
        self.assert_has_error("missing opening YAML delimiter")

    def test_validation_does_not_modify_markdown(self) -> None:
        before = {
            path.relative_to(self.root): path.read_bytes()
            for path in self.root.rglob("*.md")
        }

        self.assertEqual(validate_kb.validate(self.root), [])

        after = {
            path.relative_to(self.root): path.read_bytes()
            for path in self.root.rglob("*.md")
        }
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
