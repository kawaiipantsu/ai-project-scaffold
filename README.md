# AI Project Scaffold

[![Validate](https://github.com/kawaiipantsu/ai-project-scaffold/actions/workflows/validate.yml/badge.svg)](https://github.com/kawaiipantsu/ai-project-scaffold/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/kawaiipantsu/ai-project-scaffold)](https://github.com/kawaiipantsu/ai-project-scaffold/releases/latest)

A repository for your own project scaffold, AI instructions, and architecture notes.
You define the contents of `ai-scaffold/`; this repository provides validation,
PR-only maintenance, documentation, and ZIP releases.

**[Website](https://thugs.red) · [Wiki](https://github.com/kawaiipantsu/ai-project-scaffold/wiki) · [Download ZIP](https://github.com/kawaiipantsu/ai-project-scaffold/releases/latest/download/scaffold.zip)**

## Get started

```sh
cd /path/to/project
curl --fail --location --output scaffold.zip \\
  https://github.com/kawaiipantsu/ai-project-scaffold/releases/latest/download/scaffold.zip
unzip -n scaffold.zip && rm scaffold.zip
```

The ZIP extracts into `ai-scaffold/`, including any tracked hidden files you add.
The payload is intentionally empty until you populate it. Existing files are preserved
by `unzip -n`; extracting an empty ZIP will not remove files from an older installation.
For checksum verification and upgrades, see [releases](docs/RELEASING.md).

Git does not track empty directories. After cloning, run `mkdir -p ai-scaffold` if
needed. No placeholder or generated instructions are placed inside it. Release ZIPs
always include an explicit `ai-scaffold/` directory entry, even when it is empty.

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

## Add your scaffold

Populate `ai-scaffold/` with the files, directories, instructions, and prompts you want.
Commit those files on `develop` and open a PR to `main`. Only tracked payload files
are packaged. Payload lint and content requirements are deferred until your files
are ready; current checks cover repository maintenance. Add any files and exact rule sentences that must remain present to
`contrib/requirements.json`; there are no preset requirements for your payload.

## Maintainer workflow

Work on `develop` and open a PR into protected `main`. Keep individual, focused
commits; merge commits preserve the detailed history. Required CI checks lint,
required files and rule text, sensitive patterns, tests, and archive contents.
Version tags on `main` publish `scaffold.zip` and a SHA-256 checksum.

Read [contributing](docs/CONTRIBUTING.md), [validation](docs/VALIDATION.md),
[security](docs/SECURITY.md), and [wiki maintenance](docs/WIKI.md).
