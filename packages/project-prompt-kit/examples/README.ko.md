# 예제

이 디렉터리는 `project-prompt-kit`의 공개해도 안전한 예제(public-safe examples)를 담고 있습니다.

## 명세 예제(Contract)

`sample-contract.*.json` 파일은 `schemas/prompt-contract.schema.json`으로 검증되는 정규화된 프롬프트 입력값(normalized prompt payload)입니다.

- `sample-contract.codex.json`
- `sample-contract.claude.json`
- `sample-contract.generic.json`

새 프롬프트 명세(prompt contract)를 작성할 때 이 파일들을 시작점으로 사용합니다.

## 렌더링된 예제(Rendered)

`rendered/`에는 샘플 명세(sample contract)를 대상 렌더러 템플릿(target renderer template)에 적용한 최종 프롬프트(prompt) 예제가 있습니다.

- `rendered/codex-review.md`
- `rendered/claude-implement.md`
- `rendered/generic-task.md`

렌더링된 예제(rendered example)는 문서용 고정 예제(documentation fixture)이며 생성된 스냅샷(generated snapshot)이 아닙니다. 수동 사용 시 기대되는 프롬프트 형태(prompt shape)를 보여줍니다.

## 출력 예시(Sample Outputs)

`sample-outputs/`에는 모드 단위 출력 형태(mode-level output shape) 예제가 있습니다. 렌더링된 프롬프트(rendered prompt)를 사용한 뒤 에이전트 응답(agent response)이 어떤 형태가 될 수 있는지 설명합니다.

## 안전 규칙

예제는 이식 가능해야 합니다(portable).

- 상대 경로(relative path)만 사용합니다.
- 정리된 프로젝트 이름(sanitized project name)을 사용합니다.
- 비공개 사용자 이름(private username), 로컬 절대 경로(local absolute path), 비밀 정보(secret), 토큰(token), 인증 정보가 들어 있는 URL(credential-bearing URL)을 포함하지 않습니다.
- 프롬프트 삽입 경계(prompt-injection boundary)를 보이게 유지합니다.
