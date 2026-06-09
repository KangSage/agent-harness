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
6. ask one concise question only when required information is missing

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
Before editing, the worker should fetch the remote and create a fresh worktree from origin/develop.
Use a task-specific branch such as codex/<task-slug>.
Example: git worktree add ../<repo>-<task-slug> -b codex/<task-slug> origin/develop
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
