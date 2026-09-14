# Project Rules

This document defines the basic rules that apply throughout the project.

Always prioritize the user's requirements and instructions.

## General Rules

* Keep implementations simple, readable, and maintainable.
* Avoid unnecessary complexity and over-engineering.
* Follow existing project conventions before introducing new ones.
* Keep changes focused on the requested task.
* Do not remove or change existing functionality without a reason.
* Prefer established and maintained technologies.
* Handle errors properly and avoid silent failures.
* Validate changes before considering work complete.
* Update documentation when behavior or structure changes.

## Security

Security must be considered throughout development.

* Never expose credentials, passwords, secrets, keys, or tokens.
* Validate untrusted input.
* Enforce authentication and authorization server-side.
* Follow least privilege.
* Use secure defaults.
* Never intentionally weaken security merely for convenience.

Follow `SECURITY.md`, `CREDS_PREDEFINED.md`, and `CREDS_DB.md` for detailed requirements.

## Project Structure

Follow `STRUCTURE.md` and existing repository conventions.

Do not create unnecessary top-level directories or duplicate existing functionality.

## Architecture & Technology

Follow:

* `ARCHITECTURE.md` for architectural principles.
* `TECHNOLOGY.md` for technology choices.
* `GIT_RULES.md` for Git and repository practices.
* `ASSETS.md` for external assets.
* `PENTEST.md` for basic security testing.

Prefer the simplest solution appropriate for the project's current requirements while leaving reasonable room for future growth.

## Dependencies

Only add dependencies when they provide clear value.

Prefer existing project dependencies and maintained libraries over custom implementations or unnecessary packages.

## AI Agents

AI agents should:

1. Understand the user's request before making changes.
2. Read relevant project documentation.
3. Inspect existing code before modifying it.
4. Follow established patterns.
5. Avoid guessing when important information can be determined from the repository.
6. Test or validate changes where practical.
7. Clearly state anything that could not be verified.

## Final Rule

**The user's requirements take priority.**

These rules provide sensible defaults, not reasons to ignore explicit user instructions or unnecessarily complicate the project.
