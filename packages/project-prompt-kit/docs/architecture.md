# Architecture

`project-prompt-kit` uses a portable core with host adapters.

```text
mode specs + prompt contract
        |
renderer templates: codex / claude / generic
        |
host adapters: Codex command, Claude slash command, plain Markdown
```

Core mode specs are agent-neutral. Host-specific wording belongs in renderer templates or command adapters only.

v0.2 ships the portable prompt contract plus the planning-governance scaffold: `plan` mode, optional `governance` fields, preset/scenario references, examples, and validation. It still does not ship a standalone CLI, renderer engine, agent runner, or automatic risk classifier.
