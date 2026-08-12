from __future__ import annotations

import importlib.util
from contextlib import redirect_stdout
from io import StringIO
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate_kb.py"
SPEC = importlib.util.spec_from_file_location("validate_kb", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import guard
    raise RuntimeError("Unable to load scripts/validate_kb.py")
validate_kb = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_kb
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


def minimal_note(
    note_type: str,
    title: str,
    *,
    techniques: tuple[str, ...] = (),
    domain: tuple[str, ...] = ("general",),
    source: tuple[str, ...] = ("other",),
) -> str:
    def yaml_list(name: str, values: tuple[str, ...], *, links: bool = False) -> str:
        if not values:
            return f"{name}: []"
        items = [f'  - "[[{value}]]"' if links else f"  - {value}" for value in values]
        return f"{name}:\n" + "\n".join(items)

    return f"""---
type: {note_type}
{yaml_list("domain", domain)}
{yaml_list("techniques", techniques, links=True)}
status: new
confidence: 1
{yaml_list("source", source)}
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

    @property
    def http_path(self) -> Path:
        return self.root / "10 Concepts" / "HTTP.md"

    @property
    def dirb_path(self) -> Path:
        return self.root / "30 Tools" / "DIRB.md"

    def _create_valid_kb(self) -> None:
        for directory in validate_kb.REQUIRED_DIRECTORIES:
            (self.root / directory).mkdir(parents=True, exist_ok=True)

        for filename in validate_kb.REQUIRED_FILES:
            relative_path = Path(filename)
            path = self.root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)

            is_template = relative_path.parts[0] == "90 Templates"
            is_knowledge = relative_path.parts[0] in validate_kb.KNOWLEDGE_DIRECTORIES
            if is_template or is_knowledge:
                note_type = note_type_for(relative_path)
                techniques: tuple[str, ...] = ()
                if note_type == "tool" and not is_template:
                    techniques = ("Content Discovery",)
                title = "{{title}}" if is_template else relative_path.stem
                path.write_text(
                    minimal_note(note_type, title, techniques=techniques),
                    encoding="utf-8",
                )
            elif path.suffix == ".md":
                path.write_text(f"# {path.stem}\n", encoding="utf-8")
            else:
                path.write_text("", encoding="utf-8")

    def _replace(self, path: Path, old: str, new: str) -> None:
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def _append(self, path: Path, text: str) -> None:
        with path.open("a", encoding="utf-8") as stream:
            stream.write(text)

    def errors(self) -> list[str]:
        return validate_kb.validate(self.root)

    def assert_has_error(self, fragment: str) -> None:
        errors = self.errors()
        self.assertTrue(
            any(fragment in error for error in errors),
            msg=f"Expected error containing {fragment!r}, got: {errors}",
        )

    def test_valid_kb_passes(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_invalid_type_fails(self) -> None:
        self._replace(self.http_path, "type: concept", "type: something-random")
        self.assert_has_error("invalid type")

    def test_type_must_match_directory(self) -> None:
        self._replace(self.http_path, "type: concept", "type: tool")
        self.assert_has_error("does not match location")

    def test_invalid_status_fails(self) -> None:
        self._replace(self.http_path, "status: new", "status: archived")
        self.assert_has_error("invalid status")

    def test_invalid_confidence_fails(self) -> None:
        self._replace(self.http_path, "confidence: 1", "confidence: 8")
        self.assert_has_error("confidence must be an integer from 1 to 5")

    def test_non_integer_confidence_fails(self) -> None:
        self._replace(self.http_path, "confidence: 1", "confidence: high")
        self.assert_has_error("confidence must be an integer from 1 to 5")

    def test_unicode_digit_confidence_fails_without_crash(self) -> None:
        self._replace(self.http_path, "confidence: 1", "confidence: ¹")
        self.assert_has_error("confidence must be an integer from 1 to 5")

    def test_empty_domain_and_source_fail(self) -> None:
        self._replace(self.http_path, "domain:\n  - general", "domain: []")
        self._replace(self.http_path, "source:\n  - other", "source: []")
        errors = self.errors()
        self.assertTrue(any("property 'domain' must not be empty" in e for e in errors))
        self.assertTrue(any("property 'source' must not be empty" in e for e in errors))

    def test_domain_and_source_use_lowercase_kebab_case(self) -> None:
        self._replace(self.http_path, "  - general", "  - Active_Directory")
        self.assert_has_error("domain entries must use lowercase kebab-case")

    def test_fallback_values_cannot_mix_with_specific_values(self) -> None:
        self._replace(
            self.http_path,
            "domain:\n  - general",
            "domain:\n  - general\n  - web",
        )
        self._replace(
            self.http_path,
            "source:\n  - other",
            "source:\n  - other\n  - documentation",
        )
        errors = self.errors()
        self.assertTrue(any("remove fallback 'general'" in e for e in errors))
        self.assertTrue(any("remove fallback 'other'" in e for e in errors))

    def test_duplicate_list_values_fail(self) -> None:
        self._replace(
            self.http_path,
            "domain:\n  - general",
            "domain:\n  - web\n  - web",
        )
        self.assert_has_error("property 'domain' contains duplicates")

    def test_tool_requires_technique(self) -> None:
        self._replace(
            self.dirb_path,
            'techniques:\n  - "[[Content Discovery]]"',
            "techniques: []",
        )
        self.assert_has_error("Tool must link at least one Technique")

    def test_technique_entries_must_be_quoted_wikilinks(self) -> None:
        self._replace(
            self.http_path,
            "techniques: []",
            "techniques:\n  - Content Discovery",
        )
        self.assert_has_error("techniques entries must be quoted wikilinks")

    def test_technique_link_must_target_technique_note(self) -> None:
        self._replace(
            self.http_path,
            "techniques: []",
            'techniques:\n  - "[[Wordlists]]"',
        )
        self.assert_has_error("techniques link must target a Technique")

    def test_explicit_technique_path_is_valid(self) -> None:
        self._replace(
            self.dirb_path,
            '  - "[[Content Discovery]]"',
            '  - "[[20 Techniques/Content Discovery]]"',
        )
        self.assertEqual(self.errors(), [])

    def test_aliased_duplicate_techniques_fail(self) -> None:
        self._replace(
            self.dirb_path,
            '  - "[[Content Discovery]]"',
            '  - "[[Content Discovery]]"\n  - "[[Content Discovery|Discovery]]"',
        )
        self.assert_has_error("property 'techniques' contains duplicates")

    def test_bare_and_explicit_duplicate_techniques_fail(self) -> None:
        self._replace(
            self.dirb_path,
            '  - "[[Content Discovery]]"',
            '  - "[[Content Discovery]]"\n'
            '  - "[[20 Techniques/Content Discovery]]"',
        )
        self.assert_has_error("property 'techniques' contains duplicates")

    def test_unsupported_and_duplicate_properties_fail(self) -> None:
        self._replace(self.http_path, "status: new", "extra: value\nstatus: new\nstatus: new")
        errors = self.errors()
        self.assertTrue(any("unsupported properties: extra" in e for e in errors))
        self.assertTrue(any("duplicate property 'status'" in e for e in errors))

    def test_list_property_cannot_be_scalar(self) -> None:
        self._replace(self.http_path, "domain:\n  - general", "domain: general")
        self.assert_has_error("property 'domain' must be a list")

    def test_broken_frontmatter_fails(self) -> None:
        self._replace(self.http_path, "---\n", "")
        self.assert_has_error("missing opening YAML delimiter")

    def test_malformed_yaml_quote_flow_and_tab_fail(self) -> None:
        cases = (
            ("domain:\n  - general", 'domain:\n  - "general'),
            ("domain:\n  - general", "domain:\n  - [general"),
            ("domain:\n  - general", "domain:\n\t- general"),
        )
        for old, new in cases:
            with self.subTest(new=new):
                self._create_valid_kb()
                self._replace(self.http_path, old, new)
                self.assertTrue(self.errors())

    def test_inline_yaml_comments_are_supported(self) -> None:
        self._replace(self.http_path, "status: new", "status: new # learning stage")
        self._replace(self.http_path, "  - general", "  - general # fallback")
        self.assertEqual(self.errors(), [])

    def test_empty_list_with_inline_comment_is_supported(self) -> None:
        self._replace(self.http_path, "techniques: []", "techniques: [] # none yet")
        self.assertEqual(self.errors(), [])

    def test_missing_required_template_and_conventions_fail(self) -> None:
        (self.root / "90 Templates" / "Lab.md").unlink()
        (self.root / "docs" / "Conventions.md").unlink()
        errors = self.errors()
        self.assertTrue(any("missing required file: 90 Templates/Lab.md" in e for e in errors))
        self.assertTrue(any("missing required file: docs/Conventions.md" in e for e in errors))

    def test_missing_required_directory_fails(self) -> None:
        (self.root / "00 Inbox").rmdir()
        self.assert_has_error("missing required directory: 00 Inbox")

    def test_template_requires_title_heading(self) -> None:
        template = self.root / "90 Templates" / "Concept.md"
        self.assertEqual(self.errors(), [])
        self._replace(template, "# {{title}}", "# Wrong")
        self.assert_has_error("template H1 must be '# {{title}}'")

    def test_extra_or_nested_template_fails(self) -> None:
        extra = self.root / "90 Templates" / "Cheatsheet.md"
        extra.write_text(minimal_note("cheatsheet", "Cheatsheet"), encoding="utf-8")
        self.assert_has_error("unsupported template file")
        extra.unlink()
        nested = self.root / "90 Templates" / "Extra" / "Anything.md"
        nested.parent.mkdir()
        nested.write_text("# Anything\n", encoding="utf-8")
        self.assert_has_error("unsupported template file")

    def test_missing_property_does_not_emit_cascading_semantic_error(self) -> None:
        self._replace(self.http_path, "status: new\n", "")
        errors = self.errors()
        self.assertTrue(any("missing properties: status" in e for e in errors))
        self.assertFalse(any("invalid status" in e for e in errors))

    def test_broken_wikilink_fails_with_line_number(self) -> None:
        self._append(self.http_path, "\n- [[Definitely Missing Note]]\n")
        self.assert_has_error(": broken wikilink [[Definitely Missing Note]]")

    def test_explicit_wikilink_path_must_be_correct(self) -> None:
        self._append(self.http_path, "\n- [[10 Concepts/Wordlists]]\n")
        self.assertEqual(self.errors(), [])
        self._replace(
            self.http_path,
            "[[10 Concepts/Wordlists]]",
            "[[nowhere/Wordlists]]",
        )
        self.assert_has_error("broken wikilink [[nowhere/Wordlists]]")

    def test_local_anchor_and_code_examples_are_not_broken_links(self) -> None:
        self._append(
            self.http_path,
            "\n## Details\n\n[[#Details]]\n\n"
            "```text\n[[Missing In Fence]]\n```\n"
            "Inline: ``[[Missing Inline]]``\n",
        )
        self.assertEqual(self.errors(), [])

    def test_multiline_inline_code_link_is_ignored(self) -> None:
        self._append(
            self.http_path,
            "\nBefore `inline code\n[[Missing In Multiline Code]]\nend` after\n",
        )
        self.assertEqual(self.errors(), [])

    def test_escaped_and_html_comment_links_are_ignored(self) -> None:
        self._append(
            self.http_path,
            "\n\\[[Escaped Missing]]\n<!-- [[Comment Missing]] -->\n",
        )
        self.assertEqual(self.errors(), [])

    def test_broken_embedded_note_fails_but_attachment_is_ignored(self) -> None:
        self._append(
            self.http_path,
            "\n![[Missing Note]]\n![[image.png]]\n",
        )
        self.assert_has_error("broken embedded note [[Missing Note]]")

    def test_empty_embed_fails_and_local_heading_embed_is_valid(self) -> None:
        self._append(self.http_path, "\n![[ ]]\n![[#Details]]\n")
        self.assert_has_error("empty embedded wikilink")

    def test_trash_and_templates_cannot_satisfy_live_link(self) -> None:
        trash = self.root / ".trash"
        trash.mkdir()
        (trash / "Ghost.md").write_text("# Ghost\n", encoding="utf-8")
        self._append(self.http_path, "\n- [[Ghost]]\n- [[Lab]]\n")
        errors = self.errors()
        self.assertTrue(any("broken wikilink [[Ghost]]" in e for e in errors))
        self.assertTrue(any("broken wikilink [[Lab]]" in e for e in errors))

    def test_template_ghost_link_is_reported(self) -> None:
        template = self.root / "90 Templates" / "Lab.md"
        self._append(template, "\n- [[Template Ghost]]\n")
        self.assert_has_error("broken wikilink [[Template Ghost]]")

    def test_unclosed_backtick_and_tilde_fences_fail(self) -> None:
        for marker in ("```text", "~~~text"):
            with self.subTest(marker=marker):
                self._create_valid_kb()
                self._append(self.http_path, f"\n{marker}\ncontent\n")
                self.assert_has_error("unclosed fenced code block")

    def test_four_space_pseudo_fence_does_not_mask_live_link(self) -> None:
        self._append(
            self.http_path,
            "\n    ```text\n[[Missing After Indented Code]]\n    ```\n",
        )
        self.assert_has_error("broken wikilink [[Missing After Indented Code]]")

    def test_tool_in_nested_templates_named_folder_is_still_real_tool(self) -> None:
        path = self.root / "30 Tools" / "90 Templates" / "Empty Tool.md"
        path.parent.mkdir()
        path.write_text(minimal_note("tool", "Empty Tool"), encoding="utf-8")
        self.assert_has_error("Tool must link at least one Technique")

    def test_trash_fence_is_ignored(self) -> None:
        trash = self.root / ".trash"
        trash.mkdir()
        (trash / "Deleted.md").write_text("```text\n", encoding="utf-8")
        self.assertEqual(self.errors(), [])

    def test_h1_must_match_filename(self) -> None:
        self._replace(self.http_path, "# HTTP", "# Wrong Title")
        self.assert_has_error("does not match filename 'HTTP'")

    def test_h1_with_closing_hashes_is_valid(self) -> None:
        self._replace(self.http_path, "# HTTP", "# HTTP ##")
        self.assertEqual(self.errors(), [])

    def test_h1_inside_code_block_does_not_satisfy_naming_check(self) -> None:
        self._replace(self.http_path, "# HTTP", "```text\n# HTTP\n```")
        self.assert_has_error("missing H1 heading")

    def test_h1_inside_html_comment_does_not_satisfy_naming_check(self) -> None:
        self._replace(self.http_path, "# HTTP", "<!--\n# HTTP\n-->")
        self.assert_has_error("missing H1 heading")

    def test_template_h1_inside_code_or_comment_does_not_satisfy_contract(self) -> None:
        template = self.root / "90 Templates" / "Concept.md"
        for replacement in (
            "```text\n# {{title}}\n```",
            "<!--\n# {{title}}\n-->",
        ):
            with self.subTest(replacement=replacement):
                self._create_valid_kb()
                self._replace(template, "# {{title}}", replacement)
                self.assert_has_error("missing template H1")

    def test_tryhackme_lab_prefix_is_required(self) -> None:
        path = self.root / "40 Labs" / "TryHackMe" / "Bad Name.md"
        path.write_text(minimal_note("lab", "Bad Name"), encoding="utf-8")
        self.assert_has_error("TryHackMe Lab filename must start with 'THM - '")

    def test_real_tryhackme_lab_requires_tryhackme_source(self) -> None:
        path = self.root / "40 Labs" / "TryHackMe" / "THM - Real Room.md"
        path.write_text(minimal_note("lab", "THM - Real Room"), encoding="utf-8")
        self.assert_has_error("real TryHackMe Lab must use source 'tryhackme'")
        path.write_text(
            minimal_note("lab", "THM - Real Room", source=("tryhackme",)),
            encoding="utf-8",
        )
        self.assertEqual(self.errors(), [])

    def test_duplicate_entity_filename_fails_case_insensitively(self) -> None:
        path = self.root / "30 Tools" / "http.md"
        path.write_text(
            minimal_note("tool", "http", techniques=("Content Discovery",)),
            encoding="utf-8",
        )
        self.assert_has_error("duplicate knowledge-note filename/entity")

    def test_invalid_utf8_is_actionable_and_deduplicated(self) -> None:
        self.http_path.write_bytes(b"\xff\xfe")
        errors = self.errors()
        matching = [error for error in errors if "invalid UTF-8" in error]
        self.assertEqual(len(matching), 1)
        self.assertIn("10 Concepts/HTTP.md", matching[0])

    def test_validation_is_deterministic(self) -> None:
        self._append(self.http_path, "\n- [[Missing]]\n")
        self.assertEqual(self.errors(), self.errors())

    def test_main_returns_zero_for_pass_and_nonzero_for_failure(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(validate_kb.main(self.root), 0)
        self.assertIn("PASS:", output.getvalue())

        self._append(self.http_path, "\n- [[Missing]]\n")
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(validate_kb.main(self.root), 1)
        self.assertIn("FAIL:", output.getvalue())

    def test_validation_does_not_modify_any_file_or_path(self) -> None:
        before = {
            path.relative_to(self.root): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }

        self.assertEqual(self.errors(), [])

        after = {
            path.relative_to(self.root): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
