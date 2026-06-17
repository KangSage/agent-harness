# Governance Preset Expansion

This reference fixes the deterministic expansion rules for the optional `governance` block. It is prompt-writing guidance, not a workflow engine.

## Contract

Use `governance.preset` to choose review strength. Use `governance.scenario_template` to add a scenario checklist.

Omit `governance` when no governance layer is needed. Do not add a `none` preset.

Do not create `governance.review_panel_preset`. Expand reviewer guidance through the existing `review_panel` structure when a rendered prompt needs explicit reviewer instructions.

## Selection Guide

Use `light` when the task is low-risk and only needs a quick plan check for scope, acceptance criteria, and validation evidence.

Use `standard` when the task is a normal implementation plan that needs architecture, product, and QA review before coding starts.

Use `high_risk` when the task may affect auth, permissions, privacy, production data, payment, customer impact, legal/compliance review triggers, support operations, rollout, or rollback.

Use `auth_migration` when sessions, tokens, permissions, account recovery, audit logs, or authentication data flow may change.

Use `production_incident` when the work analyzes, mitigates, explains, or follows up on an incident or production data inconsistency.

Use `regulated_data_or_domain` when retention, deletion, consent, notice, policy, regulated data handling, or lawyer-review triggers may be involved.

## Preset Expansion

| Preset | Reviewer set | Required sections | Stop rules | Output requirement |
| --- | --- | --- | --- | --- |
| `light` | Product / Information Architecture Reviewer; QA Engineer | Goal; scope; assumptions; open issues summary; validation notes; go / no-go verdict | Stop if scope, acceptance criteria, or validation evidence is missing. | Short planning check with open issues and a go / no-go verdict. |
| `standard` | CTO Reviewer; Product / Information Architecture Reviewer; Software Architect; QA Engineer | Goal; non-goals; scope; assumptions; options; decisions; affected domains; open issues burn-down; validation strategy; implementation boundary; rollback or fallback; remaining risks; go / no-go verdict | Stop if architecture boundary, testability, rollback/fallback, or implementation boundary is unclear. | Reviewed implementation plan with explicit decisions, blockers, and remaining risks. |
| `high_risk` | CTO Reviewer; Product / Information Architecture Reviewer; Software Architect; QA Engineer; Security / Privacy Reviewer; Legal / Compliance Risk Screener; Operations / CS Lead | Goal; non-goals; scope; assumptions; options; decisions; affected domains; open issues burn-down; review findings; decision gates section; implementation boundary; rollback or fallback; operations readiness; support path; customer-facing comms owner; human approval points; AI stop conditions; remaining risks; go / no-go verdict | Stop if security/privacy impact, legal/compliance review trigger, customer impact, rollback/fallback, support path, customer-facing comms owner, production access boundary, or human approval point is unresolved. | High-risk planning brief with reviewer findings, decision-gate section labels, operations readiness, and explicit human-review triggers. |

Minimum required high-risk reviewers:

- Security / Privacy Reviewer
- Legal / Compliance Risk Screener
- Operations / CS Lead

Recommended full high-risk panel:

- CTO Reviewer
- Product / Information Architecture Reviewer
- Software Architect
- QA Engineer
- Security / Privacy Reviewer
- Legal / Compliance Risk Screener
- Operations / CS Lead

Validation currently enforces the minimum required high-risk reviewers. Prompt authors should include the recommended full high-risk panel when the task needs product, architecture, or QA decision review in addition to the safety-critical reviewers.

This is not legal advice. This identifies review triggers for qualified humans.

`decision gates section` means the rendered plan must reserve a section for gates and their status. The gate object schema, accepted-risk rules, and executable gate semantics are later governance work.

## Scenario Template Additions

| Scenario template | Added checklist | Added stop rules |
| --- | --- | --- |
| `auth_migration` | secrets inventory and rotation plan; PII/data-flow mapping; permission or role migration matrix; session/token invalidation strategy; account recovery impact; audit log continuity; rollback/fallback boundary; customer impact scope; customer-facing comms owner; support escalation path; customer notice trigger; cutover stop conditions; monitoring/alerting plan; manual intervention points | Stop if session/token invalidation, permission migration, rollback/fallback, audit continuity, customer impact, customer-facing comms owner, or support path is unclear. |
| `production_incident` | incident window; evidence timeline; mitigation options; customer impact scope; comms owner; support path; rollback or containment plan; monitoring/alerting; manual intervention points | Stop if incident scope, evidence timeline, customer communication owner, mitigation boundary, or rollback/containment path is unclear. |
| `regulated_data_or_domain` | data classification; retention/deletion trigger; consent or notice trigger; lawyer-review trigger; customer notice trigger; customer impact scope; customer-facing comms owner; support path; rollback/fallback boundary; data handling boundary; human approval point | Stop if legal/compliance conclusion is required, data handling authority is unclear, customer impact scope, customer-facing comms owner, support path, rollback/fallback, or a qualified human review point is unresolved. |

Scenario templates add checklist and stop-rule requirements to the selected preset. They do not replace the preset reviewer set.

## Deferred

The following are intentionally deferred from this reference:

- accepted-risk handling
- automatic risk classifier
- renderer engine
- standalone CLI
- jurisdiction-specific legal conclusions
- automatic legal/compliance judgment
