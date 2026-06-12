# Prompt Builder セッション

Prompt Builder セッションは、1つのエージェントセッションで project prompt だけを作り、実際の作業は別のエージェントセッションで行うためのパターンです。

既存プロジェクト、リスクの高い作業、本番調査、長い handoff に向いています。Prompt Builder セッションは、まだ整理されていない意図を contract JSON と rendered prompt に変換します。コード編集、本番システムへの接続、実作業の実行は行いません。

## セッション開始プロンプト

対象プロジェクト内で新しいエージェントセッションを開き、次のプロンプトを貼り付けます。

```text
あなたはこのプロジェクトの Prompt Builder です。

.tools/project-prompt-kit を使って、project prompt のみを作成してください。
コード編集、git commit、DB 接続、本番作業、依頼された実作業の実行はしないでください。

私が提供する目標、範囲、背景、制約をもとに:
1. mode と target renderer を選ぶ、または確認する
2. contract JSON を作成する
3. rendered prompt markdown を作成する
4. workspace strategy が提供された場合は rendered prompt に反映する
5. infrastructure boundaries が提供された場合は rendered prompt に反映する
6. communication policy が提供された場合は rendered prompt に反映する
7. role-specific review が worker prompt の品質を上げる場合は review panel を選ぶ
8. 必須情報が不足している場合だけ、短い質問を1つする

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

target renderer:
codex、claude、generic のいずれか

作業スペース方針:
現在の checkout は他のセッションと共有されている可能性があり、無関係なローカル変更を含む可能性がある。
worker は現在の checkout を read-only として扱う。
編集前に remote を fetch し、指定された remote base ref を基準に新しい worktree を作成する。
codex/<task-slug> のようなタスク専用 branch を使う。
例: git worktree add ../<repo>-<task-slug> -b codex/<task-slug> origin/<base-branch>
worker は新しい worktree の中だけで編集、テスト、commit、push を行う。
worker は現在の checkout で reset、clean、checkout、revert を実行しない。

インフラ境界:
worker は本番 DB、本番 API、cloud console、secret store、admin dashboard に直接接続しない。
本番データが必要な場合、worker は read-only SQL を段階的に作成する。
私が本番 DB で各 SQL を実行し、その結果を返す。
許可 SQL: read-only の SELECT/WITH query。
禁止 SQL: UPDATE、DELETE、INSERT、ALTER、DROP、LOCK、transaction control statement。
worker は secret、credential、token、environment 値を要求、出力、推測しない。
worker は返された本番結果を sensitive data として扱い、必要な最小限の根拠だけ引用する。

communication policy:
worker はユーザーへの質問、進捗報告、最終まとめをユーザーの言語で書く。
agent-to-agent handoff、内部調整メモ、短い技術 brief は simple English を使う。
agent-to-agent English は短く、直接的で、余計な表現を減らす。
code、command、SQL、log、error、identifier、file path は翻訳しない。
SQL の目的と解釈はユーザーの言語で説明し、SQL 本文はそのまま維持する。
本番 query の結果が必要な場合、ユーザーに一度に1つずつユーザーの言語で質問する。

review panel:
この作業に必要な役割だけを選ぶ。
実装作業では CTO Reviewer、Software Architect、QA Engineer、Security / Privacy Reviewer を含める。
本番障害や本番調査では CTO Reviewer、Software Architect、QA Engineer、Operations / CS Lead、Security / Privacy Reviewer を含める。
policy、terms、customer notice では Legal / Compliance Advisor、Operations / CS Lead、Product / Information Architecture Reviewer、Growth / Marketing Reviewer を含める。
新機能企画では CTO Reviewer、Product / Information Architecture Reviewer、UX / Product Designer、Growth / Marketing Reviewer、QA Engineer を含める。
docs や handoff では Product / Information Architecture Reviewer、Operations / CS Lead、QA Engineer、CTO Reviewer を含める。
Legal / Compliance Advisor は確定的な法律助言ではなく、risk identification と lawyer-review flags に限定する。

目標:
本番環境のポイント移転トランザクションデータの整合性を調査する。

進め方:
worker は結果を解釈し、次の read-only SQL を提案する。

範囲:
ポイントドメインのみ。

制約:
- AGENTS.md に従う
- .promptkitignore を守る
- secret、env 値、local absolute path を出力しない
- 原因分析のみ行い、補正作業は実行しない

出力:
contract JSON と rendered prompt markdown。
```

## 作業スペース方針 (Workspace Strategy)

現在の checkout が共有中、dirty 状態、または他のエージェントセッションで使用中の場合は、workspace strategy を使います。Prompt Builder はこの方針を rendered worker prompt に入れ、worker がどこで write 作業をしてよいかを明確にします。

v0.1 では、optional contract schema field として扱います。すべての prompt で必須にはしません。read-only 作業やドキュメント作業では、worktree 分離が不要な場合があるためです。

推奨 worker 方針:

```text
現在の checkout は read-only context として扱う。
worktree 作成前に git fetch origin を実行する。
指定された remote base ref からタスク専用 worktree を作成する。
指定された branch prefix でタスク専用 branch を作成する。
新しい worktree 内で AGENTS.md を再確認してから編集する。
編集、テスト、commit、push は新しい worktree 内だけで行う。
既存 checkout の無関係なファイルを reset、clean、checkout、revert しない。
```

## インフラ境界 (Infrastructure Boundaries)

作業が DB、本番 API、cloud console、secret store、admin dashboard などの外部システムに関係する場合は、infrastructure boundaries を使います。Prompt Builder は、アクセスルールを一般的な制約リストに埋め込まず、rendered worker prompt の中で独立した境界として明確に書きます。

v0.1 では、optional contract schema field として扱います。すべての prompt で必須にはしません。local-only prompt では外部インフラに触れない場合があるためです。

推奨 worker 方針:

```text
worker は本番インフラに直接接続しない。
worker は人間の運用者に、承認済みの read-only command または query の実行を依頼できる。
本番 SQL は、prompt が明示的に追加許可しない限り read-only SELECT/WITH のみ使う。
worker は各 query の目的を先に説明してから query を提示する。
worker は人間が返した結果を受け取ってから、次の本番 query を提案する。
worker は secret、token、credential、environment 値を要求、公開、推測しない。
返された本番データは sensitive data として扱い、必要な最小限の根拠だけ引用する。
```

## コミュニケーション方針 (Communication Policy)

rendered prompt は一つの言語で書かれていても、worker がユーザーには別の言語で話す必要がある場合は communication policy を使います。Prompt Builder は、user-facing language と agent-to-agent coordination language を分けて明確に書きます。

v0.1 では、optional contract schema field として扱います。すべての prompt で必須にはしません。prompt によっては、すでに一つの明確なコミュニケーション言語があるためです。

推奨 worker 方針:

```text
ユーザーへの質問、進捗報告、最終まとめはユーザーの言語で書く。
agent-to-agent handoff と短い技術調整メモは simple English を使う。
agent-to-agent English は短く、直接的で、余計な表現を減らす。
code、command、SQL、log、error、identifier、file path は翻訳しない。
SQL の目的と解釈はユーザーの言語で説明し、SQL 本文はそのまま維持する。
本番結果が必要な場合、user-facing question は一度に1つだけにする。
```

## レビューパネル (Review Panel)

実装、リリース、policy 公開、customer-facing communication の前に、役割ごとの観点で確認したい場合は review panel を使います。Prompt Builder はすべての reviewer を常に有効にせず、作業に合う役割だけを選びます。

v0.1 では、optional contract schema field として扱います。役割は host-specific subagent name ではなく portable text として維持します。

推奨役割:

- CTO Reviewer: product/technical decision の一貫性、実装準備度、複雑さの抑制。
- Software Architect: domain boundary、data flow、state transition、system responsibility split、設計入力の不足。
- QA Engineer: edge case、acceptance criteria、testability、本番前検証。
- Security / Privacy Reviewer: auth、permission、personal data、log、masking、secret、abuse risk。
- Legal / Compliance Advisor: terms、notice、liability、operational risk、lawyer-review flags。確定的な法律助言はしない。
- Operations / CS Lead: customer support、incident handling、運用者視点の明確さ、policy explanation の一貫性。
- Product / Information Architecture Reviewer: topic structure、decision、scope、next action、document scanability。
- UX / Product Designer: user flow、copy、accessibility、error prevention、UI decision quality。
- Growth / Marketing Reviewer: target user、positioning、conversion、launch message、pricing/package risk。
- Data / Analytics Reviewer: event design、metric、funnel、experiment readiness。
- Finance / Unit Economics Reviewer: cost、margin、pricing、refund、compensation risk。

推奨 preset:

```text
implementation_review:
CTO Reviewer, Software Architect, QA Engineer, Security / Privacy Reviewer

production_incident:
CTO Reviewer, Software Architect, QA Engineer, Operations / CS Lead, Security / Privacy Reviewer

policy_or_customer_notice:
Legal / Compliance Advisor, Operations / CS Lead, Product / Information Architecture Reviewer, Growth / Marketing Reviewer

new_feature_planning:
CTO Reviewer, Product / Information Architecture Reviewer, UX / Product Designer, Growth / Marketing Reviewer, QA Engineer

docs_or_handoff:
Product / Information Architecture Reviewer, Operations / CS Lead, QA Engineer, CTO Reviewer
```

### レビュー行動パターン

レビューパネル (review panel) を worker prompt にレンダリングするときは、各 reviewer への指示を固定した形で短く、繰り返し使えるように書きます。下の項目は新しい contract field ではなく、prompt 作成のガイドです。対象と許可/禁止する行動は task context、constraints、workspace strategy、infrastructure boundaries から取ります。

```text
役割:
対象:
許可する行動:
禁止する行動:
レビュー観点:
成果物:
fact / inference の区別:
```

worker には reviewer の結果を次の表にまとめさせます。

```text
役割 | 判定 | 主な根拠 | 判定への反映 | 残るリスク
```

`TIMELINE.md` は、同じ review pattern を複数の作業で繰り返したときの任意のローカル成果物 (optional local artifact) としてだけ使います。`.tools/project-prompt-kit/local/` または git から除外されたローカル作業パスに置き、必須の prompt contract field にはしません。

## ローカル成果物

ローカル専用で使う場合、生成した prompt 成果物は vendored kit の下に置きます。

```text
.tools/project-prompt-kit/local/contracts/
.tools/project-prompt-kit/local/rendered/
```

プロジェクトで kit を意図的に vendor として取り込まない場合は、`.tools/` を git から除外してください。

## 役割分離

- Prompt Builder セッション: prompt contract と rendered prompt だけを作成します。
- Worker セッション: rendered prompt を実行します。
- 人間の運用者: リスクの高い操作を承認し、本番専用の read-only query が必要な場合に自分で実行します。

この形にすると、prompt 作成は portable に保ちながら、本番データとプロジェクト secret の safety boundary を守れます。
