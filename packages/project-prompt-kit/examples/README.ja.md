# 例

このディレクトリには `project-prompt-kit` の公開しても安全な例（public-safe examples）があります。

## 契約の例（Contract）

`sample-contract.*.json` は、`schemas/prompt-contract.schema.json` で検証される正規化済みプロンプト入力値（normalized prompt payload）です。

- `sample-contract.codex.json`
- `sample-contract.accepted-risk.codex.json`
- `sample-contract.claude.json`
- `sample-contract.decision-gates.codex.json`
- `sample-contract.generic.json`
- `sample-contract.prompt-injection.claude.json`
- `sample-contract.prompt-injection.codex.json`
- `sample-contract.prompt-injection.generic.json`

新しいプロンプト契約（prompt contract）を書くときの出発点として使います。

## 描画済みの例（Rendered）

`rendered/` には、サンプル契約（sample contract）を対象の描画器テンプレート（target renderer template）に適用した最終プロンプト（prompt）の例があります。

- `rendered/codex-review.md`
- `rendered/codex-plan-accepted-risk.md`
- `rendered/codex-plan-decision-gates.md`
- `rendered/codex-plan-prompt-injection-boundary.md`
- `rendered/claude-plan-prompt-injection-boundary.md`
- `rendered/claude-implement.md`
- `rendered/generic-plan-prompt-injection-boundary.md`
- `rendered/generic-task.md`

描画済みの例（rendered example）は文書用の固定データ（documentation fixture）であり、生成されたスナップショット（generated snapshot）ではありません。手動利用時に期待されるプロンプトの形（prompt shape）を示します。

## 出力例（Sample Outputs）

`sample-outputs/` にはモード単位の出力構造（mode-level output shape）の例があります。描画済みプロンプト（rendered prompt）を使った後、エージェント応答（agent response）がどのような形になり得るかを説明します。

## 安全ルール

例は持ち運び可能（portable）である必要があります。

- 相対パス（relative path）だけを使います。
- 無害化済みプロジェクト名（sanitized project name）を使います。
- 非公開ユーザー名（private username）、ローカル絶対パス（local absolute path）、秘密情報（secret）、トークン（token）、認証情報を含む URL（credential-bearing URL）を含めません。
- プロンプト注入境界（prompt-injection boundary）を見える形で維持します。
