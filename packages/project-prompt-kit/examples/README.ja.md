# 例

このディレクトリには `project-prompt-kit` の public-safe な例があります。

## Contract の例

`sample-contract.*.json` は、`schemas/prompt-contract.schema.json` で検証される normalized prompt payload です。

- `sample-contract.codex.json`
- `sample-contract.claude.json`
- `sample-contract.generic.json`

新しい prompt contract を書くときの出発点として使います。

## Rendered の例

`rendered/` には、sample contract を target renderer template に適用した最終 prompt の例があります。

- `rendered/codex-review.md`
- `rendered/claude-implement.md`
- `rendered/generic-task.md`

rendered example は documentation fixture であり、generated snapshot ではありません。手動利用時に期待される prompt shape を示します。

## Sample Outputs

`sample-outputs/` には mode-level output shape の例があります。rendered prompt を使った後、agent response がどのような形になり得るかを説明します。

## 安全ルール

例は portable である必要があります。

- relative path だけを使います。
- sanitized project name を使います。
- private username, local absolute path, secret, token, credential-bearing URL を含めません。
- prompt-injection boundary を見える形で維持します。
