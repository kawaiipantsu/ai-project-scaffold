# Git & Repository Rules

This document defines the basic Git and GitHub workflow for this project.

The goal is to protect the integrity of the source code while keeping contribution and maintenance simple.

Use sensible checks, clear history, and lightweight automation.

Avoid unnecessary process overhead.

---

# General Principles

The repository should be:

* Easy to contribute to.
* Difficult to accidentally break.
* Simple to review.
* Protected against obvious mistakes.
* Automatically checked where practical.
* Flexible enough for small and fast-moving projects.

Prefer lightweight safeguards over complicated approval processes.

---

# Main Branch

The default branch should normally be:

`main`

The `main` branch should be treated as the stable integration branch.

Direct pushes to `main` should be restricted when GitHub branch protection is available.

Prefer changes to reach `main` through Pull Requests.

---

# Branch Protection

Where practical, enable branch protection for `main`.

Recommended protections:

* Require Pull Requests before merging.
* Require required CI checks to pass.
* Prevent force pushes.
* Prevent branch deletion.
* Require the branch to be up to date when appropriate.

Do not require excessive approvals for small projects.

A single approval or maintainer merge may be sufficient.

For very small or solo-maintained projects, allow maintainers enough flexibility to avoid making normal maintenance unnecessarily difficult.

---

# Branches

Use short-lived branches for changes.

Examples:

```text
feature/add-api
fix/login-error
docs/update-readme
refactor/config-loader
chore/update-dependencies
```

Prefer clear, descriptive branch names.

Avoid keeping stale branches around after they have been merged.

---

# Pull Requests

Use Pull Requests for meaningful changes.

A Pull Request should normally:

* Describe what changed.
* Explain why the change is needed.
* Mention relevant issues when applicable.
* Keep unrelated changes out.
* Pass required automated checks.
* Be reviewed before merge when practical.

Small documentation changes or trivial maintainer fixes may use a lighter process where appropriate.

Do not make the Pull Request process unnecessarily bureaucratic.

---

# Pull Request Size

Prefer small and focused Pull Requests.

Smaller changes are easier to:

* Review.
* Test.
* Revert.
* Understand.
* Debug.

Avoid mixing unrelated features, refactors, formatting changes, and dependency updates into the same Pull Request unless they are tightly connected.

---

# Commits

Commit messages should be clear and meaningful.

Examples:

```text
Add user audit logging
Fix migration ordering
Update installation instructions
Improve API validation
```

Avoid meaningless commit messages such as:

```text
stuff
changes
fix
test
update
asdf
```

Perfect commit conventions are not required.

Clarity is more important than strict formatting.

---

# Commit Hygiene

Before committing:

* Review `git status`.
* Review staged changes.
* Ensure no credentials or secrets are included.
* Remove temporary/debug files.
* Avoid committing build output unless intentionally required.
* Avoid unrelated formatting churn.

Use `.gitignore` to exclude common generated and local files.

Remember that `.gitignore` is not a security boundary.

---

# Secrets

Never commit:

* Passwords
* API keys
* Access tokens
* Refresh tokens
* Private keys
* Database credentials
* Encryption keys
* Secret environment files
* Sensitive configuration
* Authentication cookies
* Internal secrets

If a secret is committed accidentally:

1. Treat it as compromised.
2. Rotate or revoke it.
3. Remove it from active configuration.
4. Clean repository history if appropriate.
5. Review how the leak occurred.

Deleting the latest commit alone does not make the secret safe.

See:

`docs/SECURITY.md`

---

# GitHub Issues

Use GitHub Issues for:

* Bugs
* Feature requests
* Security-adjacent non-sensitive problems
* Documentation improvements
* Project planning
* Enhancement requests

Do not use public issues to disclose sensitive credentials or secrets.

Security reporting should follow the root `SECURITY.md`.

---

# Issue Templates

Create simple issue templates appropriate to the project.

Recommended templates include:

```text
.github/ISSUE_TEMPLATE/
├── bug_report.md
├── feature_request.md
└── config.yml
```

Add more templates only when they provide real value.

For example:

* Documentation issue
* Performance issue
* Packaging issue

Avoid creating too many issue categories.

The goal is to help users provide useful information, not make issue creation difficult.

---

# Bug Report Template

Bug reports should encourage users to include:

* What happened.
* What they expected.
* Steps to reproduce.
* Version or commit.
* Operating system/environment.
* Relevant logs with sensitive data removed.
* Screenshots when useful.

Never ask users to post credentials, secrets, private keys, or access tokens.

---

# Feature Request Template

Feature requests should encourage users to explain:

* What they want.
* Why it is useful.
* The problem being solved.
* Possible alternatives.

Keep the template short.

---

# GitHub Actions

Use GitHub Actions for lightweight automated validation.

The exact checks should match the project's technology stack.

Typical checks may include:

* Build
* Tests
* Linting
* Formatting checks
* Static analysis
* Type checking
* Dependency validation
* Security scanning

Do not add expensive or slow workflows without a clear benefit.

CI should help contributors, not punish them.

---

# Basic CI

A basic Pull Request workflow should preferably:

1. Check out the repository.
2. Install the required toolchain.
3. Restore dependency caches where useful.
4. Build the project.
5. Run tests.
6. Run linting or formatting checks.
7. Report failures clearly.

Only require checks that are reliable and reasonably fast.

Flaky checks should be fixed or removed from required status checks.

---

# Validation by Technology

Examples may include:

## Rust

```text
cargo check
cargo test
cargo fmt --check
cargo clippy
```

## Go

```text
go build ./...
go test ./...
go vet ./...
gofmt
```

## Make-based projects

Use available project targets such as:

```text
make build
make test
make lint
```

The exact commands should be documented in:

`docs/TECHNOLOGY.md`

---

# Security Scanning

Enable lightweight security scanning where GitHub or the project tooling supports it.

Useful protections may include:

* Dependabot alerts
* Dependency review
* Secret scanning
* Code scanning
* CodeQL
* Package vulnerability scanning

Use available GitHub-native protections where practical.

Do not add multiple overlapping scanners unless they provide meaningful additional value.

---

# Dependabot

Dependabot may be enabled for supported package ecosystems.

Prefer a manageable update cadence.

Avoid creating excessive automated Pull Requests.

Where supported, group routine dependency updates when this makes maintenance easier.

Security updates should generally receive higher priority than routine version bumps.

---

# CodeQL

For supported languages, CodeQL may be enabled as a basic static security check.

It should normally run:

* On Pull Requests.
* On pushes to `main`.
* Periodically if useful.

Do not block development on noisy or irrelevant findings without reviewing them.

Security tooling should assist maintainers rather than blindly dictate project decisions.

---

# Secret Scanning

Enable GitHub secret scanning and push protection when available.

These protections help prevent credentials from entering Git history.

They do not replace normal developer review.

Always inspect changes before committing.

---

# Dependency Changes

New dependencies should have a clear purpose.

Before adding a dependency:

* Check whether the project already provides the needed functionality.
* Prefer maintained packages.
* Avoid suspicious or abandoned packages.
* Review licensing where relevant.
* Consider security implications.

See:

`docs/TECHNOLOGY.md`

---

# Reviews

Code review should focus on meaningful risks.

Reviewers should consider:

* Does the change solve the intended problem?
* Is the implementation understandable?
* Are tests appropriate?
* Are there obvious security issues?
* Does it introduce unnecessary complexity?
* Does it follow project structure and conventions?
* Does documentation need updating?

Avoid blocking changes over minor personal style preferences when automated formatting or existing conventions already provide consistency.

---

# Merge Strategy

Prefer a simple merge strategy.

For many projects, **Squash and Merge** is a good default because it keeps `main` history clean.

Regular merge commits are also acceptable if the project benefits from preserving branch history.

Use one primary strategy consistently when practical.

---

# Rebase & Force Pushes

Rebasing local feature branches is acceptable.

Do not force-push shared or protected branches such as:

`main`

Force-pushing a personal feature branch may be acceptable when it does not disrupt other contributors.

Use `--force-with-lease` rather than unrestricted force pushes when rewriting your own remote branch.

---

# Releases

When releases are used:

* Release from known commits or tags.
* Use meaningful version tags.
* Keep release notes concise.
* Include important fixes and compatibility changes.
* Do not include credentials or internal secrets in release artifacts.

Release automation may be added when it simplifies maintenance.

Do not introduce complex release infrastructure unless needed.

---

# Tags

Use annotated or standard version tags according to project needs.

Common examples:

```text
v1.0.0
v1.1.0
v2.0.0
```

Semantic versioning is recommended when it fits the project.

---

# Generated Files

Generated files should generally not be committed unless they are intentionally part of the source or distribution process.

Examples normally excluded:

* Build output
* Binaries
* Logs
* Temporary files
* Coverage reports
* Local databases
* Dependency caches

Follow `.gitignore` and `docs/STRUCTURE.md`.

---

# Documentation

Update relevant documentation when changes affect:

* Installation
* Usage
* Architecture
* Security
* Configuration
* Database schema
* Dependencies
* Development workflow
* Repository structure

Do not leave documentation knowingly inconsistent with the implementation.

---

# Database Changes

Database schema changes should be handled through the project's migration process.

Store migrations under:

`database/migrations/`

Do not silently alter deployed migrations when a new migration is more appropriate.

See:

`docs/STRUCTURE.md`

and:

`docs/CREDS_DB.md`

---

# AI Agent Git Rules

AI agents working on this repository should:

1. Read this file before performing substantial Git-related work.
2. Inspect the current repository state before modifying files.
3. Keep changes focused on the requested task.
4. Avoid unrelated refactoring.
5. Never commit credentials or secrets.
6. Follow existing branch and Pull Request conventions.
7. Run relevant validation before claiming completion.
8. Do not claim CI or tests passed unless they were actually run.
9. Avoid destructive Git commands unless explicitly required.
10. Do not force-push protected branches.
11. Do not rewrite shared history unnecessarily.
12. Update documentation when required.
13. Preserve maintainability over process complexity.

---

# Recommended GitHub Baseline

For a typical project, a good lightweight baseline is:

* Protected `main` branch.
* Pull Requests for meaningful changes.
* At least one passing CI workflow.
* Build validation.
* Tests where available.
* Linting or formatting checks where practical.
* Dependabot alerts.
* Secret scanning.
* CodeQL or equivalent when supported.
* Simple bug and feature request templates.

This provides useful protection without creating excessive maintenance overhead.

---

# Keep the Process Practical

Repository protections should reduce mistakes, not make normal development frustrating.

Do not add:

* Excessive approval requirements.
* Large numbers of mandatory workflows.
* Slow checks with little value.
* Redundant security scanners.
* Complex branching models for small projects.
* Unnecessary release bureaucracy.

Prefer automation where it removes repetitive manual work.

Prefer human judgment where rigid rules would create more problems than they solve.

The project should remain easy to maintain while still protecting the integrity of the source code.
