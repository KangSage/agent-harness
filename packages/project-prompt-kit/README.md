# project-prompt-kit

Repo-aware prompt templates for coding agents.

`project-prompt-kit` is a lightweight host-neutral prompt kit scaffold for coding-agent and project-agent workflows. It turns loose intent into a structured prompt contract with objective, context, scope, constraints, evidence requirements, output format, and stop condition.

## Command Contract
- Primary command: `/prompt`
- Canonical alias: `/project-prompt`

Supported modes in v0.1:
- `choose`
- `task`
- `implement`
- `review`
- `debug`
- `research`
- `docs`
- `release`
- `correction`
- `handoff`

## Scope
This package currently provides:
- command specs
- a skill scaffold
- mode specs
- prompt contract schema and renderer templates
- safety defaults
- examples, golden sample outputs, and validation script

It intentionally does **not** include a full CLI in v0.1. Handoff is one supported mode, not the default or only use case.

## Safety Defaults
- No telemetry by default
- No network calls by default
- Local-first usage guidance
- Redaction-first handling for sensitive content
- `.promptkitignore` support
- Prompt-injection boundary notes for host prompts and untrusted project input
- Preview output before sharing
- Relative paths in public examples

Generated prompts may contain project context. Review them before sharing.

## Layout
- `commands/` — slash command docs
- `skills/project-prompt/` — skill definition
- `schemas/` — host-neutral contracts
- `examples/` — example prompt payloads
- `examples/sample-outputs/` — golden sample output shape
- `scripts/validate.sh` — structure/contract validation
- `tests/` — placeholder for future automated tests

## Validation
```bash
bash packages/project-prompt-kit/scripts/validate.sh
```
