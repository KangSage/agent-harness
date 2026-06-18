#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

import validation_cost


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


def assert_equal(actual: object, expected: object) -> None:
    if actual != expected:
        raise AssertionError(f"expected {expected!r}, got {actual!r}")


def assert_contains(errors: list[str], expected: str) -> None:
    if not any(expected in error for error in errors):
        raise AssertionError(f"expected {expected!r} in {errors!r}")


def write_validation_scripts(root: Path, overrides: dict[str, list[str]] | None = None) -> None:
    overrides = overrides or {}
    for relative, allowed_steps in validation_cost.ALLOWED_VALIDATION_STEPS.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        variable_line = 'ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"'
        if relative != "scripts/validate.sh":
            variable_line = 'SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"'
        steps = overrides.get(relative, allowed_steps)
        path.write_text(
            "\n".join(["#!/usr/bin/env bash", "set -euo pipefail", "", variable_line, "", *steps, ""]),
            encoding="utf-8",
        )
    for relative in DEFAULT_VALIDATION_PYTHON_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("from __future__ import annotations\n", encoding="utf-8")


def test_current_validation_entrypoints_stay_lightweight() -> None:
    errors = validation_cost.validation_script_cost_errors(validation_cost.ROOT)
    assert_equal(errors, [])


def test_validation_cost_guard_rejects_network_or_package_manager_commands() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        root_steps = list(validation_cost.ALLOWED_VALIDATION_STEPS["scripts/validate.sh"])
        root_steps.insert(1, "curl https://example.invalid/bootstrap.sh")
        package_steps = list(
            validation_cost.ALLOWED_VALIDATION_STEPS["packages/project-prompt-kit/scripts/validate.sh"]
        )
        package_steps.append("python3 -m pip install example-package")
        write_validation_scripts(
            root,
            {
                "scripts/validate.sh": root_steps,
                "packages/project-prompt-kit/scripts/validate.sh": package_steps,
            },
        )

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Forbidden default validation command `curl`")
    assert_contains(errors, "Forbidden default validation command `python3 -m pip`")


def test_validation_cost_guard_rejects_unregistered_extra_steps() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        root_steps = list(validation_cost.ALLOWED_VALIDATION_STEPS["scripts/validate.sh"])
        root_steps.append('python3 "$ROOT_DIR/scripts/release_check.py"')
        write_validation_scripts(root, {"scripts/validate.sh": root_steps})

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Default validation script has unregistered step in scripts/validate.sh")
    assert_contains(errors, "Default validation script exceeds step budget in scripts/validate.sh")


def test_validation_cost_guard_rejects_missing_registered_steps() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        root_steps = list(validation_cost.ALLOWED_VALIDATION_STEPS["scripts/validate.sh"])
        root_steps.remove('python3 -B "$ROOT_DIR/scripts/test_validation_cost.py"')
        write_validation_scripts(root, {"scripts/validate.sh": root_steps})

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Default validation script is missing registered step in scripts/validate.sh")
    assert_contains(errors, "Default validation script step order/count drift in scripts/validate.sh")


def test_validation_cost_guard_rejects_unknown_executable_lines() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        root_steps = list(validation_cost.ALLOWED_VALIDATION_STEPS["scripts/validate.sh"])
        root_steps.append("sh scripts/slow-validation.sh")
        write_validation_scripts(root, {"scripts/validate.sh": root_steps})

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Default validation script has unregistered step in scripts/validate.sh")


def test_validation_cost_guard_rejects_assignment_command_substitution() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        root_steps = list(validation_cost.ALLOWED_VALIDATION_STEPS["scripts/validate.sh"])
        root_steps.insert(0, 'EXPENSIVE_CHECK="$(python3 "$ROOT_DIR/scripts/slow.py")"')
        write_validation_scripts(root, {"scripts/validate.sh": root_steps})

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Default validation script has unregistered step in scripts/validate.sh")


def test_validation_cost_guard_rejects_forbidden_python_imports() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_validation_scripts(root)
        (root / "scripts" / "validate_repo.py").write_text(
            "from __future__ import annotations\nimport requests\n",
            encoding="utf-8",
        )

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Forbidden default validation Python import `requests`")


def test_validation_cost_guard_rejects_forbidden_python_submodule_imports() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_validation_scripts(root)
        (root / "scripts" / "validate_repo.py").write_text(
            "from __future__ import annotations\nfrom requests.sessions import Session\n",
            encoding="utf-8",
        )

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Forbidden default validation Python import `requests.sessions`")


def test_validation_cost_guard_rejects_dynamic_python_process_calls() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_validation_scripts(root)
        (root / "scripts" / "validate_repo.py").write_text(
            "from __future__ import annotations\nimport os\nos.popen('curl https://example.invalid').read()\n",
            encoding="utf-8",
        )

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Forbidden default validation Python call `os.popen`")


def test_validation_cost_guard_rejects_aliased_python_process_calls() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_validation_scripts(root)
        (root / "scripts" / "validate_repo.py").write_text(
            "from __future__ import annotations\n"
            + "import os as safe_os\n"
            + "from os import system as run_shell\n"
            + "safe_os.popen('curl https://example.invalid').read()\n"
            + "run_shell('curl https://example.invalid')\n",
            encoding="utf-8",
        )

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Forbidden default validation Python call `os.popen`")
    assert_contains(errors, "Forbidden default validation Python call `os.system`")


def test_validation_cost_guard_rejects_process_star_imports() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_validation_scripts(root)
        (root / "scripts" / "validate_repo.py").write_text(
            "from __future__ import annotations\n"
            + "from os import *\n"
            + "popen('curl https://example.invalid').read()\n",
            encoding="utf-8",
        )

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Forbidden default validation Python star import `os.*`")


def test_validation_cost_guard_rejects_dynamic_python_imports() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_validation_scripts(root)
        (root / "scripts" / "validate_repo.py").write_text(
            "from __future__ import annotations\n"
            + "import importlib\n"
            + "importlib.import_module('subprocess')\n"
            + "__import__('subprocess').run(['curl', 'https://example.invalid'])\n",
            encoding="utf-8",
        )

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Forbidden default validation Python dynamic import `subprocess`")


def test_validation_cost_guard_rejects_aliased_dynamic_python_imports() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write_validation_scripts(root)
        (root / "scripts" / "validate_repo.py").write_text(
            "from __future__ import annotations\n"
            + "import importlib as il\n"
            + "from importlib import import_module as load_module\n"
            + "il.import_module('subprocess')\n"
            + "load_module('subprocess')\n",
            encoding="utf-8",
        )

        errors = validation_cost.validation_script_cost_errors(root)

    assert_contains(errors, "Forbidden default validation Python dynamic import `subprocess`")


def main() -> int:
    test_current_validation_entrypoints_stay_lightweight()
    test_validation_cost_guard_rejects_network_or_package_manager_commands()
    test_validation_cost_guard_rejects_unregistered_extra_steps()
    test_validation_cost_guard_rejects_missing_registered_steps()
    test_validation_cost_guard_rejects_unknown_executable_lines()
    test_validation_cost_guard_rejects_assignment_command_substitution()
    test_validation_cost_guard_rejects_forbidden_python_imports()
    test_validation_cost_guard_rejects_forbidden_python_submodule_imports()
    test_validation_cost_guard_rejects_dynamic_python_process_calls()
    test_validation_cost_guard_rejects_aliased_python_process_calls()
    test_validation_cost_guard_rejects_process_star_imports()
    test_validation_cost_guard_rejects_dynamic_python_imports()
    test_validation_cost_guard_rejects_aliased_dynamic_python_imports()
    print("Validation cost tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
