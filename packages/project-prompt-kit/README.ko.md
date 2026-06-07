# project-prompt-kit

코딩 에이전트를 위한 저장소 인지형 프롬프트 템플릿입니다.

언어: [English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`project-prompt-kit`은 코딩 에이전트와 프로젝트 에이전트 워크플로우를 위한 가벼운 호스트 중립 프롬프트 키트 스캐폴드입니다. 느슨한 의도를 objective, context, scope, constraints, evidence requirements, output format, stop condition을 갖춘 구조화된 prompt contract로 바꿉니다.

## 명령 계약

- 기본 명령: `/prompt`
- 표준 별칭: `/project-prompt`

v0.1에서 지원하는 mode:

- `choose`
- `task`
- `implement`
- `review`
- `debug`
- `research`
- `docs`
- `release`
- `correction`
- `handoff`

## 범위

현재 이 패키지가 제공하는 것:

- command spec
- skill scaffold
- mode spec
- prompt contract, prompt request, mode metadata schema
- renderer template
- safety default
- example, fixture-backed golden output shape, validation script

v0.1에서는 의도적으로 full CLI를 제공하지 않습니다. `handoff`는 지원 mode 중 하나일 뿐이며, 기본값이나 유일한 사용 사례가 아닙니다.

## 빠른 시작

이 키트는 repo-distributed prompt scaffold로 사용합니다.

1. `docs/quickstart.ko.md`를 읽습니다.
2. `skills/project-prompt/references/modes/`에서 mode를 고릅니다.
3. `skills/project-prompt/references/templates/`에서 target renderer를 고릅니다.
4. `examples/sample-contract.*.json`에서 시작합니다.
5. 실제 프로젝트에 적용하기 전에 `examples/rendered/`와 비교합니다.
6. 변경사항을 공유하기 전에 validation을 실행합니다.

이 패키지는 저장소를 clone하거나 vendor해서 바로 사용할 수 있습니다. 아직 설치형 CLI나 registry package는 아닙니다.

## 안전 기본값

- 기본 telemetry 없음
- 기본 network call 없음
- local-first 사용 가이드
- 민감정보는 redaction-first로 처리
- `.promptkitignore` 지원
- host prompt와 신뢰할 수 없는 project input 사이의 prompt injection boundary 문서화
- 공유 전 preview
- 공개 예제에서는 relative path 사용

생성된 prompt에는 프로젝트 맥락이 들어갈 수 있습니다. 외부에 공유하기 전에 반드시 검토하세요.

## 구조

- `commands/` — slash command 문서
- `skills/project-prompt/` — skill 정의
- `schemas/` — host-neutral contract
- `examples/` — 예제 prompt payload
- `examples/rendered/` — target-specific rendered prompt 예제
- `examples/sample-outputs/` — golden sample output shape
- `scripts/validate.sh` — 구조/계약 validation
- `tests/fixtures/` — valid/invalid contract fixture
- `tests/golden/` — static mode output shape 예제
- `tests/validate-fixtures.sh` — fixture validation entry point

## 검증

```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

fixture만 검증할 때:

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```
