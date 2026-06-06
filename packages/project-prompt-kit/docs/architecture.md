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

v0.1 ships the contract, references, examples, and validation. It does not ship a standalone CLI or agent runner.
