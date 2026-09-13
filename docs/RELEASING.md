# Releases

Releases are version tags on commits already reachable from `main`.
Use semantic versions such as `v1.0.0`. Never move a published tag.
An active ruleset prevents updating or deleting version tags.

```sh
git fetch origin main
git tag -a v1.0.0 origin/main -m 'Release v1.0.0'
git push origin v1.0.0
```

The release workflow verifies main ancestry, rechecks the contract and tests,
builds `scaffold.zip` and `scaffold.zip.sha256`, and publishes a GitHub release.
`scaffold.zip` contains an explicit `ai-scaffold/` directory entry plus exactly the
tracked payload files, including dotfiles. An empty payload produces an empty folder.
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

The payload is intentionally empty until the owner populates it. Git does not track
empty directories; use `mkdir -p ai-scaffold` after cloning when needed. ZIP extraction
recreates the folder even when no files are tracked. Extracting an empty ZIP over an
existing folder does not delete its old contents; use a fresh directory for a clean start.

When adding your own AI instructions, document how a consuming project should adopt
them. This repository does not generate those instructions or choose their layout.
