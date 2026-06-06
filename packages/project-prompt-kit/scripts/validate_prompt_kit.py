#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PKG = ROOT / "packages" / "project-prompt-kit"

MODES = [
    "choose",
    "task",
    "implement",
    "review",
    "debug",
    "research",
    "docs",
    "release",
    "correction",
    "handoff",
]

CORE_FIELDS = [
    "mode",
    "project",
    "role",
    "objective",
    "current_state",
    "inputs",
    "constraints",
    "success_criteria",
    "risks",
    "output_format",
    "evidence_required",
    "stop_condition",
]

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "README.ko.md",
    ROOT / "README.ja.md",
    ROOT / "LICENSE",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CHANGELOG.md",
    ROOT / ".github" / "workflows" / "validate.yml",
    ROOT / "docs" / "principles.md",
    ROOT / "docs" / "architecture.md",
    ROOT / "docs" / "roadmap.md",
    PKG / "README.md",
    PKG / ".codex-plugin" / "plugin.json",
    PKG / ".promptkitignore",
    PKG / "commands" / "prompt.md",
    PKG / "commands" / "project-prompt.md",
    PKG / "docs" / "architecture.md",
    PKG / "docs" / "authoring-modes.md",
    PKG / "docs" / "portability.md",
    PKG / "schemas" / "prompt-contract.schema.json",
    PKG / "scripts" / "validate.sh",
    PKG / "scripts" / "validate_prompt_kit.py",
    PKG / "skills" / "project-prompt" / "SKILL.md",
    PKG / "skills" / "project-prompt" / "references" / "prompt-contract.md",
]

REQUIRED_DIRS = [
    ROOT / "docs",
    PKG / "commands",
    PKG / "docs",
    PKG / "examples",
    PKG / "examples" / "sample-outputs",
    PKG / "schemas",
    PKG / "scripts",
    PKG / "skills" / "project-prompt" / "references" / "modes",
    PKG / "skills" / "project-prompt" / "references" / "templates",
    PKG / "tests",
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
    re.compile(r"://[^/\s]+:[^/\s]+@"),
]


def text_files() -> list[Path]:
    suffixes = {".md", ".json", ".yml", ".yaml", ".sh", ".py", ".txt"}
    ignored_dirs = {".git", ".omx", ".idea"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.is_file() and (path.suffix in suffixes or path.name in {".promptkitignore"}):
            files.append(path)
    return files


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    errors: list[str] = []

    for directory in REQUIRED_DIRS:
        if not directory.is_dir():
            errors.append(f"Missing required directory: {rel(directory)}")

    for file_path in REQUIRED_FILES:
        if not file_path.is_file():
            errors.append(f"Missing required file: {rel(file_path)}")

    for mode in MODES:
        mode_file = PKG / "skills" / "project-prompt" / "references" / "modes" / f"{mode}.md"
        if not mode_file.is_file():
            errors.append(f"Missing mode file: {rel(mode_file)}")
            continue
        mode_text = read(mode_file)
        for required in ["Purpose:", "Primary output:", "Required prompt fields:", "Guardrail:"]:
            if required not in mode_text:
                errors.append(f"Mode file {rel(mode_file)} missing {required}")

    for template in ["codex", "claude", "generic"]:
        template_file = PKG / "skills" / "project-prompt" / "references" / "templates" / f"{template}.md"
        if not template_file.is_file():
            errors.append(f"Missing renderer template: {rel(template_file)}")
            continue
        template_text = read(template_file)
        for token in [
            "{{objective}}",
            "{{project_context}}",
            "{{constraints}}",
            "{{success_criteria}}",
            "{{evidence_required}}",
            "{{output_format}}",
            "{{stop_condition}}",
        ]:
            if token not in template_text:
                errors.append(f"Template {rel(template_file)} missing {token}")

    language_link = "[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md)"
    for readme in [ROOT / "README.md", ROOT / "README.ko.md", ROOT / "README.ja.md"]:
        if readme.is_file() and language_link not in read(readme):
            errors.append(f"Missing language links in {rel(readme)}")

    prompt_doc = PKG / "commands" / "prompt.md"
    alias_doc = PKG / "commands" / "project-prompt.md"
    if prompt_doc.is_file() and "# /prompt" not in read(prompt_doc):
        errors.append("Expected /prompt command documentation")
    if alias_doc.is_file() and "Canonical alias for `/prompt`" not in read(alias_doc):
        errors.append("Expected /project-prompt alias documentation")

    schema_path = PKG / "schemas" / "prompt-contract.schema.json"
    try:
        schema = json.loads(read(schema_path))
        required = set(schema.get("required", []))
        for field in ["command", "alias", "target", *CORE_FIELDS, "safety"]:
            if field not in required:
                errors.append(f"Schema missing required field: {field}")
        mode_enum = schema.get("properties", {}).get("mode", {}).get("enum", [])
        if mode_enum != MODES:
            errors.append("Schema mode enum does not match documented mode taxonomy")
        safety_required = set(schema.get("properties", {}).get("safety", {}).get("required", []))
        for field in ["telemetry", "local_first", "no_network", "redaction", "prompt_injection_boundary"]:
            if field not in safety_required:
                errors.append(f"Schema safety missing required field: {field}")
    except Exception as exc:
        errors.append(f"Invalid schema JSON: {exc}")

    for example in sorted((PKG / "examples").glob("sample-contract.*.json")):
        try:
            data = json.loads(read(example))
        except Exception as exc:
            errors.append(f"Invalid example JSON {rel(example)}: {exc}")
            continue
        for field in ["command", "alias", "target", *CORE_FIELDS, "safety"]:
            if field not in data:
                errors.append(f"Example {rel(example)} missing field: {field}")
        safety = data.get("safety", {})
        if safety.get("telemetry") != "off":
            errors.append(f"Example {rel(example)} must set telemetry off")
        if safety.get("local_first") is not True or safety.get("no_network") is not True:
            errors.append(f"Example {rel(example)} must be local-first and no-network")
        if safety.get("redaction") is not True:
            errors.append(f"Example {rel(example)} must enable redaction")

    for sample in ["choose", "implement", "review", "debug", "docs", "handoff"]:
        sample_file = PKG / "examples" / "sample-outputs" / f"{sample}.md"
        if not sample_file.is_file():
            errors.append(f"Missing golden sample output: {rel(sample_file)}")
            continue
        sample_text = read(sample_file)
        for phrase in ["Source of truth:", "Scope:", "Validation:", "Gap handling:"]:
            if phrase not in sample_text:
                errors.append(f"Sample output {rel(sample_file)} missing {phrase}")

    ignore_text = read(PKG / ".promptkitignore") if (PKG / ".promptkitignore").is_file() else ""
    for pattern in [".git/", ".env", ".env.*", "*.pem", "*.key", "node_modules/", "vendor/", "dist/", "build/", "target/", "coverage/"]:
        if pattern not in ignore_text:
            errors.append(f".promptkitignore missing default deny pattern: {pattern}")

    skill_text = read(PKG / "skills" / "project-prompt" / "SKILL.md")
    if "Handoff is one mode among several" not in skill_text:
        errors.append("Skill must state that handoff is not the default mode")

    for file_path in text_files():
        content = read(file_path)
        for term in FORBIDDEN_TERMS:
            if term in content:
                errors.append(f"Forbidden public reference `{term}` in {rel(file_path)}")
        if re.search(r"\bgpt-[0-9]", content, re.IGNORECASE):
            errors.append(f"Hardcoded model name in {rel(file_path)}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"Secret-like pattern in {rel(file_path)}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
