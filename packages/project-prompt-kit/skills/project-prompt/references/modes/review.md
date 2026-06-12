# review

Korean: `리뷰`

Purpose: perform code review, CTO review, architecture review, or quality/risk review.

Primary output: findings and verdict.

Required prompt fields:
- artifact under review
- source of truth
- review range
- quality bar
- known concerns
- decision needed
- findings format
- verdict format

Guardrail: findings first, separate facts from opinions, and do not edit files unless explicitly requested.

When `review_panel` is rendered into a worker prompt, keep each reviewer instruction fixed and repeatable. These labels are prompt-writing guidance, not extra contract fields:

```text
Role:
Target:
Allowed actions:
Forbidden actions:
Review perspective:
Expected output:
Fact / inference boundary:
```

Combine reviewer results with this table:

```text
Role | Verdict | Key evidence | Decision impact | Residual risk
```

`TIMELINE.md` is optional local evidence for repeated use of the same review pattern. It is not a required prompt contract field.
