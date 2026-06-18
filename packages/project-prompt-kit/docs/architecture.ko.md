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

v0.2는 portable prompt contract에 계획 검토용 기본 틀(planning governance scaffold)을 더합니다. 포함되는 것은 `plan` mode, optional `governance` field, preset/scenario reference, example, validation입니다. standalone CLI, renderer engine, agent runner, automatic risk classifier는 아직 제공하지 않습니다.
