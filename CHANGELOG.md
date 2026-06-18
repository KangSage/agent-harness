# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Documented the Korean v0.2 planning governance design note for high-risk prompt planning workflows
- Added the `plan` mode skeleton for pre-implementation planning prompts
- Added the optional `governance` prompt contract/request block for selecting planning review strength and scenario templates
- Added deterministic governance preset and scenario-template expansion reference guidance
- Added validation for the `plan` mode output shape, including open-issue burn-down, decision-gate labels, operations readiness, human approval points, and AI stop conditions
- Added Prompt Builder governance-selection guidance in English, Korean, and Japanese
- Added synthetic governance scenario fixtures for production incident and regulated data/domain planning
- Added invalid fixtures for missing synthetic governance markers and unsafe public marker detection
- Added high-risk governance reviewer coverage validation for Security / Privacy, Legal / Compliance, and Operations / CS roles
- Clarified required versus recommended reviewer coverage for high-risk governance presets
- Added fixture-level validation that `accepted_risk` requires an explicit `human_acceptor` marker
- Added v0.2 release-readiness validation for auth-migration rollback/stop boundaries and `not_applicable` rationale markers
- Added synthetic DB credential URL fixture coverage for unsafe governance examples
- Added exact expected-error assertions for every invalid fixture
- Added decoded-JSON public hygiene scanning for escaped secret-like fixture content
- Added positive valid-fixture coverage for every governance preset
- Added a default-validation cost guard that keeps scaffold validation on an explicit local/offline step allowlist

### Changed
- Aligned Prompt Builder review-panel docs with the `Legal / Compliance Risk Screener` role label
- Hardened governance fixture hygiene and plan golden validation to reduce brittle false positives

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
