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
            "'not_applicable without rationale marker'",
            "Invalid fixture fixtures/invalid/example.contract.json produced unexpected error: "
            "\"fixtures/invalid/example.contract.json: $.mode value 'broken' not in enum\"",
        ],
    )


def test_expected_error_matching_reports_unexpected_observed_errors() -> None:
    errors = validate_prompt_kit.expected_error_mismatches(
        "fixtures/invalid/example.contract.json",
        [
            "fixtures/invalid/example.contract.json: $.mode value 'broken' not in enum",
            "fixtures/invalid/example.contract.json: $.target value 'browser' not in enum",
        ],
        ["$.mode value 'broken' not in enum"],
    )
    assert_equal(
        errors,
        [
            "Invalid fixture fixtures/invalid/example.contract.json produced unexpected error: "
            "\"fixtures/invalid/example.contract.json: $.target value 'browser' not in enum\""
        ],
    )


def test_governance_policy_flags_runtime_credential_url_without_public_fixture() -> None:
    fixture = validate_prompt_kit.PKG / "tests/fixtures/invalid/runtime-only.contract.json"
    credential_url = (
        "postgres"
        + "ql://"
        + "synthetic_user"
        + ":"
        + "synthetic_pass"
        + "@"
        + "example.invalid/synthetic_db"
    )
    data = {
        "governance": {"scenario_template": "regulated_data_or_domain"},
        "current_state": "Synthetic note includes an unsafe marker: " + credential_url,
    }

    errors = validate_prompt_kit.governance_scenario_fixture_policy_errors(data, fixture)

    assert_equal(
        errors,
        [
            "Governance scenario fixture contains unsafe public marker `PostgreSQL credential URL`: "
            "tests/fixtures/invalid/runtime-only.contract.json"
        ],
    )


def main() -> int:
    test_expected_error_matching_accepts_observed_substrings()
    test_expected_error_matching_reports_missing_substrings()
    test_expected_error_matching_reports_unexpected_observed_errors()
    test_governance_policy_flags_runtime_credential_url_without_public_fixture()
    print("Invalid fixture expectation tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
