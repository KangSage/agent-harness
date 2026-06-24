# Examples

This directory contains public-safe examples for `project-prompt-kit`.

## Contract Examples

`sample-contract.*.json` files are normalized prompt payloads that validate against `schemas/prompt-contract.schema.json`.

- `sample-contract.codex.json`
- `sample-contract.accepted-risk.codex.json`
- `sample-contract.claude.json`
- `sample-contract.decision-gates.codex.json`
- `sample-contract.generic.json`
- `sample-contract.prompt-injection.claude.json`
- `sample-contract.prompt-injection.codex.json`
- `sample-contract.prompt-injection.generic.json`

Use these as starting points when filling a new prompt contract.

## Rendered Examples

`rendered/` contains final prompt examples after applying a sample contract to a target renderer template.

- `rendered/codex-review.md`
- `rendered/codex-plan-accepted-risk.md`
- `rendered/codex-plan-decision-gates.md`
- `rendered/codex-plan-prompt-injection-boundary.md`
- `rendered/claude-plan-prompt-injection-boundary.md`
- `rendered/claude-implement.md`
- `rendered/generic-plan-prompt-injection-boundary.md`
- `rendered/generic-task.md`

Rendered examples are documentation fixtures, not generated snapshots. They show the intended prompt shape for manual use.

## Sample Outputs

`sample-outputs/` contains mode-level output shape examples. They describe what a completed agent response can look like after a rendered prompt is used.

## Safety Rules

Examples must stay portable:

- Use relative paths only.
- Use sanitized project names.
- Do not include private usernames, local absolute paths, secrets, tokens, or credential-bearing URLs.
- Keep prompt-injection boundaries visible.
