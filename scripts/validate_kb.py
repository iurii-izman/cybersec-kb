#!/usr/bin/env python3
"""Read-only structural validator for CyberSec Knowledge Base v0.1."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

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
)

REQUIRED_FILES = (
    "Home.md",
    "README.md",
    "AGENTS.md",
    ".gitignore",
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

KNOWLEDGE_DIRECTORIES = (
    "10 Concepts",
    "20 Techniques",
    "30 Tools",
    "40 Labs",
    "50 Cheatsheets",
)

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

TOP_LEVEL_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")
LIST_ITEM = re.compile(r"^\s+-\s+(.+?)\s*$")
WIKILINK = re.compile(r"\[\[([^\[\]]+)\]\]")
FENCE = re.compile(r"^\s*```")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, object] | None:
    """Parse the small YAML subset used by the Vault without third-party packages."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    label = relative(path)

    if not lines or lines[0].strip() != "---":
        errors.append(f"{label}: missing opening YAML delimiter")
        return None

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        errors.append(f"{label}: missing closing YAML delimiter")
        return None

    properties: dict[str, object] = {}
    current_key: str | None = None

    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        key_match = TOP_LEVEL_KEY.match(line)
        if key_match and not line.startswith((" ", "\t")):
            key, raw_value = key_match.groups()
            if key in properties:
                errors.append(f"{label}:{line_number}: duplicate property '{key}'")
                continue
            raw_value = (raw_value or "").strip()
            if raw_value == "[]":
                properties[key] = []
            elif raw_value:
                properties[key] = unquote(raw_value)
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
            current_value.append(unquote(item_match.group(1)))
            continue

        errors.append(f"{label}:{line_number}: unsupported or malformed YAML line")

    return properties


def knowledge_files() -> list[Path]:
    paths: list[Path] = []
    for directory in KNOWLEDGE_DIRECTORIES:
        paths.extend((ROOT / directory).rglob("*.md"))
    return sorted(paths)


def maintained_markdown_files() -> list[Path]:
    excluded = {ROOT / "CyberSec_KB_v0.1_start_TZ.md"}
    return sorted(path for path in ROOT.rglob("*.md") if path not in excluded)


def validate_structure(errors: list[str]) -> None:
    for directory in REQUIRED_DIRECTORIES:
        if not (ROOT / directory).is_dir():
            errors.append(f"missing required directory: {directory}")
    for filename in REQUIRED_FILES:
        if not (ROOT / filename).is_file():
            errors.append(f"missing required file: {filename}")


def validate_properties(errors: list[str]) -> None:
    paths = knowledge_files() + sorted((ROOT / "90 Templates").glob("*.md"))
    for path in paths:
        properties = parse_frontmatter(path, errors)
        if properties is None:
            continue

        missing = REQUIRED_PROPERTIES - properties.keys()
        if missing:
            errors.append(
                f"{relative(path)}: missing properties: {', '.join(sorted(missing))}"
            )

        note_type = properties.get("type")
        if note_type not in ALLOWED_TYPES:
            errors.append(f"{relative(path)}: invalid type: {note_type!r}")

        status = properties.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{relative(path)}: invalid status: {status!r}")

        confidence = properties.get("confidence")
        try:
            numeric_confidence = int(str(confidence))
        except (TypeError, ValueError):
            errors.append(f"{relative(path)}: confidence must be an integer from 1 to 5")
        else:
            if numeric_confidence not in range(1, 6):
                errors.append(f"{relative(path)}: confidence must be from 1 to 5")


def validate_fences(errors: list[str]) -> None:
    for path in maintained_markdown_files():
        fence_count = sum(
            1
            for line in path.read_text(encoding="utf-8").splitlines()
            if FENCE.match(line)
        )
        if fence_count % 2:
            errors.append(f"{relative(path)}: unpaired fenced code block")


def validate_duplicates(errors: list[str]) -> None:
    by_name: dict[str, list[Path]] = defaultdict(list)
    for path in knowledge_files():
        by_name[path.stem.casefold()].append(path)
    for paths in by_name.values():
        if len(paths) > 1:
            joined = ", ".join(relative(path) for path in paths)
            errors.append(f"duplicate knowledge-note filename/entity: {joined}")


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    if target.casefold().endswith(".md"):
        target = target[:-3]
    return target.rsplit("/", 1)[-1].strip().casefold()


def validate_wikilinks(errors: list[str]) -> None:
    all_note_names: dict[str, list[Path]] = defaultdict(list)
    for path in ROOT.rglob("*.md"):
        all_note_names[path.stem.casefold()].append(path)

    checked_paths = knowledge_files() + [ROOT / "Home.md"]
    for path in checked_paths:
        text = path.read_text(encoding="utf-8")
        for match in WIKILINK.finditer(text):
            raw_target = match.group(1)
            target = normalize_link_target(raw_target)
            if not target:
                errors.append(f"{relative(path)}: empty wikilink [[{raw_target}]]")
            elif target not in all_note_names:
                errors.append(f"{relative(path)}: broken wikilink [[{raw_target}]]")


def main() -> int:
    errors: list[str] = []
    validate_structure(errors)
    validate_properties(errors)
    validate_fences(errors)
    validate_duplicates(errors)
    validate_wikilinks(errors)

    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: CyberSec Knowledge Base v0.1 validation succeeded")
    print(f"Checked {len(knowledge_files())} knowledge notes and 4 required templates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
