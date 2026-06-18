#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 -B "$SCRIPT_DIR/../scripts/validate_prompt_kit.py" --fixtures-only
python3 -B "$SCRIPT_DIR/test_invalid_fixture_expectations.py"
python3 -B "$SCRIPT_DIR/test_governance_preset_coverage.py"
