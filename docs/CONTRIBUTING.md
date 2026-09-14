# Contributing

## Two branches

`develop` is the shared integration branch. `main` is the release branch.
Commit focused changes to `develop`, push, and open a PR targeting `main`.
Use a merge commit to preserve individual commits. Squash and rebase merging are disabled.
After merging, fast-forward local `main`, then merge `origin/main` into `develop` and push it.
Do not force-push shared history. Rules prevent creating other branches in this
repository and protect develop from deletion and force pushes. Make dependency
updates on develop as focused commits; external contributors can use forks.

```sh
git switch develop
git pull --ff-only origin develop
# Make a focused change, validate it, and commit it.
git push origin develop
gh pr create --base main --head develop
```

Main requires the `Validate scaffold` GitHub Actions check, an up-to-date branch,
resolved review threads, and a PR. Force pushes and deletion are prohibited.
The ruleset has no bypass actors, including administrators. Administrators can still
edit repository settings; GitHub settings cannot prevent that administrative ability.
No approval count is imposed so the repository owner can merge their own checked PR.

## Scaffold shortcuts

```sh
git switch develop
contrib/commit-scaffold "describe your scaffold change"
contrib/pr-scaffold
```

The first helper stages the payload, commits with `New scaffold change: <note>`,
and pushes develop. The second synchronizes branches and creates or updates a PR
with commit notes, changed files, and a reviewer checklist. It leaves the merge for
you to perform manually on GitHub. See [helper details](../contrib/README.md).

## Before opening a PR

Use the fixes or scaffold changes issue form. Describe the reason, changed behavior,
and validation. Keep AI rules explicit and technology decisions evidence-based.
Never include private logs, credentials, personal addresses, or client information.
Use placeholders in examples and preserve the configured global Git identity.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r contrib/requirements-dev.txt
python3 contrib/validate.py
python3 -m unittest discover -s contrib/tests
python3 -m ruff check contrib contrib/commit-scaffold contrib/pr-scaffold contrib/publish-release
python3 -m yamllint --strict .github
npx --yes markdownlint-cli@0.45.0 '**/*.md' --ignore node_modules --ignore ai-scaffold --ignore .venv
python3 contrib/package.py
```

Wiki content lives in the separate wiki Git repository. See `docs/WIKI.md`.
