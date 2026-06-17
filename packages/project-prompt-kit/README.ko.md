# project-prompt-kit

코딩 에이전트를 위한 저장소 맥락 인식 프롬프트 템플릿입니다.

언어: [English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`project-prompt-kit`은 코딩 에이전트와 프로젝트 에이전트의 작업 흐름(workflow)을 위한 가벼운 실행 환경에 종속되지 않는 프롬프트 묶음 기본 뼈대(host-neutral prompt kit scaffold)입니다. 느슨한 의도를 목표(`objective`), 맥락(context), 범위(scope), 제약(`constraints`), 증거 요구사항(`evidence_required`), 출력 형식(`output_format`), 중단 조건(`stop_condition`)을 갖춘 구조화된 프롬프트 명세(prompt contract)로 바꿉니다.

## 명령 계약

- 기본 명령: `/prompt`
- 정식 별칭: `/project-prompt`

지원하는 모드(mode):

- `choose`
- `task`
- `plan`
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

- 명령 명세(command spec)
- 스킬 기본 뼈대(skill scaffold)
- 모드 명세(mode spec)
- 프롬프트 명세(prompt contract), 프롬프트 요청(prompt request), 모드 메타데이터 스키마(mode metadata schema)
- 렌더러 템플릿(renderer template)
- 안전 기본값(safety defaults)
- 예제, 고정 입력 예제(fixture)로 검증한 기준 출력 형태(golden output shape), 검증 스크립트(validation script)

의도적으로 완전한 CLI(full CLI)는 아직 제공하지 않습니다. `handoff`는 지원 모드(mode) 중 하나일 뿐이며, 기본값이나 유일한 사용 사례가 아닙니다.

## 빠른 시작

이 키트는 저장소에 포함해 배포하는 프롬프트 기본 뼈대(repo-distributed prompt scaffold)로 사용합니다.

1. `docs/quickstart.ko.md`를 읽습니다.
2. `skills/project-prompt/references/modes/`에서 모드(mode)를 고릅니다.
3. `skills/project-prompt/references/templates/`에서 대상 렌더러(target renderer)를 고릅니다.
4. `examples/sample-contract.*.json`에서 시작합니다.
5. 실제 프로젝트에 적용하기 전에 `examples/rendered/`와 비교합니다.
6. 프롬프트(prompt) 작성만 담당하는 전용 세션이 필요하면 `docs/prompt-builder-session.ko.md`를 사용합니다.
7. 변경사항을 공유하기 전에 검증(validation)을 실행합니다.

이 패키지는 저장소를 복제(clone)하거나 프로젝트 안에 가져와서(vendor) 바로 사용할 수 있습니다. 아직 설치형 CLI나 패키지 저장소에 등록된 패키지(registry package)는 아닙니다.

## 안전 기본값

- 기본 사용 통계 전송(telemetry) 없음
- 기본 네트워크 호출(network call) 없음
- 로컬 우선(local-first) 사용 가이드
- 민감정보를 먼저 가리고 처리(redaction-first handling)
- `.promptkitignore` 지원
- 호스트 프롬프트(host prompt)와 신뢰할 수 없는 프로젝트 입력(project input) 사이의 프롬프트 삽입 경계(prompt injection boundary) 문서화
- 공유 전 미리 확인(preview)
- 공개 예제에서는 상대 경로(relative path) 사용

생성된 프롬프트(prompt)에는 프로젝트 맥락이 들어갈 수 있습니다. 외부에 공유하기 전에 반드시 검토하세요.

## 구조

- `commands/` — 슬래시 명령(slash command) 문서
- `skills/project-prompt/` — skill 정의
- `schemas/` — 실행 환경에 종속되지 않는 프롬프트 명세(host-neutral contract)
- `examples/` — 예제 프롬프트 입력값(prompt payload)
- `examples/rendered/` — 대상별로 렌더링된 프롬프트 예제(target-specific rendered prompt)
- `examples/sample-outputs/` — 기준 샘플 출력 형태(golden sample output shape)
- `docs/prompt-builder-session.ko.md` — 프롬프트 작성 전용 세션 패턴
- `scripts/validate.sh` — 구조/명세 검증(validation)
- `tests/fixtures/` — 유효/무효 명세 고정 입력 예제(valid/invalid contract fixture)
- `tests/golden/` — 정적 모드 출력 형태 예제(static mode output shape)
- `tests/validate-fixtures.sh` — 고정 입력 예제 검증 시작점(fixture validation entry point)

## 검증

```bash
bash packages/project-prompt-kit/scripts/validate.sh
```

고정 입력 예제(fixture)만 검증할 때:

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```
