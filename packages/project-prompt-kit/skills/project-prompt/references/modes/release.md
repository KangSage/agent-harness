# release

Korean: `릴리즈`

Purpose: evaluate readiness before publishing, merging, deploying, or claiming release status.

Primary output: evidence gate prompt.

Required prompt fields:
- release scope
- changes
- tests run
- known gaps
- deployment or publish target
- approval requirements
- rollout and rollback
- evidence log

Guardrail: distinguish tested from not tested and do not claim readiness without evidence.
