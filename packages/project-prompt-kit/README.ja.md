# project-prompt-kit

コーディングエージェント向けの、リポジトリ文脈を扱うプロンプトテンプレートです。

言語: [English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`project-prompt-kit` は、コーディングエージェントやプロジェクトエージェント向けの、軽量で実行環境に依存しないプロンプト用ツール群のひな形（host-neutral prompt kit scaffold）です。あいまいな依頼を、目的（`objective`）、文脈（context）、範囲（scope）、制約（`constraints`）、根拠要件（`evidence_required`）、出力形式（`output_format`）、停止条件（`stop_condition`）を持つ構造化されたプロンプト契約（prompt contract）に変換します。

## コマンド契約

- 基本コマンド: `/prompt`
- 正式エイリアス: `/project-prompt`

対応するモード（mode）:

- `choose`
- `task`
- `plan`
- `implement`
- `review`
- `debug`
- `research`
- `docs`
- `release`
- `correction`
- `handoff`

## スコープ

このパッケージ（package）が現在提供するもの:

- コマンド仕様（command spec）
- スキルのひな形（skill scaffold）
- モード仕様（mode spec）
- プロンプト契約（prompt contract）、プロンプト依頼（prompt request）、モードメタデータスキーマ（mode metadata schema）
- 描画器テンプレート（renderer template）
- 安全な既定値（safety default）
- 例、固定データ（fixture）で裏付けた正解例の出力構造（golden output shape）、検証スクリプト（validation script）

意図的に完全なコマンドラインツール（full CLI）はまだ含めません。`handoff` は対応モード（mode）の一つであり、既定用途（default）や唯一の用途ではありません。

## クイックスタート

このキットは、リポジトリ配布型のプロンプトひな形（repo-distributed prompt scaffold）として使います。

1. `docs/quickstart.ja.md` を読みます。
2. `skills/project-prompt/references/modes/` からモード（mode）を選びます。
3. `skills/project-prompt/references/templates/` から対象描画器（target renderer）を選びます。
4. `examples/sample-contract.*.json` から始めます。
5. 実プロジェクトへ適用する前に `examples/rendered/` と比較します。
6. プロンプト（prompt）作成だけを担当する専用セッションが必要な場合は `docs/prompt-builder-session.ja.md` を使います。
7. 変更を共有する前に検証（validation）を実行します。

このパッケージ（package）は、リポジトリ（repository）を複製（clone）するか、プロジェクトに取り込む（vendor）ことで使えます。まだインストール型 CLI やレジストリ配布パッケージ（registry package）ではありません。

## 安全なデフォルト

- デフォルトで利用情報送信（telemetry）なし
- デフォルトでネットワーク呼び出し（network call）なし
- ローカル優先（local-first）の利用方針
- 機密情報を先に秘匿化する方針（redaction-first）
- `.promptkitignore` 対応
- ホスト側プロンプト（host prompt）と信頼できないプロジェクト入力（project input）の、プロンプト注入境界（prompt injection boundary）を明記
- 共有前に事前確認（preview）
- 公開例では相対パス（relative path）を使う

生成されたプロンプト（prompt）にはプロジェクト文脈が含まれる場合があります。外部へ共有する前に必ず確認してください。

## 構成

- `commands/` — スラッシュコマンド（slash command）の文書
- `skills/project-prompt/` — skill 定義
- `schemas/` — 実行環境に依存しないプロンプト契約（host-neutral contract）
- `examples/` — プロンプト入力値（prompt payload）の例
- `examples/rendered/` — 対象別に描画済みのプロンプト例（target-specific rendered prompt）
- `examples/sample-outputs/` — 正解例のサンプル出力構造（golden sample output shape）
- `docs/prompt-builder-session.ja.md` — プロンプト作成専用セッションのパターン
- `scripts/validate.sh` — 構造/契約の検証（validation）
- `tests/fixtures/` — 有効/無効な契約用固定データ（valid/invalid contract fixture）
- `tests/golden/` — 静的なモード出力構造の例（static mode output shape）
- `tests/validate-fixtures.sh` — 固定データ検証の入口（fixture validation entry point）

## 検証

```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

固定データ（fixture）だけを検証する場合:

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```
