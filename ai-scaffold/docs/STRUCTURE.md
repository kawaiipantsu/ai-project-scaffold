# Project Structure

This document describes the standard repository scaffold and the intended purpose of its directories and files.
The scaffold provides a predictable starting point for projects while allowing technology-specific directories and files to be added as the project develops.
Developers and AI agents should follow this structure and avoid creating new top-level directories without a clear reason.

---

## Base Structure

```text
.
├── assets/
├── contrib/
├── database/
│   ├── migrations/
│   └── schemas/
├── docs/
├── .github/
│   ├── files/
│   └── images/
├── logs/
├── CONTRIBUTORS.md
├── .gitignore
├── LICENSE
├── README.md
└── SECURITY.md
```

Additional directories may be introduced when required by the project's selected technologies or architecture.

Examples may include:

```text
src/
cmd/
internal/
pkg/
crates/
tests/
scripts/
config/
```

Do not create these directories automatically unless they are appropriate for the project.

---

# Directory Structure

## `assets/`

```text
assets/
```

Stores externally sourced and project-owned assets.

Examples include:

* Images
* Icons
* Fonts
* Audio
* Video
* SVG files
* 3D models
* Textures
* Datasets
* Other external resources

Externally sourced assets must follow the requirements defined in:

```text
docs/ASSETS.md
```

All externally sourced assets must first be downloaded into `assets/`, documented, and tracked according to the asset policy.
The `assets/` directory acts as the repository's source of truth for sourced external assets.

---

## `contrib/`

```text
contrib/
```

Contains supporting material that contributes to the project but does not belong directly in the primary application source.
Depending on the project, this may include:

* Integration helpers
* Example configurations
* Packaging helpers
* Service definitions
* Third-party integration files
* Deployment examples
* Community-contributed utilities
* Supporting scripts

Files placed here should have a clear purpose related to supporting the project.

---

## `database/`

```text
database/
├── migrations/
└── schemas/
```

Contains version-controlled database definitions and database change history.

### `database/migrations/`

Contains database migration files.

Examples include:

```text
database/migrations/
├── 0001_initial.sql
├── 0002_add_users.sql
└── 0003_add_indexes.sql
```

Migrations should:

* Be version controlled.
* Have deterministic ordering.
* Represent intentional database changes.
* Avoid containing credentials or secrets.
* Be safe to review before execution.
* Follow the migration conventions selected by the project.

Do not silently modify an already-deployed migration when a new migration should be created instead.
The exact migration format may depend on the database tooling selected in `docs/TECHNOLOGY.md`.

### `database/schemas/`

Contains database schema definitions or canonical schema files.
Examples may include:

```text
database/schemas/
├── schema.sql
├── users.sql
└── permissions.sql
```

Depending on the project, this directory may contain:

* SQL schema definitions
* Table definitions
* Views
* Index definitions
* Stored procedures
* Functions
* Triggers
* Database extensions
* Roles or permission definitions when appropriate

Schema files must not contain real passwords, credentials, access tokens, or other secrets.
Database credential handling is documented separately in:

```text
docs/CREDS_DB.md
```

---

## `docs/`

```text
docs/
├── AGENTS.md
├── ARCHITECTURE.md
├── ASSETS.md
├── CREDS_DB.md
├── CREDS_PREDEFINED.md
├── GIT_RULES.md
├── PENTEST.md
├── PROJECT.md
├── PROJECT_PROGRESS.md
├── PROJECT_RULES.md
├── PROMPTS.md
├── SECURITY.md
├── STRUCTURE.md
└── TECHNOLOGY.md
```

Contains internal project documentation and operational instructions.
This directory is the primary source of project-specific guidance for developers and AI agents.

### `docs/AGENTS.md`

Entry point and operating instructions for AI coding agents and automated development tools.

### `docs/ARCHITECTURE.md`

Documents the application's architecture, components, boundaries, data flow, and important architectural decisions.

### `docs/ASSETS.md`

Defines how external assets are sourced, licensed, downloaded, stored, copied, and tracked.

### `docs/CREDS_DB.md`

Documents how database credentials and database-related secrets are expected to be provided and handled.

### `docs/CREDS_PREDEFINED.md`

Documents predefined credential mechanisms or credential configuration supplied to the project.
Real secrets must not be stored directly in documentation.

### `docs/GIT_RULES.md`

Defines Git-related conventions and repository workflow requirements.

### `docs/PENTEST.md`

Describes simple security testing criteria that may be enforced/tested for.

### `docs/PROJECT.md`

Describes the project itself, including its purpose, goals, requirements, and scope.

### `docs/PROJECT_PROGRESS.md`

Keep a log/list of what has been done so far, phases, waves if such things are there. This is simply for someone to see what has been done so far.

### `docs/PROJECT_RULES.md`

Contains general project-wide rules and constraints.

### `docs/PROMPTS.md`

Contains project-specific prompt thoughout the project. Everytime from start to end, all prompts should be kept here.

### `docs/SECURITY.md`

Defines secure coding requirements, secret handling, web security, TLS/HTTPS considerations, and other application security requirements.

### `docs/STRUCTURE.md`

This file.
Defines the standard repository scaffold and explains where project files should be placed.

### `docs/TECHNOLOGY.md`

Documents the technologies, languages, frameworks, libraries, databases, build systems, and other technical choices used by the project.

---

## `.github/`

```text
.github/
├── files/
├── images/
```

Contains GitHub-specific repository resources.
Standard GitHub configuration may also be added here when needed, including:

```text
.github/
├── ISSUE_TEMPLATE/
├── workflows/
├── dependabot.yml
├── CODEOWNERS
└── pull_request_template.md
```

### `.github/files/`

Contains files intended specifically for GitHub-facing repository content.

### `.github/images/`

Contains images used by GitHub-facing documentation, issue templates, README content, or other repository presentation material.
Do not use `.github/` as a general-purpose application asset directory.
General project assets belong in `assets/`.

---

## `logs/`

```text
logs/
```

Provides the standard location for local application logs when file-based logging is required.
Log contents should normally be excluded from Git.
Logs must never contain credentials, passwords, API keys, access tokens, private keys, authentication cookies, or other sensitive secrets.

See:

```text
docs/SECURITY.md
```

for security and logging requirements.

---

# Root Files

## `README.md`

The primary public introduction to the project.
Refere to the README.md file it self for instructions on what to replace it with.

---

## `CONTRIBUTORS.md`

Contains contributor information and/or contribution-related information for the project.
Project-specific contribution procedures should remain consistent with the repository's Git and project rules.

---

## `SECURITY.md`

The public-facing GitHub security policy.
This file may describe how users should report security-related issues.

Do not confuse it with:

```text
docs/SECURITY.md
```

The two files serve different purposes:

* `/SECURITY.md` — public repository security/reporting information.
* `/docs/SECURITY.md` — internal secure development and implementation requirements.

---

## `LICENSE`

Contains the project's license.
The license applies according to its terms and should not be modified without explicit authorization.
Licenses for externally sourced assets may differ from the project's main license and must be tracked according to `docs/ASSETS.md`.

---

## `.gitignore`

Defines files and directories that should not normally be committed to Git.
This includes generated or local content such as:

* Build artifacts
* Binaries
* Logs
* Temporary files
* Local databases
* Development caches
* Environment files
* Credentials
* IDE state

Remember:

**`.gitignore` is not a security boundary.**

Sensitive information must never be committed simply because a matching `.gitignore` rule exists.
Also you might need to edit/change content in the .gitignore in order to accomendate the project.

---

# Technology-Specific Structure

The base scaffold intentionally does not enforce a particular programming language or framework.
Technology-specific directories should be introduced according to the project's actual requirements.
For example, a Rust project may use:

```text
src/
crates/
tests/
Cargo.toml
Cargo.lock
```

A Go project may use:

```text
cmd/
internal/
pkg/
go.mod
go.sum
```

A C/C++ or Make-based project may use:

```text
src/
include/
tests/
Makefile
```

These are examples, not mandatory directories.
The selected structure should be documented in:

```text
docs/ARCHITECTURE.md
docs/TECHNOLOGY.md
```

---

# Structure Rules

Developers and AI agents should follow these general rules:

1. Keep the repository root clean.
2. Put files in the most appropriate existing directory.
3. Do not create new top-level directories unnecessarily.
4. Follow established language/framework conventions where they do not conflict with project rules.
5. Store internal project documentation in `docs/`.
6. Store database migrations and schemas in `database/`.
7. Store externally sourced assets according to `docs/ASSETS.md`.
8. Keep generated build output outside version-controlled source directories.
9. Keep logs and runtime-generated data out of Git.
10. Never store credentials or secrets in the repository.
11. Update this document when introducing a significant permanent structural convention.
12. Do not move existing directories or files without understanding their purpose and references.

---

# AI Agent Instructions

Before creating a new file or directory, AI agents should determine whether an appropriate location already exists.
Do not create arbitrary directories simply for convenience.
Before making structural changes:

1. Read `docs/PROJECT.md`.
2. Read `docs/PROJECT_RULES.md`.
3. Read `docs/ARCHITECTURE.md`.
4. Read `docs/TECHNOLOGY.md`.
5. Check the existing repository structure.
6. Follow established conventions.

When adding database files:

* Place migrations under `database/migrations/`.
* Place schema definitions under `database/schemas/`.
* Follow `docs/CREDS_DB.md` for database credential handling.
* Never embed real credentials in SQL files.

When adding external assets:

* Follow `docs/ASSETS.md`.
* Download and register sourced assets before using them elsewhere.

When adding generated files:

* Determine whether they belong in version control.
* Update `.gitignore` when appropriate.

When introducing a significant new permanent directory, update this document so future developers and agents understand its purpose.
The repository structure should remain predictable, minimal, and easy to understand.
