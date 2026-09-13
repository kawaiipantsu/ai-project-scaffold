# AI Project Scaffold

[![Validate](https://github.com/kawaiipantsu/ai-project-scaffold/actions/workflows/validate.yml/badge.svg)](https://github.com/kawaiipantsu/ai-project-scaffold/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/kawaiipantsu/ai-project-scaffold)](https://github.com/kawaiipantsu/ai-project-scaffold/releases/latest)

A reusable starting point for AI-assisted projects: clear working rules, project
requirements, technology and architecture decisions, prompts, and directory structure.
It is technology-neutral so each project can document its real stack.

**[Website](https://thugs.red) · [Wiki](https://github.com/kawaiipantsu/ai-project-scaffold/wiki) · [Download ZIP](https://github.com/kawaiipantsu/ai-project-scaffold/releases/latest/download/scaffold.zip)**

## Get started

```sh
cd /path/to/project
curl --fail --location --output scaffold.zip \\
  https://github.com/kawaiipantsu/ai-project-scaffold/releases/latest/download/scaffold.zip
unzip -n scaffold.zip && rm scaffold.zip
```

The ZIP extracts into `ai-scaffold/` and includes hidden files. Read
[the scaffold guide](ai-scaffold/README.md), merge its instructions into your project
root, and fill in the project decisions. Existing files are preserved by `unzip -n`.
For checksum verification and upgrades, see [releases](docs/RELEASING.md).

## Repository layout

```text
./
├── .github/       # Issue forms, PR template, CI, releases, security
├── docs/          # Documentation for maintaining this repository
├── contrib/       # Validation, tests, packaging, maintenance
├── ai-scaffold/   # The complete distributable project scaffold
├── AGENTS.md      # Working rules for this repository
└── README.md
```

## What the scaffold provides

| Area | Included guidance |
| --- | --- |
| AI behavior | Explicit working rules, evidence, privacy, focused changes |
| Requirements | Scope, acceptance criteria, constraints, open questions |
| Architecture | Boundaries, data flow, security, reliability, decision records |
| Technology | Stack selection, dependencies, environments |
| Development | Setup, lint, tests, build, Git workflow |
| Prompts | Planning, implementation, review |
| Structure | Source, tests, maintenance, docs, GitHub notes |

## Maintainer workflow

Work on `develop` and open a PR into protected `main`. Keep individual, focused
commits; merge commits preserve the detailed history. Required CI checks lint,
required files and rule text, sensitive patterns, tests, and archive contents.
Version tags on `main` publish `scaffold.zip` and a SHA-256 checksum.

Read [contributing](docs/CONTRIBUTING.md), [validation](docs/VALIDATION.md),
[security](docs/SECURITY.md), and [wiki maintenance](docs/WIKI.md).
