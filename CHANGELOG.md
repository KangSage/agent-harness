# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Documented the Korean v0.2 planning governance design note for high-risk prompt planning workflows
- Added the `plan` mode skeleton for pre-implementation planning prompts

## [0.1.9] - 2026-06-17
### Changed
- Improved Korean and Japanese README terminology readability by explaining technical terms before showing the original English

## [0.1.8] - 2026-06-13
### Added
- Review panel behavior guidance for fixed reviewer instructions, integration result tables, and optional local `TIMELINE.md` evidence

## [0.1.7] - 2026-06-10
### Added
- Optional `review_panel` prompt contract and request field for task-specific role review perspectives

## [0.1.6] - 2026-06-09
### Added
- Optional `communication_policy` prompt contract and request field for user-language and agent-to-agent style boundaries

## [0.1.5] - 2026-06-09
### Added
- Workspace strategy guidance for Prompt Builder sessions that need isolated worker worktrees from remote base refs
- Infrastructure boundary guidance for Prompt Builder sessions that must separate worker reasoning from production access
- Optional `workspace_strategy` and `infrastructure_boundaries` prompt contract and request fields with fixture validation

## [0.1.4] - 2026-06-09
### Added
- Prompt Builder session guide for using `project-prompt-kit` as a dedicated prompt-authoring surface in existing projects

## [0.1.3] - 2026-06-07
### Added
- Korean and Japanese companion docs for `project-prompt-kit` developer-facing guides
- Validation for package README language navigation

### Changed
- Polished localized `project-prompt-kit` heading style and Japanese wording consistency

## [0.1.2] - 2026-06-07
### Added
- Quickstart documentation for using `project-prompt-kit` without a packaged CLI
- Renderer-specific prompt examples for Codex, Claude, and generic targets

## [0.1.1] - 2026-06-07
### Added
- Schema-backed `project-prompt-kit` fixture validation for the v0.1.1 contract hardening path
- Prompt request and mode metadata schemas alongside the canonical prompt contract schema
- Valid and invalid package fixtures plus full-mode golden output shape examples

### Changed
- Package validation now checks fixture coverage, schema keyword support, mode taxonomy drift, and safety-default failures
- Root validation owns public hygiene scanning across repository docs, scripts, and package files
- Package validation reports malformed schema shapes without repo-root helper imports or duplicate fixture runs

## [0.1.0] - 2026-06-06
### Added
- Initial monorepo scaffold for `agent-harness`
- `project-prompt-kit` package scaffold with commands, skill, schemas, examples, validation, and tests directory
- Multilingual root READMEs (English, Korean, Japanese)
- OSS baseline documents and CI validation workflow
- Universal prompt contract, mode references, renderer templates, safe-default checks, and golden sample output shape
- Root scaffold validation entry point with package-scoped prompt-kit validation
