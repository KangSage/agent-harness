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

Decision gates may be represented as structured planning metadata in `decision_gates[]`. Do not treat gate status as implementation approval, deployment approval, production-operation approval, legal/compliance approval, automatic risk acceptance, or executable workflow semantics. `accepted_risk` requires a structured payload with qualified human acceptance evidence and an expiry or revisit boundary.
