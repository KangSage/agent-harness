# Tests

v0.1.x의 test infrastructure는 의도적으로 최소화되어 있습니다.

package validation에는 `../scripts/validate.sh`를 사용합니다. 이 명령에는 fixture validation도 포함됩니다.

contract fixture gate만 필요할 때는 `validate-fixtures.sh`를 사용합니다.

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```

## Fixture

- `fixtures/valid/`는 지원 mode 전체, 지원 target 전체, 최소 하나의 prompt request fixture를 포함한 valid prompt contract를 담습니다.
- `fixtures/invalid/`는 required field, enum, const value, type check, string/array minimum, extra property, unsafe safety default, nested safety shape, unsupported schema keyword에 대한 독립 실패 사례를 담습니다.
- `golden/`은 지원 mode 전체에 대한 static output shape 예제를 담습니다.

golden file은 예제이며 renderer snapshot이 아닙니다. 이 package는 아직 CLI나 renderer engine을 포함하지 않습니다.
