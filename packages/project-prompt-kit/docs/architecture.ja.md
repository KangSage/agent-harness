# Architecture

`project-prompt-kit` は portable core と host adapter の構造を使います。

```text
mode specs + prompt contract
        |
renderer templates: codex / claude / generic
        |
host adapters: Codex command, Claude slash command, plain Markdown
```

core mode spec は agent-neutral である必要があります。host-specific wording は renderer template または command adapter にだけ置きます。

v0.2 は portable prompt contract に、計画レビュー用の土台（planning governance scaffold）を追加します。含まれるものは `plan` mode、optional `governance` field、preset/scenario reference、example、validation です。standalone CLI、renderer engine、agent runner、automatic risk classifier はまだ提供しません。
