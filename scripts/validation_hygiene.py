from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".sh", ".py", ".txt"}
IGNORED_DIRS = {".git", ".omx", ".idea", ".claude", "__pycache__"}

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

# Best-effort host-neutrality guardrail, not a complete model registry.
# Require a numeric family suffix to avoid product/tool slugs such as claude-code.
MODEL_NAME_PATTERNS = [
    re.compile(r"\bgpt-[0-9][A-Za-z0-9_.-]*", re.IGNORECASE),
    re.compile(r"\bclaude-[0-9][A-Za-z0-9_.-]*", re.IGNORECASE),
    re.compile(r"\bgemini-[0-9][A-Za-z0-9_.-]*", re.IGNORECASE),
    re.compile(r"\b(?:sonnet|opus|haiku)-[0-9][A-Za-z0-9_.-]*", re.IGNORECASE),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel_path(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def collect_text_files(scan_paths: Iterable[Path], extra_names: set[str] | None = None) -> list[Path]:
    names = extra_names or set()
    files: list[Path] = []
    for scan_path in scan_paths:
        if not scan_path.exists():
            continue
        candidates = [scan_path] if scan_path.is_file() else scan_path.rglob("*")
        for path in candidates:
            if any(part in IGNORED_DIRS for part in path.parts):
                continue
            if path.is_file() and (path.suffix in TEXT_SUFFIXES or path.name in names):
                files.append(path)
    return files


def scan_public_hygiene(file_paths: Iterable[Path], root: Path) -> list[str]:
    errors: list[str] = []
    for file_path in file_paths:
        content = read_text(file_path)
        for term in FORBIDDEN_TERMS:
            if term in content:
                errors.append(f"Forbidden public reference `{term}` in {rel_path(file_path, root)}")
        for pattern in MODEL_NAME_PATTERNS:
            if pattern.search(content):
                errors.append(f"Hardcoded model name in {rel_path(file_path, root)}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"Secret-like pattern in {rel_path(file_path, root)}")
    return errors
