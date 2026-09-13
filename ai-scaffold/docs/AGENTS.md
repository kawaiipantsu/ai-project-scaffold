# AI Agent Instructions

This file defines the basic operating instructions for AI agents working on this repository.

It applies to AI coding agents, autonomous development tools, and other automated contributors.

## Start Here

Before making changes to the project, read the relevant documentation in `docs/`.

At minimum, review:

* `PROJECT.md` — Project purpose, goals, and scope.
* `PROJECT_RULES.md` — General project rules and constraints.
* `PROJECT_PROCESS.md` — Expected development and implementation process.
* `ARCHITECTURE.md` — Project architecture and structural decisions.
* `TECHNOLOGY.md` — Approved technologies, frameworks, libraries, and tooling.
* `GIT_RULES.md` — Git, branch, commit, and repository rules.
* `ASSETS.md` — Rules for sourcing, licensing, downloading, storing, and tracking external assets.
* `SECURITY.md` — Security policies and vulnerability reporting.
* `PROMPTS.md` — Project-specific prompts or AI instructions.
* `CREDS_PREDEFINED.md` — Documentation for predefined credentials or credential configuration.
* `CREDS_DB.md` — Documentation related to database credentials and configuration.

Do not assume conventions when they are documented elsewhere in the repository.

## General Behavior

When working on this repository:

1. Understand the task before modifying files.
2. Inspect existing code and documentation before implementing something new.
3. Follow existing project patterns and conventions.
4. Prefer simple, maintainable solutions over unnecessary complexity.
5. Do not introduce new dependencies, frameworks, services, or architectural patterns without a clear reason.
6. Keep changes focused on the requested task.
7. Avoid unrelated refactoring.
8. Do not remove or rewrite existing functionality unless required by the task.
9. Update relevant documentation when behavior, architecture, configuration, or processes change.
10. Verify your work before considering the task complete.

## Documentation Is Authoritative

Files in `docs/` contain project-specific instructions.

When instructions exist in a dedicated document, follow that document rather than inventing new conventions.

Do not duplicate large sections of project rules into other files. Reference the appropriate documentation instead.

If documentation and existing implementation appear to conflict, investigate the conflict before making significant changes.

## Code Changes

Before changing code:

* Inspect the relevant files.
* Understand how the existing implementation works.
* Search for related functionality elsewhere in the project.
* Check `ARCHITECTURE.md` and `TECHNOLOGY.md` when making structural or technical decisions.

When implementing changes:

* Follow existing naming and formatting conventions.
* Reuse existing utilities and abstractions when appropriate.
* Keep code readable and maintainable.
* Avoid unnecessary abstractions.
* Handle errors appropriately.
* Do not leave temporary debugging code behind.

## Dependencies

Before adding a dependency:

1. Check whether the project already provides the required functionality.
2. Check `TECHNOLOGY.md` for approved technologies.
3. Prefer existing dependencies when practical.
4. Only add a new dependency when it provides a clear benefit.

Do not replace existing technology choices without explicit justification or instruction.

## External Assets

Any externally sourced asset must follow `ASSETS.md`.

Do not directly use assets found on the internet without verifying their license and provenance.

Externally sourced assets must first be downloaded into the project's `assets/` directory and registered according to `ASSETS.md`.

## Credentials and Secrets

Never invent, expose, commit, or hard-code credentials, secrets, tokens, passwords, private keys, or other sensitive information.

Follow:

* `CREDS_PREDEFINED.md`
* `CREDS_DB.md`
* `SECURITY.md`

Use the project's established credential and configuration mechanisms.

Never place real secrets into documentation, examples, tests, logs, or source code.

## Git

Follow `GIT_RULES.md` for all Git-related operations.

Do not perform destructive Git operations unless explicitly required and permitted by the project's rules.

Keep changes focused and avoid modifying unrelated files.

## Testing and Verification

Before completing a task:

* Run relevant tests when available.
* Run applicable formatting, linting, type-checking, and validation tools.
* Check for obvious regressions.
* Verify that the requested functionality works.
* Review the final diff for accidental or unrelated changes.

Do not claim that tests or checks passed unless they were actually run.

If something cannot be tested, clearly state that it was not tested.

## Documentation Updates

Update documentation when a change affects:

* Project behavior
* Architecture
* Setup
* Configuration
* Dependencies
* Development processes
* Security
* Credentials
* External assets
* Public interfaces

Keep documentation consistent with the implementation.

## Handling Uncertainty

Do not guess about important project behavior.

When uncertain:

1. Inspect the repository.
2. Search existing code.
3. Read the relevant documentation.
4. Follow established patterns.
5. Choose the least destructive reasonable approach.

If a decision cannot safely be inferred from the repository, ask for clarification rather than making a major assumption.

## Scope Control

Only change what is necessary to complete the requested task.

Do not use a small task as an opportunity to:

* Perform unrelated refactoring.
* Replace working systems.
* Change project architecture.
* Introduce new frameworks.
* Rename unrelated files.
* Reformat the entire codebase.
* Remove functionality that appears unused without verification.

## Completion

A task should only be considered complete when:

* The requested change has been implemented.
* Relevant project rules have been followed.
* Appropriate verification has been performed.
* Relevant documentation has been updated.
* No known temporary files, debugging code, or accidental changes remain.

When reporting completion, briefly describe what changed and mention any tests, checks, limitations, or unresolved issues.
