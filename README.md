# agent-harness

[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md)

`agent-harness` is a public monorepo for reusable coding-agent and project-agent harness components.

Tagline for the first package: **Repo-aware prompt templates for coding agents.**

## Goals
- Build reusable prompt kits, slash commands, workflow templates, validators, examples, and safety patterns.
- Keep artifacts host-neutral so they can be rendered in Codex, Claude, and generic agent environments.
- Default to safe operation: local-first usage, no network calls, no telemetry, redaction-first handling, and explicit prompt boundaries.
- Keep packages independent from any single local workflow, agent framework, or private workspace.

## Monorepo Structure
- `docs/` — principles, architecture, roadmap
- `packages/project-prompt-kit/` — first package scaffold (`v0.1`)
- `.github/workflows/validate.yml` — CI validation for scaffold integrity

## First Package: `project-prompt-kit`
The first package provides a lightweight, host-neutral prompt kit scaffold. It is a general project prompt kit, not a handoff-only tool.

Key command contract:
- Primary command: `/prompt`
- Canonical alias: `/project-prompt`

See: [`packages/project-prompt-kit/README.md`](./packages/project-prompt-kit/README.md)

## Quick Validation
```bash
bash scripts/validate.sh
```

Generated prompts may contain project context. Review them before sharing. Generated prompt output belongs to the user or project that created it, not to this repository.

## License
MIT — see [`LICENSE`](./LICENSE).
