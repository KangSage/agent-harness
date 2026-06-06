# Portability

Project Prompt Kit must remain independent from any private workspace, local-only framework, or single agent host.

Portable artifacts:
- mode specs
- universal prompt contract
- renderer templates
- sample outputs
- validation rules

Host-specific adapters may exist, but they must not change the core contract.

Public examples must use relative paths and sanitized project names. Do not include private usernames, local absolute paths, access tokens, or framework-specific runtime state.
