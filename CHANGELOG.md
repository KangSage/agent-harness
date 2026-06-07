# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
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
