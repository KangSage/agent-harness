# agent-harness

[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md)

`agent-harness` is a public monorepo for reusable coding-agent and project-agent harness components.

## Goals
- Build reusable prompt kits, slash commands, workflow templates, validators, examples, and safety patterns.
- Keep artifacts host-neutral so they can be rendered in Codex, Claude, and generic agent environments.
- Default to safe operation: local-first usage, no telemetry, redaction-first handling, and explicit prompt boundaries.

## Monorepo Structure
- `docs/` — principles, architecture, roadmap
- `packages/project-prompt-kit/` — first package scaffold (`v0.1`)
- `.github/workflows/validate.yml` — CI validation for scaffold integrity

## First Package: `project-prompt-kit`
The first package provides a lightweight, host-neutral prompt kit scaffold.

Key command contract:
- Primary command: `/prompt`
- Canonical alias: `/project-prompt`

See: [`packages/project-prompt-kit/README.md`](./packages/project-prompt-kit/README.md)

## Quick Validation
```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

## License
MIT — see [`LICENSE`](./LICENSE).
