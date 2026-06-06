# Architecture

`agent-harness` is a package-oriented monorepo.

- Root docs define cross-package principles and governance.
- Each package owns its contracts (`schemas/`), commands (`commands/`), examples (`examples/`), and validation (`scripts/`).
- CI validates structural integrity and command contract expectations.

The first package, `project-prompt-kit`, provides a reusable prompt contract scaffold and safety notes without shipping a full CLI.
