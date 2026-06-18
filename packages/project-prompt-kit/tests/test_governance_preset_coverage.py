#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_prompt_kit.py"
spec = importlib.util.spec_from_file_location("validate_prompt_kit", SCRIPT)
assert spec is not None and spec.loader is not None
validate_prompt_kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_prompt_kit)


def assert_equal(actual: object, expected: object) -> None:
    if actual != expected:
        raise AssertionError(f"expected {expected!r}, got {actual!r}")


def coverage_errors(observed_presets: set[str]) -> list[str]:
    helper = getattr(validate_prompt_kit, "governance_preset_coverage_errors", None)
    if helper is None:
        raise AssertionError("missing governance_preset_coverage_errors helper")
    return helper(observed_presets)


def test_governance_preset_coverage_accepts_all_presets() -> None:
    errors = coverage_errors({"light", "standard", "high_risk"})
    assert_equal(errors, [])


def test_governance_preset_coverage_reports_missing_presets() -> None:
    errors = coverage_errors({"high_risk"})
    assert_equal(
        errors,
        ["Valid governance contract fixtures do not cover every governance preset: missing light, standard"],
    )


def main() -> int:
    test_governance_preset_coverage_accepts_all_presets()
    test_governance_preset_coverage_reports_missing_presets()
    print("Governance preset coverage tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
