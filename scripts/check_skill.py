#!/usr/bin/env python3
"""Validate the gonesis skill package.

Checks:
  1. SKILL.md starts with YAML frontmatter containing a valid name and description.
  2. Every local Markdown link in every .md file resolves to an existing path
     that stays inside the repository root.

Usage: python3 -I scripts/check_skill.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1\s*$", re.DOTALL | re.MULTILINE)
MAX_DESCRIPTION = 1024
SKIP_DIRS = {".git", "node_modules"}


def check_frontmatter(errors: list[str]) -> None:
    skill = ROOT / "SKILL.md"
    if not skill.is_file():
        errors.append("SKILL.md is missing")
        return
    lines = skill.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md: frontmatter must start on the first line with ---")
        return
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        errors.append("SKILL.md: frontmatter is not closed with ---")
        return
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name:
        errors.append("SKILL.md: frontmatter 'name' is missing")
    elif not NAME_RE.match(name):
        errors.append(f"SKILL.md: name '{name}' must use lowercase letters, numbers, and hyphens")
    if not description:
        errors.append("SKILL.md: frontmatter 'description' is missing")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"SKILL.md: description is {len(description)} characters (max {MAX_DESCRIPTION})")


def markdown_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*.md") if not SKIP_DIRS.intersection(p.relative_to(ROOT).parts)
    )


def check_links(errors: list[str]) -> int:
    checked = 0
    for md in markdown_files():
        text = FENCE_RE.sub("", md.read_text(encoding="utf-8"))
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (md.parent / path_part).resolve()
            rel = md.relative_to(ROOT)
            if ROOT not in resolved.parents and resolved != ROOT:
                errors.append(f"{rel}: link '{target}' escapes the repository root")
            elif not resolved.exists():
                errors.append(f"{rel}: broken link '{target}'")
            checked += 1
    return checked


def main() -> int:
    errors: list[str] = []
    check_frontmatter(errors)
    checked = check_links(errors)
    if errors:
        print("FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"OK: SKILL.md frontmatter valid; {checked} local links resolved in {len(markdown_files())} Markdown files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
