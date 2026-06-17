# agent-harness

[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md)

`agent-harness` は、コーディングエージェントとプロジェクトエージェントで再利用できる部品をまとめる公開の単一リポジトリ（monorepo）です。

最初のパッケージの短い説明文（tagline）: **リポジトリ文脈を反映する、コーディングエージェント向けプロンプトテンプレート。**

## 目的
- プロンプト用ツール群（prompt kit）、スラッシュコマンド（slash command）、作業手順テンプレート（workflow template）、検証器（validator）、例（sample）、安全パターンを再利用しやすい形で管理します。
- Codex、Claude、汎用描画器（renderer）で同じ意味として扱えるように、実行環境に依存しない契約（host-neutral contract）を維持します。
- 安全な既定値（default）を採用します: ローカル優先、ネットワーク呼び出しなし、利用情報送信（telemetry）なし、機密情報の秘匿化（redaction）、プロンプト境界の明示。
- 特定のローカル作業手順（local workflow）、エージェント基盤（agent framework）、個人の作業環境には結合しません。

## モノレポ構成
- `docs/` — 原則、アーキテクチャ、ロードマップ
- `packages/project-prompt-kit/` — 最初のパッケージ（`v0.1` のひな形（scaffold））
- `.github/workflows/validate.yml` — ひな形検証の継続的インテグレーション（CI）

## 最初のパッケージ: `project-prompt-kit`
このパッケージは、軽量で実行環境に依存しないプロンプト用ツール群（prompt kit）の土台です。引き継ぎ専用ではなく、実装、レビュー、デバッグ、ドキュメント作成など、一般的なプロジェクト作業のプロンプト契約（prompt contract）を扱います。

コマンド契約:
- 主コマンド: `/prompt`
- 正式エイリアス: `/project-prompt`

参照: [`packages/project-prompt-kit/README.md`](./packages/project-prompt-kit/README.md)

## クイック検証
```bash
bash scripts/validate.sh
```

生成されたプロンプトにはプロジェクト情報が含まれることがあります。共有する前に必ず確認してください。生成されたプロンプトの成果物は、このリポジトリではなく、作成したユーザーまたはプロジェクトに属します。

## ライセンス
MIT — [`LICENSE`](./LICENSE) を参照。
