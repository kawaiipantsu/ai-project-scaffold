# Releases

Releases are version tags on commits already reachable from `main`.
Use semantic versions such as `v1.0.0`. Never move a published tag.

```sh
git fetch origin main
git tag -a v1.0.0 origin/main -m 'Release v1.0.0'
git push origin v1.0.0
```

The release workflow verifies main ancestry, rechecks the contract and tests,
builds `scaffold.zip` and `scaffold.zip.sha256`, and publishes a GitHub release.
`scaffold.zip` contains exactly the tracked `ai-scaffold/` tree, including dotfiles.
Timestamps and permissions are normalized for reproducible archives.
GitHub's automatic source archives are not the scaffold download.

```sh
cd /path/to/project
curl --fail --location --output scaffold.zip \
  https://github.com/kawaiipantsu/ai-project-scaffold/releases/latest/download/scaffold.zip
curl --fail --location --output scaffold.zip.sha256 \
  https://github.com/kawaiipantsu/ai-project-scaffold/releases/latest/download/scaffold.zip.sha256
sha256sum --check scaffold.zip.sha256
unzip -n scaffold.zip
rm scaffold.zip scaffold.zip.sha256
```

`-o` / `--output` chooses the filename; `-O` uses the remote filename and takes no
local filename argument. `unzip -n` preserves existing files. Inspect and deliberately
merge updates if an `ai-scaffold/` folder already exists.

After extraction, read `ai-scaffold/README.md`. Most AI tools discover root-level
instruction files, so consciously merge `ai-scaffold/AGENTS.md` into a project-root
`AGENTS.md`, then adapt its paths and project-specific decisions. Existing project
instructions take precedence until you explicitly reconcile them.
