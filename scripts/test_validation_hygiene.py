#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

from validation_hygiene import scan_public_hygiene


ALLOWED_RELATIVE_PATH = (
    "packages/project-prompt-kit/tests/fixtures/invalid/"
    "invalid-governance-scenario-db-credential-url.contract.json"
)
ALLOWED_DECODED_SECRET = (
    ALLOWED_RELATIVE_PATH,
    "credential URL",
    "postgresql://synthetic_user:synthetic_pass" + "@example.invalid/synthetic_db",
)


def write_json(root: Path, relative_path: str, json_text: str) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_text, encoding="utf-8")
    return path


def assert_equal(actual: object, expected: object) -> None:
    if actual != expected:
        raise AssertionError(f"expected {expected!r}, got {actual!r}")


def test_decoded_json_scan_flags_escaped_credential_url() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            "example.json",
            '{"value":"postgresql://synthetic_user:synthetic_pass\\u0040example.invalid/synthetic_db"}',
        )

        errors = scan_public_hygiene([fixture], root)

    assert_equal(errors, ["Secret-like pattern `credential URL` in decoded JSON example.json"])


def test_decoded_json_allowlist_is_exact_and_decoded_only() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        escaped_fixture = write_json(
            root,
            ALLOWED_RELATIVE_PATH,
            '{"value":"postgresql://synthetic_user:synthetic_pass\\u0040example.invalid/synthetic_db"}',
        )
        escaped_errors = scan_public_hygiene([escaped_fixture], root, {ALLOWED_DECODED_SECRET})

        raw_fixture = write_json(
            root,
            ALLOWED_RELATIVE_PATH,
            '{"value":"postgresql://synthetic_user:synthetic_pass'
            + '@example.invalid/synthetic_db"}',
        )

        raw_errors = scan_public_hygiene([raw_fixture], root, {ALLOWED_DECODED_SECRET})

    assert_equal(escaped_errors, [])
    assert_equal(raw_errors, [f"Secret-like pattern `credential URL` in {ALLOWED_RELATIVE_PATH}"])


def test_decoded_json_allowlist_does_not_hide_other_paths_or_patterns() -> None:
    same_basename_elsewhere = (
        "docs/invalid-governance-scenario-db-credential-url.contract.json"
    )
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        other_pattern_fixture = write_json(
            root,
            ALLOWED_RELATIVE_PATH,
            '{"value":"' + "ghp_" + ("A" * 36) + '"}',
        )
        other_path_fixture = write_json(
            root,
            same_basename_elsewhere,
            '{"value":"postgresql://synthetic_user:synthetic_pass\\u0040example.invalid/synthetic_db"}',
        )

        other_pattern_errors = scan_public_hygiene(
            [other_pattern_fixture], root, {ALLOWED_DECODED_SECRET}
        )
        other_path_errors = scan_public_hygiene(
            [other_path_fixture], root, {ALLOWED_DECODED_SECRET}
        )

    assert_equal(
        other_pattern_errors,
        [f"Secret-like pattern `GitHub token` in {ALLOWED_RELATIVE_PATH}"],
    )
    assert_equal(
        other_path_errors,
        [f"Secret-like pattern `credential URL` in decoded JSON {same_basename_elsewhere}"],
    )


def test_decoded_json_allowlist_requires_exact_decoded_match() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            ALLOWED_RELATIVE_PATH,
            '{"value":"postgresql://synthetic_user:other_pass\\u0040example.invalid/synthetic_db"}',
        )

        errors = scan_public_hygiene([fixture], root, {ALLOWED_DECODED_SECRET})

    assert_equal(
        errors,
        [f"Secret-like pattern `credential URL` in decoded JSON {ALLOWED_RELATIVE_PATH}"],
    )


def test_malformed_json_still_uses_raw_scan() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            "malformed.json",
            '{"value":"postgresql://synthetic_user:synthetic_pass'
            + '@example.invalid/synthetic_db"',
        )

        errors = scan_public_hygiene([fixture], root)

    assert_equal(errors, ["Secret-like pattern `credential URL` in malformed.json"])


def test_raw_json_secret_is_not_reported_twice_after_decoding() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            "raw-secret.json",
            '{"value":"postgresql://synthetic_user:synthetic_pass'
            + '@example.invalid/synthetic_db"}',
        )

        errors = scan_public_hygiene([fixture], root)

    assert_equal(errors, ["Secret-like pattern `credential URL` in raw-secret.json"])


def test_raw_json_secret_does_not_hide_distinct_decoded_secret() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            "mixed-secret.json",
            '{"values":["postgresql://synthetic_user:synthetic_pass'
            + '@example.invalid/raw_db",'
            + '"postgresql://synthetic_user:other_pass\\u0040example.invalid/escaped_db"]}',
        )

        errors = scan_public_hygiene([fixture], root)

    assert_equal(
        errors,
        [
            "Secret-like pattern `credential URL` in mixed-secret.json",
            "Secret-like pattern `credential URL` in decoded JSON mixed-secret.json",
        ],
    )


def main() -> int:
    test_decoded_json_scan_flags_escaped_credential_url()
    test_decoded_json_allowlist_is_exact_and_decoded_only()
    test_decoded_json_allowlist_does_not_hide_other_paths_or_patterns()
    test_decoded_json_allowlist_requires_exact_decoded_match()
    test_malformed_json_still_uses_raw_scan()
    test_raw_json_secret_is_not_reported_twice_after_decoding()
    test_raw_json_secret_does_not_hide_distinct_decoded_secret()
    print("Validation hygiene tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
