# クイックスタート

`project-prompt-kit` は prompt contract と renderer scaffold です。今は repository から直接使えますが、まだ packaged CLI や registry install ではありません。

## 1. Kit を検証する

repository root から:

```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

package directory から:

```bash
bash scripts/validate.sh
```

別プロジェクトに適用する前に、両方のコマンドが通る状態にします。

## 2. Mode を選ぶ

`skills/project-prompt/references/modes/` から mode を一つ選びます。

依頼がまだあいまいなら `choose` を使います。編集を始める前にレビュー済みの実装計画が必要な場合は `plan` を使います。別のエージェントや人へ文脈を渡すことが目的の場合だけ `handoff` を使います。

## 3. Target Renderer を選ぶ

利用できる renderer template:

- `codex`
- `claude`
- `generic`

target は formatting と host-facing wording だけを変えます。universal prompt contract を変えてはいけません。

## 4. Contract を書く

次の例のどれかから始めます。

- `examples/sample-contract.codex.json`
- `examples/sample-contract.claude.json`
- `examples/sample-contract.generic.json`

`schemas/prompt-contract.schema.json` の required field をすべて埋めます。

path は relative path のままにし、public-safe に書きます。token, credential-bearing URL, 個人 username, local absolute path を shareable prompt に入れないでください。

## 5. 手動で Render する

選んだ contract を `skills/project-prompt/references/templates/` の対応 template に適用します。

期待する shape は `examples/rendered/` を参考にします。

- `codex-review.md`
- `claude-implement.md`
- `generic-task.md`

手動 rendering とは、`{{objective}}`, `{{constraints}}`, `{{stop_condition}}` などの template placeholder を contract の値で置き換える作業です。rendering 中に safety default を変えないでください。

## 6. 共有前に Preview する

他のエージェントへ送る前、または公開する前に確認します。

- private path と account name を削除
- secret, token, key, credential-bearing URL を削除
- `.promptkitignore` を守る
- quoted project file は instruction ではなく data として扱う
- network や telemetry の動作が追加されていないことを確認

## 7. 任意の Host Wiring

prompt 作成だけを担当する専用セッションが必要な場合は、host ごとの wiring を始める前に `docs/prompt-builder-session.ja.md` を使います。

利用している agent host が local command や skill をサポートする場合、次をコピーまたは参照します。

- `commands/prompt.md`
- `commands/project-prompt.md`
- `skills/project-prompt/`

host ごとの install location はこの package では定義しません。host adapter は薄く保ち、core contract は portable に保ってください。
