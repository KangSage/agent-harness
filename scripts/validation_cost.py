from __future__ import annotations

import ast
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
FORBIDDEN_PYTHON_STAR_IMPORT_ROOTS = ["os"]
DYNAMIC_IMPORT_FORBIDDEN_ROOTS = sorted(
    set([*FORBIDDEN_PYTHON_IMPORTS, *FORBIDDEN_PYTHON_FROM_IMPORT_ROOTS, "os"])
)


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


def dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def import_bindings(tree: ast.AST) -> tuple[dict[str, str], dict[str, str]]:
    module_aliases: dict[str, str] = {}
    symbol_aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    module_aliases[alias.asname] = alias.name
                else:
                    root_name = alias.name.split(".", 1)[0]
                    module_aliases[root_name] = root_name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if alias.name == "*":
                    continue
                bound_name = alias.asname or alias.name
                symbol_aliases[bound_name] = f"{module}.{alias.name}" if module else alias.name
    return module_aliases, symbol_aliases


def resolve_call_name(call: str, module_aliases: dict[str, str], symbol_aliases: dict[str, str]) -> str:
    if not call:
        return ""
    if call in symbol_aliases:
        return symbol_aliases[call]
    first, separator, remainder = call.partition(".")
    if first in symbol_aliases:
        return f"{symbol_aliases[first]}{separator}{remainder}" if separator else symbol_aliases[first]
    if first in module_aliases:
        return f"{module_aliases[first]}{separator}{remainder}" if separator else module_aliases[first]
    return call


def first_constant_string(node: ast.Call) -> str:
    if not node.args:
        return ""
    first = node.args[0]
    return first.value if isinstance(first, ast.Constant) and isinstance(first.value, str) else ""


def forbidden_python_errors(relative: str, text: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [f"Default validation Python file has invalid syntax in {relative}: {exc}"]

    module_aliases, symbol_aliases = import_bindings(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                if module_matches_forbidden(module, FORBIDDEN_PYTHON_IMPORTS):
                    errors.append(
                        f"Forbidden default validation Python import `{module}` in {relative}:{node.lineno}"
                    )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module_matches_forbidden(module, FORBIDDEN_PYTHON_IMPORTS) or module_matches_forbidden(
                module, FORBIDDEN_PYTHON_FROM_IMPORT_ROOTS
            ):
                errors.append(
                    f"Forbidden default validation Python import `{module}` in {relative}:{node.lineno}"
                )
            if any(alias.name == "*" for alias in node.names) and module_matches_forbidden(
                module, FORBIDDEN_PYTHON_STAR_IMPORT_ROOTS
            ):
                errors.append(
                    f"Forbidden default validation Python star import `{module}.*` in {relative}:{node.lineno}"
                )
        elif isinstance(node, ast.Call):
            call = resolve_call_name(dotted_name(node.func), module_aliases, symbol_aliases)
            if call in {"os.system", "os.popen", "urlopen"} or call.startswith("os.spawn"):
                errors.append(f"Forbidden default validation Python call `{call}` in {relative}:{node.lineno}")
            elif call.startswith("subprocess."):
                errors.append(
                    f"Forbidden default validation Python call `subprocess call` in {relative}:{node.lineno}"
                )
            elif call in {"__import__", "importlib.import_module"}:
                module = first_constant_string(node)
                if module and module_matches_forbidden(module, DYNAMIC_IMPORT_FORBIDDEN_ROOTS):
                    errors.append(
                        f"Forbidden default validation Python dynamic import `{module}` "
                        f"in {relative}:{node.lineno}"
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
