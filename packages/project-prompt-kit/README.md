# project-prompt-kit

Lightweight host-neutral prompt kit scaffold for project-agent workflows.

## Command Contract
- Primary command: `/prompt`
- Canonical alias: `/project-prompt`

## Scope
This package currently provides:
- command specs
- a skill scaffold
- prompt contract schema
- safety defaults
- examples and validation script

It intentionally does **not** include a full CLI in v0.1.

## Safety Defaults
- No telemetry by default
- Local-first usage guidance
- Redaction-first handling for sensitive content
- `.promptkitignore` support
- Prompt-injection boundary notes for host prompts and untrusted project input

## Layout
- `commands/` — slash command docs
- `skills/project-prompt/` — skill definition
- `schemas/` — host-neutral contracts
- `examples/` — example prompt payloads
- `scripts/validate.sh` — structure/contract validation
- `tests/` — placeholder for future automated tests
