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
For policy or customer notices, include Legal / Compliance Advisor, Operations / CS Lead, Product / Information Architecture Reviewer, and Growth / Marketing Reviewer.
For new feature planning, include CTO Reviewer, Product / Information Architecture Reviewer, UX / Product Designer, Growth / Marketing Reviewer, and QA Engineer.
For docs or handoff, include Product / Information Architecture Reviewer, Operations / CS Lead, QA Engineer, and CTO Reviewer.
Use Legal / Compliance Advisor only for risk identification and lawyer-review flags, not final legal advice.

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

## Review Panel

Use a review panel when the worker prompt should ask role-specific reviewers to inspect the task before implementation, release, policy publication, or customer-facing communication. The Prompt Builder should choose only the roles that fit the task instead of always enabling every reviewer.

For v0.1, this is an optional contract schema field. Keep roles as portable text, not host-specific subagent names.

Suggested roles:

- CTO Reviewer: product and technical decision consistency, implementation readiness, complexity control.
- Software Architect: domain boundaries, data flow, state transitions, system responsibility splits, missing design inputs.
- QA Engineer: edge cases, acceptance criteria, testability, pre-production verification.
- Security / Privacy Reviewer: auth, permission, personal data, logs, masking, secrets, abuse risk.
- Legal / Compliance Advisor: terms, notices, liability, operational risk, lawyer-review flags only.
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
Legal / Compliance Advisor, Operations / CS Lead, Product / Information Architecture Reviewer, Growth / Marketing Reviewer

new_feature_planning:
CTO Reviewer, Product / Information Architecture Reviewer, UX / Product Designer, Growth / Marketing Reviewer, QA Engineer

docs_or_handoff:
Product / Information Architecture Reviewer, Operations / CS Lead, QA Engineer, CTO Reviewer
```

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
