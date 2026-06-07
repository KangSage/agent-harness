# Tests

v0.1.x の test infrastructure は意図的に最小限です。

package validation には `../scripts/validate.sh` を使います。このコマンドには fixture validation も含まれます。

contract fixture gate だけが必要な場合は `validate-fixtures.sh` を使います。

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```

## Fixture

- `fixtures/valid/` は、対応 mode 全体、対応 target 全体、少なくとも一つの prompt request fixture を含む valid prompt contract を持ちます。
- `fixtures/invalid/` は、required field, enum, const value, type check, string/array minimum, extra property, unsafe safety default, nested safety shape, unsupported schema keyword の独立した失敗ケースを持ちます。
- `golden/` は、対応 mode 全体に対する static output shape の例を持ちます。

golden file は例であり、renderer snapshot ではありません。この package はまだ CLI や renderer engine を含みません。
