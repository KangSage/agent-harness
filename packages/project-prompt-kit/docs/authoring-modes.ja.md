# Mode 作成

mode spec は、生成された prompt がエージェントに何を依頼するべきかを説明します。

各 mode reference は次を含みます。

- purpose
- primary output
- required prompt fields
- guardrail

`handoff` は複数ある mode の一つです。project prompt の default mode として扱わないでください。

現在のひな形（scaffold）は、対応するすべての mode を文書化し、golden example を mode taxonomy 全体とそろえて維持します。
