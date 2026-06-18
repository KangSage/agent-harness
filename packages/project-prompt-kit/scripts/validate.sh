#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 -B "$SCRIPT_DIR/validate_prompt_kit.py"
python3 -B "$SCRIPT_DIR/../tests/test_invalid_fixture_expectations.py"
python3 -B "$SCRIPT_DIR/../tests/test_governance_preset_coverage.py"
