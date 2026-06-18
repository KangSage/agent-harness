# Tests

Test infrastructure is intentionally minimal.

Use `../scripts/validate.sh` for package validation. It includes fixture validation.

Use `validate-fixtures.sh` when you only need the contract fixture gate:

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```

## Fixtures

- `fixtures/valid/` contains valid prompt contracts for every supported mode, all supported targets, and at least one prompt request fixture.
- `fixtures/invalid/` contains isolated failure cases for required fields, enums, const values, type checks, string and array minimums, extra properties, unsafe safety defaults, nested safety shape, unsupported schema keywords, and governance policy failures.
- Governance policy fixtures cover synthetic-data markers, unsafe public markers, high-risk reviewer coverage, accepted-risk human markers, auth-migration rollback/stop boundaries, and `not_applicable` rationale markers.
- `golden/` contains static output shape examples for every supported mode.

Golden files are examples, not renderer snapshots. The package still does not include a CLI or renderer engine.
