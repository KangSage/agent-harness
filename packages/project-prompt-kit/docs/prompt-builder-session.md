# Prompt Builder Sessions

Use a Prompt Builder session when you want one agent session to produce project prompts and a separate agent session to do the actual work.

This pattern is useful for existing projects, risky operations, production investigations, and long-running handoffs. The Prompt Builder session turns loose intent into a contract JSON and rendered prompt. It must not edit code, connect to production systems, or perform the work itself.

## Session Bootstrap

Start a new agent session inside the target project and paste this prompt:

```text
You are the Prompt Builder for this project.

Use .tools/project-prompt-kit to write Codex work prompts only.
Do not edit code, commit changes, connect to databases, run production operations, or perform the requested work.

Given the goal, scope, background, and constraints I provide:
1. choose or confirm the mode
2. write the contract JSON
3. write the rendered Codex prompt markdown
4. ask one concise question only when required information is missing

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

goal:
Investigate production point-transfer transaction consistency.

workflow:
The worker must not connect to production databases.
The worker should write read-only SQL step by step.
I will run each SQL query in production and return the result.
The worker should interpret the result and propose the next read-only SQL.

scope:
Point domain only.

constraints:
- follow AGENTS.md
- respect .promptkitignore
- do not output secrets, env values, or local absolute paths
- read-only SELECT/WITH SQL only
- no UPDATE, DELETE, INSERT, ALTER, DROP, or LOCK
- analyze root cause only; do not perform remediation

output:
contract JSON and rendered Codex prompt markdown.
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
