# Prompt Builder セッション

Prompt Builder セッションは、1つのエージェントセッションで project prompt だけを作り、実際の作業は別のエージェントセッションで行うためのパターンです。

既存プロジェクト、リスクの高い作業、本番調査、長い handoff に向いています。Prompt Builder セッションは、まだ粗い意図を contract JSON と rendered prompt に変換します。コード編集、本番システム接続、実作業の実行は行いません。

## セッション開始プロンプト

対象プロジェクト内で新しいエージェントセッションを開き、次のプロンプトを貼り付けます。

```text
あなたはこのプロジェクトの Prompt Builder です。

.tools/project-prompt-kit を使って、Codex 作業用 prompt だけを作成してください。
コード編集、git commit、DB 接続、本番作業、依頼された実作業の実行はしないでください。

私が提供する目標、範囲、背景、制約をもとに:
1. mode を選ぶ、または確認する
2. contract JSON を作成する
3. rendered Codex prompt markdown を作成する
4. 必須情報が不足している場合だけ、短い質問を1つする

プロジェクトルール:
- AGENTS.md と下位の AGENTS.md に従う
- .promptkitignore を守る
- secret、environment 値、credential-bearing URL、local absolute path を出力しない
- 本番システムに接続しない
```

## 依頼の形

セッション開始プロンプトの後は、次の形で依頼します。

```text
mode: debug

目標:
本番環境のポイント送信トランザクションデータの整合性を調査する。

進め方:
worker は本番 DB に直接接続しない。
worker は read-only SQL を段階的に作成する。
私が本番 DB で各 SQL を実行し、その結果を返す。
worker は結果を解釈し、次の read-only SQL を提案する。

範囲:
ポイントドメインのみ。

制約:
- AGENTS.md に従う
- .promptkitignore を守る
- secret、env 値、local absolute path を出力しない
- read-only の SELECT/WITH SQL のみ許可
- UPDATE、DELETE、INSERT、ALTER、DROP、LOCK は禁止
- 原因分析のみ行い、補正作業は実行しない

出力:
contract JSON と rendered Codex prompt markdown。
```

## ローカル成果物

ローカル専用で使う場合、生成した prompt 成果物は vendored kit の下に置きます。

```text
.tools/project-prompt-kit/local/contracts/
.tools/project-prompt-kit/local/rendered/
```

プロジェクトで kit を意図的に vendor 管理しない場合は、`.tools/` を git から除外してください。

## 役割分離

- Prompt Builder セッション: prompt contract と rendered prompt だけを作成します。
- Worker セッション: rendered prompt を実行します。
- 人間の運用者: リスクの高い操作を承認し、本番専用の read-only query が必要な場合に自分で実行します。

この形にすると、prompt 作成は portable に保ちながら、本番データとプロジェクト secret の safety boundary を守れます。
