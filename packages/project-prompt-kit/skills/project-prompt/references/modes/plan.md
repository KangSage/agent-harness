# plan

Korean: `계획`

Purpose: turn scoped intent and source material into a reviewed implementation plan before work begins.

Primary output: planning brief.

Required prompt fields:
- goal
- non-goals
- scope
- assumptions
- options
- decisions
- affected domains
- validation strategy
- open issues burn-down
- review findings
- decision gates
- implementation boundary
- rollback or fallback
- operations readiness
- human approval points
- AI stop conditions
- remaining risks
- go/no-go verdict

Guardrail: do not implement, edit files, or claim readiness while planning blockers remain unresolved. If human approval is required, leave the plan blocked instead of converting it into implementation instructions.

Decision gates are section labels only in this scaffold. Do not invent gate object schemas, accepted-risk rules, or executable gate semantics.
