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


def test_expected_error_matching_accepts_observed_substrings() -> None:
    errors = validate_prompt_kit.expected_error_mismatches(
        "fixtures/invalid/example.contract.json",
        [
            "fixtures/invalid/example.contract.json: $.mode value 'broken' not in enum",
            "Fixture uses not_applicable without rationale marker: fixtures/invalid/example.contract.json",
        ],
        [
            "$.mode value 'broken' not in enum",
            "not_applicable without rationale marker",
        ],
    )
    assert_equal(errors, [])


def test_expected_error_matching_reports_missing_substrings() -> None:
    errors = validate_prompt_kit.expected_error_mismatches(
        "fixtures/invalid/example.contract.json",
        ["fixtures/invalid/example.contract.json: $.mode value 'broken' not in enum"],
        ["not_applicable without rationale marker"],
    )
    assert_equal(
        errors,
        [
            "Invalid fixture fixtures/invalid/example.contract.json did not produce expected error substring: "
            "'not_applicable without rationale marker'"
        ],
    )


def main() -> int:
    test_expected_error_matching_accepts_observed_substrings()
    test_expected_error_matching_reports_missing_substrings()
    print("Invalid fixture expectation tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
