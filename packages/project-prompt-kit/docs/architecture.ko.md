# Architecture

`project-prompt-kit`은 portable core와 host adapter 구조를 사용합니다.

```text
mode specs + prompt contract
        |
renderer templates: codex / claude / generic
        |
host adapters: Codex command, Claude slash command, plain Markdown
```

core mode spec은 agent-neutral해야 합니다. host-specific wording은 renderer template이나 command adapter에만 둡니다.

v0.1은 contract, reference, example, validation을 제공합니다. standalone CLI나 agent runner는 제공하지 않습니다.
