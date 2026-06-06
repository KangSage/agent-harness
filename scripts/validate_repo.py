#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


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
    ROOT / "scripts",
]

FORBIDDEN_TERMS = [
    "vibe" + "-sunsang",
    "O" + "MX",
    "/U" + "sers/",
    "Kang" + "Sage",
    "github.com/" + "Kang" + "Sage",
    "START " + "COPILOT",
]

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"xox[baprs]-[0-9A-Za-z-]+"),
    re.compile(r"ghp_[0-9A-Za-z_]{36}"),
    re.compile(r"github_pat_[0-9A-Za-z_]+"),
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    re.compile(r"glpat-[A-Za-z0-9_-]{20,}"),
    re.compile(r"npm_[A-Za-z0-9]{20,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"://[^/\s]+:[^/\s]+@"),
]

MODEL_NAME_PATTERNS = [
    re.compile(r"\bgpt-[0-9][A-Za-z0-9_.-]*", re.IGNORECASE),
    re.compile(r"\bclaude-[0-9A-Za-z_.-]+", re.IGNORECASE),
    re.compile(r"\bgemini-[0-9A-Za-z_.-]+", re.IGNORECASE),
    re.compile(r"\b(?:sonnet|opus|haiku)-[0-9][A-Za-z0-9_.-]*", re.IGNORECASE),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def text_files() -> list[Path]:
    suffixes = {".md", ".json", ".yml", ".yaml", ".sh", ".py", ".txt"}
    ignored_dirs = {".git", ".omx", ".idea", ".claude", "__pycache__"}
    files: list[Path] = []
    for scan_path in SCAN_PATHS:
        candidates = [scan_path] if scan_path.is_file() else scan_path.rglob("*")
        for path in candidates:
            if any(part in ignored_dirs for part in path.parts):
                continue
            if path.is_file() and (path.suffix in suffixes or path.name == ".gitignore"):
                files.append(path)
    return files


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

    for file_path in text_files():
        content = read(file_path)
        for term in FORBIDDEN_TERMS:
            if term in content:
                errors.append(f"Forbidden public reference `{term}` in {rel(file_path)}")
        for pattern in MODEL_NAME_PATTERNS:
            if pattern.search(content):
                errors.append(f"Hardcoded model name in {rel(file_path)}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"Secret-like pattern in {rel(file_path)}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Root validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
