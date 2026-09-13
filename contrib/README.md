# Maintenance tools

Run tools from the repository root with Python 3.12 or newer.

- `validate.py`: check required structure, rule text, links, and sensitive patterns.
- `requirements.json`: explicit minimum content contract.
- `package.py`: build the tracked scaffold ZIP and SHA-256 checksum in `dist/`.
- `tests/`: regression and negative tests for validation and packaging.

Development lint dependencies are pinned in `requirements-dev.txt`.

## Scaffold shortcuts

Requires Git, Python 3.12+, and an authenticated GitHub CLI (`gh`) for PRs.
Run on `develop`. Helpers locate the repository from their own path, so they also
work when invoked from another directory.

```sh
contrib/commit-scaffold "describe your change"
contrib/pr-scaffold
```

`commit-scaffold` stages only `ai-scaffold/` (including additions and deletions),
commits as `New scaffold change: describe your change`, and pushes to `origin/develop`.
It uses the existing Git identity. It refuses an empty note, no changes, a different
branch, or unrelated staged files. Unstaged maintenance changes are left alone.
If pushing fails, the local commit remains; resolve the remote divergence and retry
`git push origin develop` rather than creating a duplicate commit.

`pr-scaffold` requires a clean working tree and already-created commits. It fetches
and merges remote develop and main into local develop, preserving individual
commits, then pushes develop. Conflicting merges are aborted for manual resolution.
It creates a PR into main or refreshes the existing open PR, using a unified title,
overview, commit notes, file list, diff summary, and review checklist explaining why
each review area matters. CI status is left for GitHub to report; no successful
validation is invented. If main already contains all commits, no PR is created.

The helper never approves, merges a PR, or enables auto-merge. Review and merge from
the GitHub page once checks and feedback are resolved. Rerunning it replaces the PR
title and description, so keep discussion in review comments.
