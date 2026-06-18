#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True

from validation_hygiene import collect_text_files, read_text, rel_path, scan_public_hygiene


ROOT = Path(__file__).resolve().parents[1]
LANGUAGE_LINK = "[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md)"

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "README.ko.md",
    ROOT / "README.ja.md",
    ROOT / ".gitignore",
    ROOT / "LICENSE",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CHANGELOG.md",
    ROOT / ".github" / "workflows" / "validate.yml",
    ROOT / "docs" / "principles.md",
    ROOT / "docs" / "architecture.md",
    ROOT / "docs" / "roadmap.md",
    ROOT / "scripts" / "validate.sh",
    ROOT / "scripts" / "validate_repo.py",
]

REQUIRED_DIRS = [
    ROOT / "docs",
    ROOT / ".github" / "workflows",
    ROOT / "packages" / "project-prompt-kit",
    ROOT / "scripts",
]

SCAN_PATHS = [
    ROOT / "README.md",
    ROOT / "README.ko.md",
    ROOT / "README.ja.md",
    ROOT / ".gitignore",
    ROOT / "LICENSE",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CHANGELOG.md",
    ROOT / ".github" / "workflows",
    ROOT / "docs",
    ROOT / "packages",
    ROOT / "scripts",
]

def read(path: Path) -> str:
    return read_text(path)


def rel(path: Path) -> str:
    return rel_path(path, ROOT)


def text_files() -> list[Path]:
    return collect_text_files(SCAN_PATHS, extra_names={".gitignore", ".promptkitignore"})


def main() -> int:
    errors: list[str] = []

    for directory in REQUIRED_DIRS:
        if not directory.is_dir():
            errors.append(f"Missing required directory: {rel(directory)}")

    for file_path in REQUIRED_FILES:
        if not file_path.is_file():
            errors.append(f"Missing required file: {rel(file_path)}")

    for readme in [ROOT / "README.md", ROOT / "README.ko.md", ROOT / "README.ja.md"]:
        if readme.is_file() and LANGUAGE_LINK not in read(readme):
            errors.append(f"Missing language links in {rel(readme)}")

    root_readme = ROOT / "README.md"
    if root_readme.is_file() and "personal monorepo" in read(root_readme).lower():
        errors.append("README.md must not describe the public repo as a personal monorepo")

    errors.extend(scan_public_hygiene(text_files(), ROOT))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Root validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
