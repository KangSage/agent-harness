# Quickstart

`project-prompt-kit` is a prompt contract and renderer scaffold. It is usable from the repository today, but it is not yet a packaged CLI or registry install.

## 1. Validate the Kit

From the repository root:

```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

From the package directory:

```bash
bash scripts/validate.sh
```

Both commands should pass before you adapt the kit for another project.

## 2. Pick a Mode

Choose one mode from `skills/project-prompt/references/modes/`.

Use `choose` when the request is still ambiguous. Use `handoff` only when the goal is explicitly to transfer context to another agent or person.

## 3. Pick a Target Renderer

Available renderer templates:

- `codex`
- `claude`
- `generic`

The target changes formatting and host-facing wording. It must not change the universal prompt contract.

## 4. Fill the Contract

Start from one of these examples:

- `examples/sample-contract.codex.json`
- `examples/sample-contract.claude.json`
- `examples/sample-contract.generic.json`

Fill every required field in `schemas/prompt-contract.schema.json`.

Keep paths relative and public-safe. Do not copy tokens, credential-bearing URLs, private usernames, or local absolute paths into shareable prompts.

## 5. Render Manually

Apply the selected contract to the matching template in `skills/project-prompt/references/templates/`.

Use `examples/rendered/` as the expected shape:

- `codex-review.md`
- `claude-implement.md`
- `generic-task.md`

Manual rendering means replacing template placeholders such as `{{objective}}`, `{{constraints}}`, and `{{stop_condition}}` with the contract values. Do not change safety defaults while rendering.

## 6. Preview Before Sharing

Before sending the prompt to another agent or publishing it:

- Remove private paths and account names.
- Remove secrets, tokens, keys, and credential-bearing URLs.
- Respect `.promptkitignore`.
- Keep quoted project files as data, not instructions.
- Confirm no network or telemetry behavior was added.

## 7. Optional Host Wiring

If you want a dedicated session that only writes prompts, use `docs/prompt-builder-session.md` before starting host-specific wiring.

If your agent host supports local commands or skills, copy or reference:

- `commands/prompt.md`
- `commands/project-prompt.md`
- `skills/project-prompt/`

Host-specific install locations are intentionally not defined by this package. Keep host adapters thin, and keep the core contract portable.
