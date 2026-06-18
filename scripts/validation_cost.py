from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_VALIDATION_STEPS = {
    "scripts/validate.sh": [
        'python3 -B "$ROOT_DIR/scripts/validate_repo.py"',
        'python3 -B "$ROOT_DIR/scripts/test_validation_hygiene.py"',
        'python3 -B "$ROOT_DIR/scripts/test_validation_cost.py"',
        'bash "$ROOT_DIR/packages/project-prompt-kit/scripts/validate.sh"',
    ],
    "packages/project-prompt-kit/scripts/validate.sh": [
        'python3 -B "$SCRIPT_DIR/validate_prompt_kit.py"',
        'python3 -B "$SCRIPT_DIR/../tests/test_invalid_fixture_expectations.py"',
        'python3 -B "$SCRIPT_DIR/../tests/test_governance_preset_coverage.py"',
    ],
    "packages/project-prompt-kit/tests/validate-fixtures.sh": [
        'python3 -B "$SCRIPT_DIR/../scripts/validate_prompt_kit.py" --fixtures-only',
        'python3 -B "$SCRIPT_DIR/test_invalid_fixture_expectations.py"',
        'python3 -B "$SCRIPT_DIR/test_governance_preset_coverage.py"',
    ],
}

DEFAULT_VALIDATION_PYTHON_FILES = [
    "scripts/validation_cost.py",
    "scripts/validation_hygiene.py",
    "scripts/validate_repo.py",
    "scripts/test_validation_hygiene.py",
    "scripts/test_validation_cost.py",
    "packages/project-prompt-kit/scripts/validate_prompt_kit.py",
    "packages/project-prompt-kit/tests/test_invalid_fixture_expectations.py",
    "packages/project-prompt-kit/tests/test_governance_preset_coverage.py",
]

SHELL_BOILERPLATE_PATTERNS = [
    re.compile(r"^set\s+-euo\s+pipefail$"),
    re.compile(r'^ROOT_DIR="\$\(cd "\$\(dirname "\$\{BASH_SOURCE\[0\]\}"\)/\.\." && pwd\)"$'),
    re.compile(r'^SCRIPT_DIR="\$\(cd "\$\(dirname "\$\{BASH_SOURCE\[0\]\}"\)" && pwd\)"$'),
]
SHELL_COMMAND_BOUNDARY = r"(^|[;&|`(]|\$\()\s*"
FORBIDDEN_COMMAND_GROUPS = {
    "network downloader": ["curl", "wget"],
    "package manager": [
        "npm",
        "npx",
        "pnpm",
        "yarn",
        "corepack",
        "bun",
        "pip",
        "pip3",
        "pipenv",
        "uv",
        "poetry",
        "hatch",
        "tox",
        "conda",
        "brew",
        "apt",
        "apt-get",
        "apk",
        "bundle",
        "gem",
    ],
    "repository or release client": ["git", "gh"],
    "container or cluster client": ["docker", "kubectl", "helm"],
    "build tool": ["make", "cargo", "go", "mvn", "gradle", "pytest"],
    "release publisher": ["twine"],
}
FORBIDDEN_PYTHON_MODULES = ["pip", "build", "twine", "ensurepip"]
FORBIDDEN_PYTHON_IMPORTS = [
    "anthropic",
    "httpx",
    "openai",
    "requests",
    "socket",
    "subprocess",
    "urllib.request",
]
FORBIDDEN_PYTHON_FROM_IMPORT_ROOTS = [
    "anthropic",
    "httpx",
    "openai",
    "requests",
    "socket",
    "subprocess",
    "urllib",
]
FORBIDDEN_PYTHON_CALL_PATTERNS = {
    "os.system": re.compile(r"\bos\.system\s*\("),
    "subprocess call": re.compile(r"\bsubprocess\.(run|Popen|call|check_call|check_output)\s*\("),
    "urlopen": re.compile(r"\burlopen\s*\("),
}


def module_matches_forbidden(module: str, forbidden_roots: list[str]) -> bool:
    return any(module == root or module.startswith(root + ".") for root in forbidden_roots)


def significant_shell_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append((line_number, stripped))
    return lines


def validation_step_lines(text: str) -> list[str]:
    return [
        stripped
        for _, stripped in significant_shell_lines(text)
        if not any(pattern.match(stripped) for pattern in SHELL_BOILERPLATE_PATTERNS)
    ]


def forbidden_command_errors(relative: str, text: str) -> list[str]:
    errors: list[str] = []
    command_patterns = [
        (
            label,
            re.compile(
                SHELL_COMMAND_BOUNDARY
                + r"(?P<cmd>"
                + "|".join(re.escape(command) for command in commands)
                + r")\b"
            ),
        )
        for label, commands in FORBIDDEN_COMMAND_GROUPS.items()
    ]
    python_module_pattern = re.compile(
        SHELL_COMMAND_BOUNDARY
        + r"(?P<cmd>python3?(?:\s+-B)?\s+-m\s+("
        + "|".join(re.escape(module) for module in FORBIDDEN_PYTHON_MODULES)
        + r"))\b"
    )

    for line_number, stripped in significant_shell_lines(text):
        for label, pattern in command_patterns:
            for match in pattern.finditer(stripped):
                errors.append(
                    f"Forbidden default validation command `{match.group('cmd')}` "
                    f"({label}) in {relative}:{line_number}"
                )
        for match in python_module_pattern.finditer(stripped):
            errors.append(
                f"Forbidden default validation command `{match.group('cmd')}` "
                f"(python package/build module) in {relative}:{line_number}"
            )
    return errors


def python_import_roots(import_targets: str) -> list[str]:
    roots: list[str] = []
    for target in import_targets.split(","):
        module = target.strip().split(" as ", 1)[0].strip()
        if module:
            roots.append(module)
    return roots


def forbidden_python_errors(relative: str, text: str) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        import_match = re.match(r"import\s+(.+)$", stripped)
        if import_match:
            for module in python_import_roots(import_match.group(1)):
                if module_matches_forbidden(module, FORBIDDEN_PYTHON_IMPORTS):
                    errors.append(
                        f"Forbidden default validation Python import `{module}` in {relative}:{line_number}"
                    )

        from_match = re.match(r"from\s+([A-Za-z0-9_.]+)\s+import\s+", stripped)
        if from_match:
            module = from_match.group(1)
            if module_matches_forbidden(module, FORBIDDEN_PYTHON_IMPORTS) or module_matches_forbidden(
                module, FORBIDDEN_PYTHON_FROM_IMPORT_ROOTS
            ):
                errors.append(
                    f"Forbidden default validation Python import `{module}` in {relative}:{line_number}"
                )

        for label, pattern in FORBIDDEN_PYTHON_CALL_PATTERNS.items():
            if pattern.search(stripped):
                errors.append(
                    f"Forbidden default validation Python call `{label}` in {relative}:{line_number}"
                )
    return errors


def validation_script_cost_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative, allowed_steps in ALLOWED_VALIDATION_STEPS.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"Missing default validation script: {relative}")
            continue

        text = path.read_text(encoding="utf-8")
        errors.extend(forbidden_command_errors(relative, text))

        observed_steps = validation_step_lines(text)
        for step in observed_steps:
            if step not in allowed_steps:
                errors.append(f"Default validation script has unregistered step in {relative}: {step}")
        for step in allowed_steps:
            if step not in observed_steps:
                errors.append(f"Default validation script is missing registered step in {relative}: {step}")
        if len(observed_steps) > len(allowed_steps):
            errors.append(
                f"Default validation script exceeds step budget in {relative}: "
                f"expected at most {len(allowed_steps)}, got {len(observed_steps)}"
            )
        if observed_steps != allowed_steps:
            errors.append(
                f"Default validation script step order/count drift in {relative}: "
                f"expected {allowed_steps!r}, got {observed_steps!r}"
            )
    for relative in DEFAULT_VALIDATION_PYTHON_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"Missing default validation Python file: {relative}")
            continue
        errors.extend(forbidden_python_errors(relative, path.read_text(encoding="utf-8")))
    return errors
