#!/usr/bin/env python3
from __future__ import annotations

import os
import re
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

GITHUB_OWNER_PATTERN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
GITHUB_REMOTE_PATTERNS = [
    re.compile(r"^git@github\.com:(?P<owner>[^/]+)/[^/]+(?:\.git)?$"),
    re.compile(r"^https://github\.com/(?P<owner>[^/]+)/[^/]+(?:\.git)?/?$"),
    re.compile(r"^ssh://git@github\.com/(?P<owner>[^/]+)/[^/]+(?:\.git)?/?$"),
]


def read(path: Path) -> str:
    return read_text(path)


def rel(path: Path) -> str:
    return rel_path(path, ROOT)


def text_files() -> list[Path]:
    return collect_text_files(SCAN_PATHS, extra_names={".gitignore", ".promptkitignore"})


def valid_github_owner(owner: str) -> bool:
    return bool(GITHUB_OWNER_PATTERN.fullmatch(owner))


def repo_owner_from_remote_url(url: str) -> str | None:
    normalized = url.strip()
    for pattern in GITHUB_REMOTE_PATTERNS:
        match = pattern.match(normalized)
        if match:
            owner = match.group("owner")
            return owner if valid_github_owner(owner) else None
    return None


def repo_owner_from_environment(environ: dict[str, str]) -> str | None:
    for key in ["PUBLIC_HYGIENE_REPO_OWNER", "GITHUB_REPOSITORY_OWNER"]:
        owner = environ.get(key, "").strip()
        if owner and valid_github_owner(owner):
            return owner
    repository = environ.get("GITHUB_REPOSITORY", "").strip()
    if "/" in repository:
        owner = repository.split("/", 1)[0]
        if valid_github_owner(owner):
            return owner
    return None


def repo_owner_from_git_config(root: Path, remote_name: str = "origin") -> str | None:
    config = root / ".git" / "config"
    if not config.is_file():
        return None

    in_remote = False
    remote_header = f'[remote "{remote_name}"]'
    for line in config.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_remote = stripped == remote_header
            continue
        if not in_remote or "=" not in stripped:
            continue
        key, value = (part.strip() for part in stripped.split("=", 1))
        if key == "url":
            return repo_owner_from_remote_url(value)
    return None


def repo_owner_forbidden_terms(owner: str | None) -> tuple[str, ...]:
    if not owner or not valid_github_owner(owner):
        return ()
    return (owner, f"github.com/{owner}", f"github.com:{owner}", f"@{owner}")


def public_hygiene_extra_forbidden_terms(root: Path, environ: dict[str, str] | None = None) -> tuple[str, ...]:
    active_environ = dict(os.environ) if environ is None else environ
    owner = repo_owner_from_environment(active_environ) or repo_owner_from_git_config(root)
    return repo_owner_forbidden_terms(owner)


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

    errors.extend(
        scan_public_hygiene(
            text_files(),
            ROOT,
            extra_forbidden_terms=public_hygiene_extra_forbidden_terms(ROOT),
        )
    )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Root validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
