#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ROOT_DIR/scripts/validate_repo.py"
bash "$ROOT_DIR/packages/project-prompt-kit/scripts/validate.sh"
