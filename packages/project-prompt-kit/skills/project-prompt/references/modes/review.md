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

Review panel execution policy: do not silently skip selected reviewers. If separate reviewer or subagent contexts are supported and capacity is unavailable, close only completed or no-longer-needed reviewer contexts owned by the current session, then retry. If a selected reviewer still cannot run separately, disclose the skipped role and reason. Label any self-review fallback and state its limits. For high-risk reviews, missing required reviewers must produce `no-go`, `needs human decision`, or explicit residual risk instead of a confident `go` verdict.

`TIMELINE.md` is optional local evidence for repeated use of the same review pattern. It is not a required prompt contract field.
