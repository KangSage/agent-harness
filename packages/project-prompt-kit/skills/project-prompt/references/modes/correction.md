# correction

Korean: `정정`

Purpose: replace a stale, wrong, or incomplete prior prompt or instruction.

Primary output: correction prompt.

Required prompt fields:
- bad output or stale basis
- new source of truth
- whether prior instruction is discarded or partially retained
- expected correction
- minimal-change rule
- regression checks

Guardrail: preserve correct parts and do not rewrite everything unless requested.
