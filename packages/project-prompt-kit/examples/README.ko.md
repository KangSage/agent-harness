# 예제

이 디렉터리는 `project-prompt-kit`의 public-safe 예제를 담고 있습니다.

## Contract 예제

`sample-contract.*.json` 파일은 `schemas/prompt-contract.schema.json`으로 검증되는 normalized prompt payload입니다.

- `sample-contract.codex.json`
- `sample-contract.claude.json`
- `sample-contract.generic.json`

새 prompt contract를 작성할 때 이 파일들을 시작점으로 사용합니다.

## Rendered 예제

`rendered/`에는 sample contract를 target renderer template에 적용한 최종 prompt 예제가 있습니다.

- `rendered/codex-review.md`
- `rendered/claude-implement.md`
- `rendered/generic-task.md`

rendered example은 documentation fixture이며 generated snapshot이 아닙니다. 수동 사용 시 기대되는 prompt shape를 보여줍니다.

## Sample Outputs

`sample-outputs/`에는 mode-level output shape 예제가 있습니다. rendered prompt를 사용한 뒤 agent response가 어떤 형태가 될 수 있는지 설명합니다.

## 안전 규칙

예제는 portable해야 합니다.

- relative path만 사용합니다.
- sanitized project name을 사용합니다.
- private username, local absolute path, secret, token, credential-bearing URL을 포함하지 않습니다.
- prompt-injection boundary를 보이게 유지합니다.
