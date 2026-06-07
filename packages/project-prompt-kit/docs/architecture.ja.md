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

v0.1 は contract, reference, example, validation を提供します。standalone CLI や agent runner は提供しません。
