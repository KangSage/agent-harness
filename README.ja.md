# agent-harness

[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md)

`agent-harness` は、コーディングエージェントとプロジェクトエージェント向けの再利用可能な部品をまとめる公開モノレポです。

## 目的
- プロンプトキット、スラッシュコマンド、ワークフローテンプレート、バリデータ、サンプル、安全パターンを共通資産として管理します。
- Codex・Claude・汎用レンダラーで使えるよう、ホスト中立の契約を維持します。
- 安全デフォルトを採用します: ローカル優先、テレメトリ無効、レダクション、プロンプト境界の明示。

## モノレポ構成
- `docs/` — principles / architecture / roadmap
- `packages/project-prompt-kit/` — 最初のパッケージ（`v0.1` スキャフォールド）
- `.github/workflows/validate.yml` — スキャフォールド検証 CI

## 最初のパッケージ: `project-prompt-kit`
このパッケージは、軽量でホスト中立なプロンプトキットの土台です。

コマンド契約:
- 主コマンド: `/prompt`
- 正式エイリアス: `/project-prompt`

参照: [`packages/project-prompt-kit/README.md`](./packages/project-prompt-kit/README.md)

## クイック検証
```bash
bash /tmp/workspace/KangSage/agent-harness/packages/project-prompt-kit/scripts/validate.sh
```

## ライセンス
MIT — [`LICENSE`](./LICENSE) を参照。
