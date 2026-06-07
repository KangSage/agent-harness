# project-prompt-kit

Repo-aware prompt templates for coding agents.

Languages: [English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

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
- prompt contract, prompt request, and mode metadata schemas
- renderer templates
- safety defaults
- examples, fixture-backed golden output shapes, and validation scripts

It intentionally does **not** include a full CLI in v0.1. Handoff is one supported mode, not the default or only use case.

## Quickstart
Use the kit as a repo-distributed prompt scaffold:

1. Read `docs/quickstart.md`.
2. Pick a mode from `skills/project-prompt/references/modes/`.
3. Pick a target renderer from `skills/project-prompt/references/templates/`.
4. Start from `examples/sample-contract.*.json`.
5. Compare against `examples/rendered/` before adapting it to a real project.
6. Run validation before sharing changes.

The package is usable after cloning or vendoring this repository. It is not yet an installed CLI or registry package.

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
- `examples/rendered/` — target-specific rendered prompt examples
- `examples/sample-outputs/` — golden sample output shape
- `scripts/validate.sh` — structure/contract validation
- `tests/fixtures/` — valid and invalid contract fixtures
- `tests/golden/` — static mode output shape examples
- `tests/validate-fixtures.sh` — fixture validation entry point

## Validation
```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

Fixture-only validation:

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```
