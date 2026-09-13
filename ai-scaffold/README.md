# Your AI project starting point

This folder is a reusable set of guidance and templates, not a runnable application.
Read `AGENTS.md`, then fill in `docs/PROJECT.md`, `docs/TECHNOLOGY.md`, and
`docs/ARCHITECTURE.md` with verified project decisions.

## Adopt the scaffold

1. Review the files before copying or merging them into an existing project.
2. Merge `AGENTS.md` into the project root so your AI tool can discover it.
3. Copy or merge `docs/`, `prompts/`, `.github/`, and `.gitignore` as appropriate.
4. Replace explicit TBD entries with real decisions; never invent infrastructure.
5. Record actual setup, lint, test, and build commands in `docs/DEVELOPMENT.md`.

## Structure

- `docs/`: requirements, architecture, technology, development, and decisions.
- `prompts/`: reusable planning, implementation, and review instructions.
- `src/`: application source once the technology is selected.
- `tests/`: behavior tests and fixtures containing synthetic data.
- `contrib/`: maintenance and management scripts.
- `.github/`: collaboration and security notes plus a PR template.

Empty runtime directories intentionally contain short READMEs rather than example
code that implies a technology choice. The source repository's CI validates this
scaffold; each consuming project must add its own runnable application checks.
