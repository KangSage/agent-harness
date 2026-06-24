# Prompt Builder Sessions

Use a Prompt Builder session when you want one agent session to produce project prompts and a separate agent session to do the actual work.

This pattern is useful for existing projects, risky operations, production investigations, and long-running handoffs. The Prompt Builder session turns loose intent into a contract JSON and rendered prompt. It must not edit code, connect to production systems, or perform the work itself.

## Session Bootstrap

Start a new agent session inside the target project and paste this prompt:

```text
You are the Prompt Builder for this project.

Use .tools/project-prompt-kit to write project prompts only.
Do not edit code, commit changes, connect to databases, run production operations, or perform the requested work.

Given the goal, scope, background, and constraints I provide:
1. choose or confirm the mode and target renderer
2. write the contract JSON
3. write the rendered prompt markdown
4. include any workspace strategy I provide in the rendered prompt
5. include any infrastructure boundaries I provide in the rendered prompt
6. include any communication policy I provide in the rendered prompt
7. choose a review panel when role-specific review would improve the worker prompt
8. ask one concise question only when required information is missing

Project rules:
- follow AGENTS.md and any nested AGENTS.md files
- respect .promptkitignore
- do not output secrets, environment values, credential-bearing URLs, or local absolute paths
- do not connect to production systems
```

## User Request Shape

After the bootstrap prompt, send requests in this shape:

```text
mode: debug

target renderer:
codex, claude, or generic

workspace strategy:
The current checkout may be shared with other sessions and may contain unrelated local changes.
The worker must treat the current checkout as read-only.
Before editing, the worker should fetch the remote and create a fresh worktree from the requested remote base ref.
Use a task-specific branch such as codex/<task-slug>.
Example: git worktree add ../<repo>-<task-slug> -b codex/<task-slug> origin/<base-branch>
The worker must edit, test, commit, and push only inside the new worktree.
The worker must not reset, clean, checkout, or revert files in the current checkout.

infrastructure boundaries:
The worker must not connect to production databases, production APIs, cloud consoles, secret stores, or admin dashboards.
When production data is required, the worker must write read-only SQL step by step.
I will run each SQL query in production and return the result.
Allowed SQL: read-only SELECT/WITH queries.
Forbidden SQL: UPDATE, DELETE, INSERT, ALTER, DROP, LOCK, or transaction control statements.
The worker must not request, reveal, or infer secrets, credentials, tokens, or environment values.
The worker should treat returned production results as sensitive and quote only the minimum evidence needed.

communication policy:
The worker should ask questions, report progress, and summarize results in the user's language.
Agent-to-agent handoffs, internal coordination notes, and compact technical briefs should use simple English.
Agent-to-agent English should be terse, direct, and low-filler.
Do not translate code, commands, SQL, logs, errors, identifiers, or file paths.
Explain SQL purpose and interpretation in the user's language, but keep SQL text exact.
When production query results are needed, ask one user-facing question at a time in the user's language.

review panel:
Choose only the roles needed for this task.
For implementation work, include CTO Reviewer, Software Architect, QA Engineer, and Security / Privacy Reviewer.
For production incidents, include CTO Reviewer, Software Architect, QA Engineer, Operations / CS Lead, and Security / Privacy Reviewer.
For policy or customer notices, include Legal / Compliance Risk Screener, Operations / CS Lead, Product / Information Architecture Reviewer, and Growth / Marketing Reviewer.
For new feature planning, include CTO Reviewer, Product / Information Architecture Reviewer, UX / Product Designer, Growth / Marketing Reviewer, and QA Engineer.
For docs or handoff, include Product / Information Architecture Reviewer, Operations / CS Lead, QA Engineer, and CTO Reviewer.
Use Legal / Compliance Risk Screener only to identify legal/compliance risks and lawyer-review triggers, not to provide legal advice or compliance approval.

goal:
Investigate production point-transfer transaction consistency.

workflow:
The worker should interpret the result and propose the next read-only SQL.

scope:
Point domain only.

constraints:
- follow AGENTS.md
- respect .promptkitignore
- do not output secrets, env values, or local absolute paths
- analyze root cause only; do not perform remediation

output:
contract JSON and rendered prompt markdown.
```

## Workspace Strategy

Use a workspace strategy when the current checkout is shared, dirty, or already used by other agent sessions. The Prompt Builder should carry this policy into the rendered worker prompt so the worker knows where it may write.

For v0.1, this is an optional contract schema field. Do not make it required for every prompt because many read-only or documentation prompts do not need worktree isolation.

Recommended worker policy:

```text
The current checkout is read-only context.
Run git fetch origin before creating the worktree.
Create a task-specific worktree from the requested remote base ref.
Use a task-specific branch with the requested branch prefix.
Read AGENTS.md again inside the new worktree before editing.
Only edit, test, commit, and push inside the new worktree.
Do not reset, clean, checkout, or revert unrelated files in any existing checkout.
```

## Infrastructure Boundaries

Use infrastructure boundaries when the task touches databases, production APIs, cloud consoles, secret stores, admin dashboards, or other external systems. The Prompt Builder should make access rules explicit in the rendered worker prompt instead of burying them in a generic constraints list.

For v0.1, this is an optional contract schema field. Do not make it required for every prompt because many local-only prompts do not touch external infrastructure.

Recommended worker policy:

```text
The worker must not connect directly to production infrastructure.
The worker may ask the human operator to run approved read-only commands or queries.
All production SQL must be read-only SELECT/WITH unless the prompt explicitly allows more.
The worker must state the purpose of each query before presenting it.
The worker must wait for human-returned results before proposing the next production query.
The worker must not request, expose, or infer secrets, tokens, credentials, or environment values.
Returned production data is sensitive; quote only the minimum evidence needed.
```

## Communication Policy

Use a communication policy when the rendered prompt may be written in one language but the worker should speak to the user in another. The Prompt Builder should make user-facing language separate from agent-to-agent coordination language.

For v0.1, this is an optional contract schema field. Do not make it required for every prompt because some prompts already have a single obvious communication language.

Recommended worker policy:

```text
User-facing questions, progress updates, and final summaries must use the user's language.
Agent-to-agent handoffs and compact technical coordination notes should use simple English.
Agent-to-agent English should be terse, direct, and low-filler.
Do not translate code, commands, SQL, logs, errors, identifiers, or file paths.
Explain SQL purpose and interpretation in the user's language, but keep SQL text exact.
When production results are needed, ask one user-facing question at a time.
```

## Governance Selection

Use governance selection when a worker prompt needs planning review, risk gates, or scenario-specific checklists before work starts.

For v0.2, this is optional contract guidance. Keep it lightweight: choose the smallest governance layer that makes unresolved risk visible.

Detailed expansion rules live in `governance-presets.md`; this session guide only helps choose the governance layer.

### Governance Selection Questions

Ask these questions in order when the user did not already provide clear governance choices. The Prompt Builder may recommend a preset and scenario template, but it must not auto-decide when required evidence is missing.

1. Does the task affect auth, permissions, privacy, payment, settlement, production data, customer impact, rollout, rollback, or support operations?
2. Does the task involve a production incident, data inconsistency, customer-facing explanation, or follow-up after production impact?
3. Does the task involve retention, deletion, consent, notice, policy, regulated data handling, or lawyer-review triggers?
4. Is rollback, fallback, support path, customer communications ownership, or runbook readiness unclear?
5. Is the task low-risk and local-only, with no external infrastructure, customer impact, or human approval boundary?

If any high-risk trigger is clear, do not downgrade the preset to `standard` or `light`. If the answer is unclear, ask one concise user-facing question instead of guessing. This flow is a prompt-authoring guide, not an automatic risk classifier.

Use `governance.preset` for review strength.

- `light`: low-risk work that needs a quick scope, acceptance, and validation check.
- `standard`: normal implementation planning that needs product, architecture, and QA review.
- `high_risk`: work that may affect auth, permissions, privacy, production data, payment, customer impact, legal/compliance review triggers, support operations, rollout, or rollback.

Use `governance.scenario_template` for scenario checklist.

- `auth_migration`: sessions, tokens, permissions, account recovery, audit logs, or authentication data flow may change.
- `production_incident`: the work investigates, mitigates, explains, or follows up on an incident or production data inconsistency.
- `regulated_data_or_domain`: retention, deletion, consent, notice, policy, regulated data handling, or lawyer-review triggers may be involved.

Omit `governance` when no governance layer is needed.
Do not add a `none` preset.
Do not create `governance.review_panel_preset`.

When governance is selected, expand reviewer guidance through the existing `review_panel` structure. The legal/compliance role identifies risk triggers for qualified humans; it does not provide legal advice or compliance approval.

### Over-trigger / Under-trigger Examples

| Situation | Recommended choice | Why |
| --- | --- | --- |
| Typo-only docs edit with no policy, release, or customer-impact change | Omit `governance` or use `light` only if a quick acceptance check helps | High-risk review would add process without exposing new risk |
| Normal feature planning with product, architecture, and QA uncertainty but no sensitive data or production boundary | `standard` | The plan needs review, but no high-risk trigger is present |
| Auth module replacement, permission change, production data investigation, payment/settlement path, or customer-impacting incident | `high_risk`, plus the matching scenario template when applicable | A clear high-risk trigger must not be downgraded |
| Production data inconsistency investigation where the worker must write SQL for a human to run | `high_risk` + `production_incident` | Production evidence and support impact need gates even when the worker has no direct DB access |
| Policy, notice, retention, deletion, consent, or regulated-data planning | `high_risk` + `regulated_data_or_domain` | Legal/compliance review triggers must be surfaced without providing legal advice |

Example:

```json
{
  "mode": "plan",
  "governance": {
    "preset": "high_risk",
    "scenario_template": "auth_migration"
  }
}
```

## Review Panel

Use a review panel when the worker prompt should ask role-specific reviewers to inspect the task before implementation, release, policy publication, or customer-facing communication. The Prompt Builder should choose only the roles that fit the task instead of always enabling every reviewer.

For v0.1, this is an optional contract schema field. Keep roles as portable text, not host-specific subagent names.

Suggested roles:

- CTO Reviewer: product and technical decision consistency, implementation readiness, complexity control.
- Software Architect: domain boundaries, data flow, state transitions, system responsibility splits, missing design inputs.
- QA Engineer: edge cases, acceptance criteria, testability, pre-production verification.
- Security / Privacy Reviewer: auth, permission, personal data, logs, masking, secrets, abuse risk.
- Legal / Compliance Risk Screener: terms, notices, liability, operational risk, legal/compliance risks, and lawyer-review triggers only; no legal advice or compliance approval.
- Operations / CS Lead: customer support, incident handling, operator-facing clarity, policy explanation consistency.
- Product / Information Architecture Reviewer: topic structure, decisions, scope, next actions, document scanability.
- UX / Product Designer: user flow, copy, accessibility, error prevention, UI decision quality.
- Growth / Marketing Reviewer: target user, positioning, conversion, launch message, pricing/package risk.
- Data / Analytics Reviewer: event design, metrics, funnels, experiment readiness.
- Finance / Unit Economics Reviewer: cost, margin, pricing, refund, compensation risk.

Recommended presets:

```text
implementation_review:
CTO Reviewer, Software Architect, QA Engineer, Security / Privacy Reviewer

production_incident:
CTO Reviewer, Software Architect, QA Engineer, Operations / CS Lead, Security / Privacy Reviewer

policy_or_customer_notice:
Legal / Compliance Risk Screener, Operations / CS Lead, Product / Information Architecture Reviewer, Growth / Marketing Reviewer

new_feature_planning:
CTO Reviewer, Product / Information Architecture Reviewer, UX / Product Designer, Growth / Marketing Reviewer, QA Engineer

docs_or_handoff:
Product / Information Architecture Reviewer, Operations / CS Lead, QA Engineer, CTO Reviewer
```

### Review Behavior Pattern

When a review panel is rendered into a worker prompt, keep each reviewer instruction fixed and repeatable. These labels are prompt-writing guidance, not extra contract fields; derive target and action boundaries from the task context, constraints, workspace strategy, and infrastructure boundaries.

```text
Role:
Target:
Allowed actions:
Forbidden actions:
Review perspective:
Expected output:
Fact / inference boundary:
```

Ask the worker to combine reviewer results with this table:

```text
Role | Verdict | Key evidence | Decision impact | Residual risk
```

Use `TIMELINE.md` only as an optional local artifact when the same review pattern is repeated across tasks. Keep it under `.tools/project-prompt-kit/local/` or another ignored local workspace path. Do not make it a required prompt contract field.

## Local Artifacts

For local-only usage, keep generated prompt artifacts under the vendored kit:

```text
.tools/project-prompt-kit/local/contracts/
.tools/project-prompt-kit/local/rendered/
```

Keep `.tools/` ignored by git unless your project intentionally vendors the kit.

## Separation Of Duties

- Prompt Builder session: author prompt contracts and rendered prompts only.
- Worker session: execute the rendered prompt.
- Human operator: approve risky actions and run production-only read-only queries when required.

This keeps prompt authoring portable while preserving safety boundaries for production data and project secrets.
