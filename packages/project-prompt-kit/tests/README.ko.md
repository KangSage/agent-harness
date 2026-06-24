# Tests

테스트 기반 구조(test infrastructure)는 의도적으로 최소화되어 있습니다.

패키지 검증(package validation)에는 `../scripts/validate.sh`를 사용합니다. 이 명령에는 고정 입력 예제 검증(fixture validation)도 포함됩니다.

프롬프트 명세 예제 검증 단계(contract fixture gate)만 필요할 때는 `validate-fixtures.sh`를 사용합니다.

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```

## Fixtures

- `fixtures/valid/`는 지원 모드(mode) 전체, 지원 대상(target) 전체, 최소 하나의 프롬프트 요청 고정 입력 예제(prompt request fixture)를 포함한 유효한 프롬프트 명세(valid prompt contract)를 담습니다.
- `fixtures/invalid/`는 필수 필드(required field), 열거형(enum), const 값(const value), 타입 검사(type check), 문자열/배열 최솟값(string/array minimum), 추가 속성(extra property), 안전하지 않은 안전 기본값(unsafe safety default), 중첩된 안전 구조(nested safety shape), 지원하지 않는 스키마 키워드(unsupported schema keyword), governance policy failure에 대한 독립 실패 사례를 담습니다.
- governance policy fixture는 synthetic data marker, unsafe public marker, high-risk reviewer coverage, decision gate shape, structured accepted-risk payload, accepted-risk 오탐 방지, non-human acceptor rejection, human decision flag, concrete revisit boundary, auth-migration rollback/stop boundary, production-incident scenario marker, regulated-data scenario marker, `not_applicable` rationale marker를 검증합니다.
- `golden/`은 지원 모드(mode) 전체에 대한 정적 출력 형태 예제(static output shape examples)를 담습니다.

기준 파일(golden file)은 예제이며 렌더러 스냅샷(renderer snapshot)이 아닙니다. 이 패키지는 아직 CLI나 렌더링 엔진(renderer engine)을 포함하지 않습니다.
