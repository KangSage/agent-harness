#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PKG_DIR="$ROOT_DIR/packages/project-prompt-kit"

require_file() {
  if [[ ! -f "$1" ]]; then
    echo "Missing required file: $1" >&2
    exit 1
  fi
}

require_dir() {
  if [[ ! -d "$1" ]]; then
    echo "Missing required directory: $1" >&2
    exit 1
  fi
}

require_dir "$ROOT_DIR/docs"
require_dir "$PKG_DIR/commands"
require_dir "$PKG_DIR/skills/project-prompt/references"
require_dir "$PKG_DIR/schemas"
require_dir "$PKG_DIR/examples"
require_dir "$PKG_DIR/scripts"
require_dir "$PKG_DIR/tests"

require_file "$ROOT_DIR/README.md"
require_file "$ROOT_DIR/README.ko.md"
require_file "$ROOT_DIR/README.ja.md"
require_file "$ROOT_DIR/SECURITY.md"
require_file "$ROOT_DIR/CONTRIBUTING.md"
require_file "$ROOT_DIR/CHANGELOG.md"
require_file "$ROOT_DIR/.github/workflows/validate.yml"

require_file "$PKG_DIR/README.md"
require_file "$PKG_DIR/.promptkitignore"
require_file "$PKG_DIR/commands/prompt.md"
require_file "$PKG_DIR/commands/project-prompt.md"
require_file "$PKG_DIR/skills/project-prompt/SKILL.md"
require_file "$PKG_DIR/schemas/prompt-contract.schema.json"

if ! grep -q '^# /prompt' "$PKG_DIR/commands/prompt.md"; then
  echo "Expected /prompt command documentation" >&2
  exit 1
fi

if ! grep -q 'Canonical alias for `/prompt`' "$PKG_DIR/commands/project-prompt.md"; then
  echo "Expected /project-prompt alias documentation" >&2
  exit 1
fi

for readme in "$ROOT_DIR/README.md" "$ROOT_DIR/README.ko.md" "$ROOT_DIR/README.ja.md"; do
  if ! grep -q 'English](./README.md) | \[한국어\](./README.ko.md) | \[日本語\](./README.ja.md)' "$readme"; then
    echo "Missing language links in $readme" >&2
    exit 1
  fi
done

echo "Validation passed."
