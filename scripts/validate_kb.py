#!/usr/bin/env python3
"""Read-only structural validator for CyberSec Knowledge Base v0.1."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRECTORIES = (
    "00 Inbox",
    "10 Concepts",
    "20 Techniques",
    "30 Tools",
    "40 Labs",
    "40 Labs/TryHackMe",
    "50 Cheatsheets",
    "90 Templates",
    "docs",
    "scripts",
    "tests",
)

REQUIRED_FILES = (
    "Home.md",
    "README.md",
    "AGENTS.md",
    ".gitignore",
    ".gitattributes",
    "docs/Conventions.md",
    "tests/__init__.py",
    "tests/test_validate_kb.py",
    "90 Templates/Concept.md",
    "90 Templates/Technique.md",
    "90 Templates/Tool.md",
    "90 Templates/Lab.md",
    "10 Concepts/HTTP.md",
    "10 Concepts/HTTP Status Codes.md",
    "10 Concepts/Wordlists.md",
    "20 Techniques/Web Enumeration.md",
    "20 Techniques/Content Discovery.md",
    "30 Tools/Nmap.md",
    "30 Tools/DIRB.md",
    "30 Tools/DirBuster.md",
    "40 Labs/TryHackMe/THM - Content Discovery Example.md",
)

KNOWLEDGE_DIRECTORY_TYPES = {
    "10 Concepts": "concept",
    "20 Techniques": "technique",
    "30 Tools": "tool",
    "40 Labs": "lab",
    "50 Cheatsheets": "cheatsheet",
}
TEMPLATE_TYPES = {
    "Concept.md": "concept",
    "Technique.md": "technique",
    "Tool.md": "tool",
    "Lab.md": "lab",
}
KNOWLEDGE_DIRECTORIES = tuple(KNOWLEDGE_DIRECTORY_TYPES)
REQUIRED_PROPERTIES = {
    "type",
    "domain",
    "techniques",
    "status",
    "confidence",
    "source",
}
ALLOWED_TYPES = {"concept", "technique", "tool", "lab", "cheatsheet"}
ALLOWED_STATUSES = {"new", "learned", "practiced", "confident"}
LIST_PROPERTIES = ("domain", "techniques", "source")
IGNORED_PARTS = {".git", ".trash", "__pycache__"}

TOP_LEVEL_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]*(.*))?$")
LIST_ITEM = re.compile(r"^  - (.+?)\s*$")
WIKILINK = re.compile(r"(?<!\\)(?<!\!)\[\[([^\[\]]+)\]\]")
EMBEDDED_WIKILINK = re.compile(r"(?<!\\)!\[\[([^\[\]]+)\]\]")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(?:[^`~]*)$")
INDENTED_FENCE_TEXT = re.compile(r"^ {4,}(`{3,}|~{3,})")
H1 = re.compile(r"^#\s+(.+?)(?:\s+#+)?\s*$")
WIKILINK_VALUE = re.compile(r'^\[\[([^\[\]]+)\]\]$')
TOKEN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


@dataclass(frozen=True)
class Frontmatter:
    values: dict[str, object]
    lines: dict[str, int]


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path, root: Path, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        errors.append(
            f"{relative(path, root)}: invalid UTF-8 at byte {error.start}"
        )
        return None


def strip_inline_comment(value: str) -> str:
    quote: str | None = None
    for index, character in enumerate(value):
        if character in "\"'":
            if quote is None:
                quote = character
            elif quote == character:
                quote = None
        elif character == "#" and quote is None and (
            index == 0 or value[index - 1].isspace()
        ):
            return value[:index].rstrip()
    return value.strip()


def parse_scalar(raw_value: str) -> str | None:
    value = strip_inline_comment(raw_value)
    if not value:
        return None
    if value[0] in "\"'":
        if len(value) < 2 or value[-1] != value[0]:
            return None
        return value[1:-1]
    if value[-1:] in "\"'" or value.startswith(("[", "{", "&", "*", "!", "|", ">")):
        return None
    return value


def parse_frontmatter(
    path: Path, root: Path, errors: list[str]
) -> Frontmatter | None:
    """Parse the strict YAML subset documented for this Vault."""
    text = read_text(path, root, errors)
    if text is None:
        return None
    lines = text.splitlines()
    label = relative(path, root)

    if not lines or lines[0] != "---":
        errors.append(f"{label}: missing opening YAML delimiter")
        return None

    try:
        end = next(i for i in range(1, len(lines)) if lines[i] == "---")
    except StopIteration:
        errors.append(f"{label}: missing closing YAML delimiter")
        return None

    properties: dict[str, object] = {}
    property_lines: dict[str, int] = {}
    current_key: str | None = None

    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line:
            errors.append(f"{label}:{line_number}: tabs are not supported in YAML")
            current_key = None
            continue

        key_match = TOP_LEVEL_KEY.match(line)
        if key_match and not line.startswith(" "):
            key, raw_value = key_match.groups()
            if key in properties:
                errors.append(f"{label}:{line_number}: duplicate property '{key}'")
                current_key = None
                continue

            raw_value = strip_inline_comment((raw_value or "").strip())
            property_lines[key] = line_number
            if raw_value == "[]":
                properties[key] = []
            elif raw_value:
                scalar = parse_scalar(raw_value)
                if scalar is None:
                    errors.append(
                        f"{label}:{line_number}: malformed scalar for property '{key}'"
                    )
                    properties[key] = None
                else:
                    properties[key] = scalar
            else:
                properties[key] = []
            current_key = key
            continue

        item_match = LIST_ITEM.match(line)
        if item_match and current_key:
            current_value = properties[current_key]
            if not isinstance(current_value, list):
                errors.append(
                    f"{label}:{line_number}: list item follows scalar property '{current_key}'"
                )
                continue
            scalar = parse_scalar(item_match.group(1))
            if scalar is None:
                errors.append(f"{label}:{line_number}: malformed YAML list item")
            else:
                current_value.append(scalar)
            continue

        errors.append(f"{label}:{line_number}: unsupported or malformed YAML line")
        current_key = None

    return Frontmatter(properties, property_lines)


def knowledge_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory in KNOWLEDGE_DIRECTORIES:
        base = root / directory
        if base.is_dir():
            paths.extend(
                path
                for path in base.rglob("*.md")
                if not IGNORED_PARTS.intersection(path.parts)
            )
    return sorted(paths)


def maintained_markdown_files(root: Path) -> list[Path]:
    excluded = {root / "CyberSec_KB_v0.1_start_TZ.md"}
    return sorted(
        path
        for path in root.rglob("*.md")
        if path not in excluded and not IGNORED_PARTS.intersection(path.parts)
    )


def expected_type(path: Path, root: Path) -> str | None:
    relative_parts = path.relative_to(root).parts
    if not relative_parts:
        return None
    if relative_parts[0] in KNOWLEDGE_DIRECTORY_TYPES:
        return KNOWLEDGE_DIRECTORY_TYPES[relative_parts[0]]
    if relative_parts[0] == "90 Templates":
        return TEMPLATE_TYPES.get(path.name)
    return None


def validate_structure(root: Path, errors: list[str]) -> None:
    for directory in REQUIRED_DIRECTORIES:
        if not (root / directory).is_dir():
            errors.append(f"missing required directory: {directory}")
    for filename in REQUIRED_FILES:
        if not (root / filename).is_file():
            errors.append(f"missing required file: {filename}")


def validate_properties(root: Path, errors: list[str]) -> None:
    template_directory = root / "90 Templates"
    template_paths = sorted(template_directory.rglob("*.md"))
    paths = knowledge_files(root) + template_paths
    for path in template_paths:
        if path.parent != template_directory or path.name not in TEMPLATE_TYPES:
            errors.append(f"{relative(path, root)}: unsupported template file")
    technique_canonical: dict[str, str] = {}
    for technique_path in knowledge_files(root):
        if expected_type(technique_path, root) != "technique":
            continue
        canonical = relative(technique_path, root)[:-3].casefold()
        technique_canonical[technique_path.stem.casefold()] = canonical
        technique_canonical[canonical] = canonical

    for path in paths:
        frontmatter = parse_frontmatter(path, root, errors)
        if frontmatter is None:
            continue
        properties = frontmatter.values
        label = relative(path, root)

        missing = REQUIRED_PROPERTIES - properties.keys()
        if missing:
            errors.append(f"{label}: missing properties: {', '.join(sorted(missing))}")

        unexpected = properties.keys() - REQUIRED_PROPERTIES
        if unexpected:
            errors.append(
                f"{label}: unsupported properties: {', '.join(sorted(unexpected))}"
            )

        for key in LIST_PROPERTIES:
            if key in properties and not isinstance(properties[key], list):
                line = frontmatter.lines[key]
                errors.append(f"{label}:{line}: property '{key}' must be a list")

        for key in ("domain", "source"):
            value = properties.get(key)
            if isinstance(value, list) and not value:
                line = frontmatter.lines[key]
                errors.append(f"{label}:{line}: property '{key}' must not be empty")
            elif isinstance(value, list):
                line = frontmatter.lines[key]
                for item in value:
                    if not TOKEN.fullmatch(item):
                        errors.append(
                            f"{label}:{line}: {key} entries must use lowercase kebab-case"
                        )
                if len(value) != len({item.casefold() for item in value}):
                    errors.append(f"{label}:{line}: property '{key}' contains duplicates")

        domains = properties.get("domain")
        if isinstance(domains, list) and len(domains) > 1 and "general" in domains:
            errors.append(
                f"{label}:{frontmatter.lines['domain']}: remove fallback 'general' "
                "when a specific domain is present"
            )
        sources = properties.get("source")
        if isinstance(sources, list) and len(sources) > 1 and "other" in sources:
            errors.append(
                f"{label}:{frontmatter.lines['source']}: remove fallback 'other' "
                "when a specific source is present"
            )
        relative_parts = path.relative_to(root).parts
        if (
            isinstance(sources, list)
            and len(relative_parts) >= 3
            and relative_parts[:2] == ("40 Labs", "TryHackMe")
            and path.name != "THM - Content Discovery Example.md"
            and "tryhackme" not in sources
        ):
            errors.append(
                f"{label}:{frontmatter.lines['source']}: real TryHackMe Lab must use "
                "source 'tryhackme'"
            )

        note_type = properties.get("type")
        if "type" in properties and (
            not isinstance(note_type, str) or note_type not in ALLOWED_TYPES
        ):
            errors.append(
                f"{label}:{frontmatter.lines['type']}: invalid type: {note_type!r}"
            )
        path_type = expected_type(path, root)
        if isinstance(note_type, str) and path_type and note_type != path_type:
            errors.append(
                f"{label}:{frontmatter.lines['type']}: type '{note_type}' does not match "
                f"location (expected '{path_type}')"
            )

        status = properties.get("status")
        if "status" in properties and (
            not isinstance(status, str) or status not in ALLOWED_STATUSES
        ):
            errors.append(
                f"{label}:{frontmatter.lines['status']}: invalid status: {status!r}"
            )

        if "confidence" in properties:
            confidence = properties["confidence"]
            line = frontmatter.lines["confidence"]
            if not isinstance(confidence, str) or not re.fullmatch(r"[1-5]", confidence):
                errors.append(f"{label}:{line}: confidence must be an integer from 1 to 5")

        techniques = properties.get("techniques")
        if isinstance(techniques, list):
            if note_type == "tool" and path.parent != template_directory and not techniques:
                errors.append(f"{label}: Tool must link at least one Technique")
            normalized_techniques: list[str] = []
            for item in techniques:
                match = WIKILINK_VALUE.fullmatch(item)
                if match is None:
                    line = frontmatter.lines["techniques"]
                    errors.append(
                        f"{label}:{line}: techniques entries must be quoted wikilinks"
                    )
                    continue
                target = normalize_link_target(match.group(1))
                normalized_techniques.append(technique_canonical.get(target, target))
                if target not in technique_canonical:
                    line = frontmatter.lines["techniques"]
                    errors.append(
                        f"{label}:{line}: techniques link must target a Technique: {item}"
                    )
            if len(normalized_techniques) != len(set(normalized_techniques)):
                line = frontmatter.lines["techniques"]
                errors.append(f"{label}:{line}: property 'techniques' contains duplicates")


def fenced_code_lines(text: str, label: str, errors: list[str]) -> set[int]:
    masked: set[int] = set()
    opening_marker: str | None = None
    opening_line: int | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        match = FENCE.match(line)
        if opening_marker is None:
            if match:
                opening_marker = match.group(1)
                opening_line = line_number
                masked.add(line_number)
        else:
            masked.add(line_number)
            stripped = line.strip()
            indentation = len(line) - len(line.lstrip(" "))
            if (
                stripped
                and indentation <= 3
                and set(stripped) == {opening_marker[0]}
                and len(stripped) >= len(opening_marker)
            ):
                opening_marker = None
                opening_line = None

    if opening_marker is not None and opening_line is not None:
        errors.append(f"{label}:{opening_line}: unclosed fenced code block")
    return masked


def validate_fences(root: Path, errors: list[str]) -> None:
    for path in maintained_markdown_files(root):
        text = read_text(path, root, errors)
        if text is not None:
            fenced_code_lines(text, relative(path, root), errors)


def validate_duplicates(root: Path, errors: list[str]) -> None:
    by_name: dict[str, list[Path]] = defaultdict(list)
    for path in knowledge_files(root):
        by_name[path.stem.casefold()].append(path)
    for paths in by_name.values():
        if len(paths) > 1:
            joined = ", ".join(relative(path, root) for path in paths)
            errors.append(f"duplicate knowledge-note filename/entity: {joined}")


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    if target.casefold().endswith(".md"):
        target = target[:-3]
    return target.casefold()


def markdown_note_index(root: Path) -> tuple[set[str], dict[str, list[str]]]:
    explicit_paths: set[str] = set()
    by_stem: dict[str, list[str]] = defaultdict(list)
    for path in maintained_markdown_files(root):
        if path.relative_to(root).parts[0] == "90 Templates":
            continue
        relative_path = relative(path, root)
        without_suffix = relative_path[:-3] if relative_path.endswith(".md") else relative_path
        normalized = without_suffix.casefold()
        explicit_paths.add(normalized)
        by_stem[path.stem.casefold()].append(normalized)
    return explicit_paths, by_stem


def link_exists(target: str, explicit_paths: set[str], by_stem: dict[str, list[str]]) -> bool:
    if "/" in target:
        return target in explicit_paths
    return len(by_stem.get(target, [])) == 1


def validate_wikilinks(root: Path, errors: list[str]) -> None:
    explicit_paths, by_stem = markdown_note_index(root)
    for path in maintained_markdown_files(root):
        text = read_text(path, root, errors)
        if text is None:
            continue
        label = relative(path, root)
        masked_lines = fenced_code_lines(text, label, [])
        visible_lines = [
            ""
            if line_number in masked_lines or INDENTED_FENCE_TEXT.match(line)
            else line
            for line_number, line in enumerate(text.splitlines(), start=1)
        ]
        visible_text = "\n".join(visible_lines)
        visible_text = HTML_COMMENT.sub(
            lambda match: "\n" * match.group(0).count("\n"), visible_text
        )
        visible_text = INLINE_CODE.sub(
            lambda match: "\n" * match.group(0).count("\n"), visible_text
        )
        for line_number, line in enumerate(visible_text.splitlines(), start=1):
            for match in WIKILINK.finditer(line):
                raw_target = match.group(1)
                base_target = raw_target.split("|", 1)[0].strip()
                if base_target.startswith("#"):
                    continue
                target = normalize_link_target(raw_target)
                if not target:
                    errors.append(f"{label}:{line_number}: empty wikilink [[{raw_target}]]")
                elif not link_exists(target, explicit_paths, by_stem):
                    errors.append(
                        f"{label}:{line_number}: broken wikilink [[{raw_target}]]"
                    )
            for match in EMBEDDED_WIKILINK.finditer(line):
                raw_target = match.group(1)
                base_target = raw_target.split("|", 1)[0].strip()
                if base_target.startswith("#"):
                    continue
                suffix = Path(base_target.split("#", 1)[0]).suffix.casefold()
                if suffix and suffix != ".md":
                    continue
                target = normalize_link_target(raw_target)
                if not target:
                    errors.append(f"{label}:{line_number}: empty embedded wikilink")
                elif not link_exists(target, explicit_paths, by_stem):
                    errors.append(
                        f"{label}:{line_number}: broken embedded note [[{raw_target}]]"
                    )


def validate_headings(root: Path, errors: list[str]) -> None:
    for path in knowledge_files(root):
        text = read_text(path, root, errors)
        if text is None:
            continue
        heading: tuple[int, str] | None = None
        masked_lines = fenced_code_lines(text, relative(path, root), [])
        frontmatter_end = 0
        visible_text = HTML_COMMENT.sub(
            lambda match: "\n" * match.group(0).count("\n"), text
        )
        lines = visible_text.splitlines()
        if lines and lines[0] == "---":
            try:
                frontmatter_end = next(
                    index for index in range(1, len(lines)) if lines[index] == "---"
                ) + 1
            except StopIteration:
                frontmatter_end = len(lines)
        for line_number, line in enumerate(lines, start=1):
            if line_number <= frontmatter_end or line_number in masked_lines:
                continue
            match = H1.match(line)
            if match:
                heading = (line_number, match.group(1))
                break
        label = relative(path, root)
        if heading is None:
            errors.append(f"{label}: missing H1 heading")
        elif heading[1] != path.stem:
            errors.append(
                f"{label}:{heading[0]}: H1 '{heading[1]}' does not match filename '{path.stem}'"
            )
        relative_parts = path.relative_to(root).parts
        if (
            len(relative_parts) >= 3
            and relative_parts[:2] == ("40 Labs", "TryHackMe")
            and not path.stem.startswith("THM - ")
        ):
            errors.append(f"{label}: TryHackMe Lab filename must start with 'THM - '")


def validate_template_headings(root: Path, errors: list[str]) -> None:
    for filename in TEMPLATE_TYPES:
        path = root / "90 Templates" / filename
        if not path.is_file():
            continue
        text = read_text(path, root, errors)
        if text is None:
            continue
        masked_lines = fenced_code_lines(text, relative(path, root), [])
        visible_text = HTML_COMMENT.sub(
            lambda match: "\n" * match.group(0).count("\n"), text
        )
        h1_lines = [
            (line_number, line)
            for line_number, line in enumerate(visible_text.splitlines(), start=1)
            if line_number not in masked_lines and line.startswith("# ")
        ]
        label = relative(path, root)
        if not h1_lines:
            errors.append(f"{label}: missing template H1 '# {{{{title}}}}'")
        elif h1_lines[0][1] != "# {{title}}":
            errors.append(
                f"{label}:{h1_lines[0][0]}: template H1 must be '# {{{{title}}}}'"
            )


def validate(root: Path = DEFAULT_ROOT) -> list[str]:
    """Return deterministic validation errors without modifying the Vault."""
    root = root.resolve()
    errors: list[str] = []
    validate_structure(root, errors)
    validate_properties(root, errors)
    validate_fences(root, errors)
    validate_duplicates(root, errors)
    validate_wikilinks(root, errors)
    validate_headings(root, errors)
    validate_template_headings(root, errors)
    return list(dict.fromkeys(errors))


def main(root: Path = DEFAULT_ROOT) -> int:
    errors = validate(root)
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: CyberSec Knowledge Base v0.1 validation succeeded")
    print(
        f"Checked {len(knowledge_files(root.resolve()))} knowledge notes "
        f"and {len(TEMPLATE_TYPES)} required templates."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
