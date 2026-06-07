# Authoring Modes

mode spec은 생성된 prompt가 에이전트에게 무엇을 요청해야 하는지 설명합니다.

각 mode reference는 아래 항목을 포함합니다.

- purpose
- primary output
- required prompt fields
- guardrail

`handoff`는 여러 mode 중 하나입니다. project prompt의 기본 mode로 취급하지 마세요.

v0.1은 계획된 모든 mode를 문서화하고, golden example은 `choose`, `implement`, `review`, `debug`, `docs`, `handoff`에 집중합니다.
