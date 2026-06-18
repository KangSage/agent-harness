from __future__ import annotations

from collections import Counter
import json
import re
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".sh", ".py", ".txt"}
IGNORED_DIRS = {
    ".git",
    ".omx",
    ".idea",
    ".claude",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "venv",
}

FORBIDDEN_TERMS = [
    "vibe" + "-sunsang",
    "O" + "MX",
    "/U" + "sers/",
    "START " + "COPILOT",
]

SECRET_PATTERN_RULES = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z-]+")),
    ("GitHub token", re.compile(r"ghp_[0-9A-Za-z_]{36}")),
    ("GitHub fine-grained token", re.compile(r"github_pat_[0-9A-Za-z_]+")),
    ("OpenAI API key", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("GitLab token", re.compile(r"glpat-[A-Za-z0-9_-]{20,}")),
    ("npm token", re.compile(r"npm_[A-Za-z0-9]{20,}")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("credential URL", re.compile(r"(?<!\\)\b[A-Za-z][A-Za-z0-9+.-]*://[^:\s/@]+:[^@\s]+@[^\s\"']+")),
]
SECRET_PATTERNS = [pattern for _, pattern in SECRET_PATTERN_RULES]
DecodedJsonSecretAllowlist = set[tuple[str, str, str]]

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


def decoded_json_text(content: str) -> str | None:
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None
    return json.dumps(data, ensure_ascii=False, sort_keys=True)


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


def scan_public_hygiene(
    file_paths: Iterable[Path],
    root: Path,
    decoded_json_secret_allowlist: DecodedJsonSecretAllowlist | None = None,
) -> list[str]:
    errors: list[str] = []
    decoded_allowlist = Counter(decoded_json_secret_allowlist or set())
    for file_path in file_paths:
        content = read_text(file_path)
        relative = rel_path(file_path, root)
        for term in FORBIDDEN_TERMS:
            if term in content:
                errors.append(f"Forbidden public reference `{term}` in {relative}")
        for pattern in MODEL_NAME_PATTERNS:
            if pattern.search(content):
                errors.append(f"Hardcoded model name in {relative}")

        raw_secret_matches: set[tuple[str, str]] = set()
        for label, pattern in SECRET_PATTERN_RULES:
            for match in pattern.finditer(content):
                raw_secret_matches.add((label, match.group(0)))
                errors.append(f"Secret-like pattern `{label}` in {relative}")

        if file_path.suffix == ".json":
            decoded = decoded_json_text(content)
            if decoded is not None:
                for term in FORBIDDEN_TERMS:
                    if term in decoded and term not in content:
                        errors.append(f"Forbidden public reference `{term}` in decoded JSON {relative}")
                for pattern in MODEL_NAME_PATTERNS:
                    if pattern.search(decoded) and not pattern.search(content):
                        errors.append(f"Hardcoded model name in decoded JSON {relative}")
                for label, pattern in SECRET_PATTERN_RULES:
                    for match in pattern.finditer(decoded):
                        key = (relative, label, match.group(0))
                        if (label, match.group(0)) in raw_secret_matches:
                            continue
                        if decoded_allowlist[key] > 0:
                            decoded_allowlist[key] -= 1
                            continue
                        errors.append(f"Secret-like pattern `{label}` in decoded JSON {relative}")
    return errors
