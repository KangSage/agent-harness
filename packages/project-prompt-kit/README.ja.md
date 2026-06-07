# project-prompt-kit

コーディングエージェント向けの、リポジトリ文脈を扱うプロンプトテンプレートです。

言語: [English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`project-prompt-kit` は、コーディングエージェントやプロジェクトエージェントのための軽量な、ホスト非依存のプロンプトキット scaffold です。あいまいな依頼を、objective, context, scope, constraints, evidence requirements, output format, stop condition を持つ構造化された prompt contract に変換します。

## コマンド契約

- 基本コマンド: `/prompt`
- 標準エイリアス: `/project-prompt`

v0.1 で対応する mode:

- `choose`
- `task`
- `implement`
- `review`
- `debug`
- `research`
- `docs`
- `release`
- `correction`
- `handoff`

## スコープ

この package が現在提供するもの:

- command spec
- skill scaffold
- mode spec
- prompt contract, prompt request, mode metadata schema
- renderer template
- safety default
- example, fixture-backed golden output shape, validation script

v0.1 では、意図的に full CLI は含めません。`handoff` は対応 mode の一つであり、default や唯一の用途ではありません。

## クイックスタート

このキットは repo-distributed prompt scaffold として使います。

1. `docs/quickstart.ja.md` を読みます。
2. `skills/project-prompt/references/modes/` から mode を選びます。
3. `skills/project-prompt/references/templates/` から target renderer を選びます。
4. `examples/sample-contract.*.json` から始めます。
5. 実プロジェクトへ適用する前に `examples/rendered/` と比較します。
6. 変更を共有する前に validation を実行します。

この package は、repository を clone するか vendor すれば使えます。まだインストール型 CLI や registry package ではありません。

## 安全なデフォルト

- デフォルトで telemetry なし
- デフォルトで network call なし
- local-first の利用方針
- 機密情報は redaction-first で扱う
- `.promptkitignore` 対応
- host prompt と信頼できない project input の prompt injection boundary を明記
- 共有前に preview
- 公開例では relative path を使う

生成された prompt にはプロジェクト文脈が含まれる場合があります。外部へ共有する前に必ず確認してください。

## 構成

- `commands/` — slash command 文書
- `skills/project-prompt/` — skill 定義
- `schemas/` — host-neutral contract
- `examples/` — prompt payload の例
- `examples/rendered/` — target-specific rendered prompt の例
- `examples/sample-outputs/` — golden sample output shape
- `scripts/validate.sh` — 構造/契約 validation
- `tests/fixtures/` — valid/invalid contract fixture
- `tests/golden/` — static mode output shape の例
- `tests/validate-fixtures.sh` — fixture validation entry point

## 検証

```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

fixture だけを検証する場合:

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```
