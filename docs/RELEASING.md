# Releases

Releases are version tags on commits already reachable from `main`.
Use semantic versions such as `v1.0.0`. Never move a published tag.
An active ruleset prevents updating or deleting version tags.

After manually merging the PR on GitHub, run from a clean `develop` checkout:

```sh
contrib/publish-release        # patch: v1.2.0 -> v1.2.1
contrib/publish-release minor  # minor: v1.2.0 -> v1.3.0
contrib/publish-release major  # major: v1.2.0 -> v2.0.0
```

Choose one command. The helper requires Git, Python 3.12+, an authenticated `gh`,
and permission to push version tags. It fetches main and tags, increments the
highest remote `vMAJOR.MINOR.PATCH` version, creates an annotated tag on
`origin/main`, and pushes it. Without existing versions, it starts from `v0.0.0`.
Unmerged develop commits are excluded. The current branch and Git identity stay
unchanged. Local version tags cannot advance the release version.

The helper waits up to two minutes for the release workflow to appear, then watches
it to completion and verifies the published ZIP and checksum assets. It prints the
release URL on success and exits with an error if publishing fails.

If main already has the latest tag, rerunning checks that release without bumping.
After a workflow failure, inspect and rerun the failed workflow in GitHub Actions,
then run the helper again. If the tag push fails, the local tag remains: inspect
it and use the exact `git push origin refs/tags/vX.Y.Z` command printed by the helper.
Existing tags are never overwritten or deleted. A conflicting local tag or a latest
version outside main history requires manual resolution.

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
