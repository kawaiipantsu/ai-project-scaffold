# Validation contract

`contrib/requirements.json` declares required files and exact rule sentences.
The checker validates presence, non-empty files, marker text, local Markdown links,
UTF-8 text, safe file types, and common secret or personal-email patterns.
It checks required content rather than guessing whether a change is appropriate.
The nine tests deliberately remove a required repository file, remove a rule,
inject a sensitive value, and inspect both empty and populated release archives.
Synthetic scaffold fixtures exist only in temporary test directories.

The default contract protects repository maintenance files and root working rules.
The payload is owner-defined: add its required files and exact rule sentences to
the contract once the owner supplies them. No payload files are required by default.
Until then, Markdown lint, local link checks, text-only restrictions, and local
sensitive-pattern checks exclude `ai-scaffold/`. Arbitrary regular payload files
can be added without imposing a layout or writing style. Packaging still rejects
symlinks to avoid including files outside the payload. GitHub secret scanning and
push protection continue to apply across the repository.

CI runs Markdown, YAML, and Python linters, contract checks, negative tests,
and a ZIP smoke test. A PR also runs the validator and contract from its base commit
against the proposed tree, so deleting a requirement from both the file and the
new manifest does not silently retire an existing requirement. The initial bootstrap
commit predates the contract and is the only allowed missing-contract base.

Workflow files themselves are review-sensitive: an authorized contributor could edit
CI behavior in a PR. Required status checks are not immutable policy enforcement.
Review workflow, validator, and manifest edits carefully. A legitimate retirement of
a required rule needs a separately reviewed policy migration; do not weaken checks
just to make a deletion pass.

Pattern scanning supplements GitHub secret scanning and push protection. Neither
can guarantee detection of every secret. Checks print locations, never matched values.
Commit metadata uses the configured Git identity and is outside content scanning.
