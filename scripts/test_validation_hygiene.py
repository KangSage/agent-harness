#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

from validation_hygiene import collect_text_files, scan_public_hygiene


SYNTHETIC_CREDENTIAL_SCHEME = "postgres" + "ql://"
SYNTHETIC_CREDENTIAL_USERINFO = "synthetic_user" + ":" + "synthetic_pass"
SYNTHETIC_CREDENTIAL_HOST = "example.invalid/synthetic_db"
SYNTHETIC_CREDENTIAL_URL = (
    SYNTHETIC_CREDENTIAL_SCHEME + SYNTHETIC_CREDENTIAL_USERINFO + "@" + SYNTHETIC_CREDENTIAL_HOST
)
SYNTHETIC_CREDENTIAL_URL_WITH_ESCAPED_AT = (
    SYNTHETIC_CREDENTIAL_SCHEME + SYNTHETIC_CREDENTIAL_USERINFO + "\\u0040" + SYNTHETIC_CREDENTIAL_HOST
)
ALLOWED_RELATIVE_PATH = (
    "packages/project-prompt-kit/tests/fixtures/invalid/"
    "runtime-only-escaped-secret.contract.json"
)
ALLOWED_DECODED_SECRET = (
    ALLOWED_RELATIVE_PATH,
    "credential URL",
    SYNTHETIC_CREDENTIAL_URL,
)
LOCAL_PATH_TERM = "/U" + "sers/"


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
            '{"value":"' + SYNTHETIC_CREDENTIAL_URL_WITH_ESCAPED_AT + '"}',
        )

        errors = scan_public_hygiene([fixture], root)

    assert_equal(errors, ["Secret-like pattern `credential URL` in decoded JSON example.json"])


def test_collect_text_files_ignores_generated_dependency_dirs() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        keep = write_json(root, "packages/project/fixtures/keep.json", '{"value":"synthetic"}')
        ignored = write_json(root, "packages/project/node_modules/generated/leak.json", '{"value":"synthetic"}')

        files = collect_text_files([root / "packages"])

    assert_equal(files, [keep])
    assert ignored not in files


def test_decoded_json_scan_flags_escaped_forbidden_terms_and_models() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            "escaped-public.json",
            '{"path":"\\/'
            + "U"
            + 'sers\\/example\\/repo","model":"gpt-\\u0035.5"}',
        )

        errors = scan_public_hygiene([fixture], root)

    assert_equal(
        errors,
        [
            f"Forbidden public reference `{LOCAL_PATH_TERM}` in decoded JSON escaped-public.json",
            "Hardcoded model name in decoded JSON escaped-public.json",
        ],
    )


def test_decoded_json_allowlist_is_exact_and_decoded_only() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        escaped_fixture = write_json(
            root,
            ALLOWED_RELATIVE_PATH,
            '{"value":"' + SYNTHETIC_CREDENTIAL_URL_WITH_ESCAPED_AT + '"}',
        )
        escaped_errors = scan_public_hygiene([escaped_fixture], root, {ALLOWED_DECODED_SECRET})

        raw_fixture = write_json(
            root,
            ALLOWED_RELATIVE_PATH,
            '{"value":"' + SYNTHETIC_CREDENTIAL_URL + '"}',
        )

        raw_errors = scan_public_hygiene([raw_fixture], root, {ALLOWED_DECODED_SECRET})

    assert_equal(escaped_errors, [])
    assert_equal(raw_errors, [f"Secret-like pattern `credential URL` in {ALLOWED_RELATIVE_PATH}"])


def test_decoded_json_allowlist_allows_only_one_occurrence() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            ALLOWED_RELATIVE_PATH,
            '{"values":['
            + '"'
            + SYNTHETIC_CREDENTIAL_URL_WITH_ESCAPED_AT
            + '",'
            + '"'
            + SYNTHETIC_CREDENTIAL_URL_WITH_ESCAPED_AT
            + '"'
            + "]}",
        )

        errors = scan_public_hygiene([fixture], root, {ALLOWED_DECODED_SECRET})

    assert_equal(
        errors,
        [f"Secret-like pattern `credential URL` in decoded JSON {ALLOWED_RELATIVE_PATH}"],
    )


def test_decoded_json_allowlist_does_not_hide_other_paths_or_patterns() -> None:
    same_basename_elsewhere = (
        "docs/runtime-only-escaped-secret.contract.json"
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
            '{"value":"' + SYNTHETIC_CREDENTIAL_URL_WITH_ESCAPED_AT + '"}',
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
            '{"value":"'
            + SYNTHETIC_CREDENTIAL_SCHEME
            + "synthetic_user"
            + ":"
            + "other_pass"
            + "\\u0040"
            + SYNTHETIC_CREDENTIAL_HOST
            + '"}',
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
            '{"value":"' + SYNTHETIC_CREDENTIAL_URL + '"',
        )

        errors = scan_public_hygiene([fixture], root)

    assert_equal(errors, ["Secret-like pattern `credential URL` in malformed.json"])


def test_raw_json_secret_is_not_reported_twice_after_decoding() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            "raw-secret.json",
            '{"value":"' + SYNTHETIC_CREDENTIAL_URL + '"}',
        )

        errors = scan_public_hygiene([fixture], root)

    assert_equal(errors, ["Secret-like pattern `credential URL` in raw-secret.json"])


def test_raw_json_secret_does_not_hide_distinct_decoded_secret() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = write_json(
            root,
            "mixed-secret.json",
            '{"values":["'
            + SYNTHETIC_CREDENTIAL_SCHEME
            + SYNTHETIC_CREDENTIAL_USERINFO
            + "@"
            + "example.invalid/raw_db"
            + '","'
            + SYNTHETIC_CREDENTIAL_SCHEME
            + "synthetic_user"
            + ":"
            + "other_pass"
            + "\\u0040example.invalid/escaped_db"
            + '"]}',
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
    test_collect_text_files_ignores_generated_dependency_dirs()
    test_decoded_json_scan_flags_escaped_forbidden_terms_and_models()
    test_decoded_json_allowlist_is_exact_and_decoded_only()
    test_decoded_json_allowlist_allows_only_one_occurrence()
    test_decoded_json_allowlist_does_not_hide_other_paths_or_patterns()
    test_decoded_json_allowlist_requires_exact_decoded_match()
    test_malformed_json_still_uses_raw_scan()
    test_raw_json_secret_is_not_reported_twice_after_decoding()
    test_raw_json_secret_does_not_hide_distinct_decoded_secret()
    print("Validation hygiene tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
