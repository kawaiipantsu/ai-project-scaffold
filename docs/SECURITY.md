# Security and privacy

Never commit secrets, passwords, access tokens, personal email addresses, private
keys, production data, or confidential logs. Use synthetic examples and environment
variables. Keep local credentials outside the tracked tree.

GitHub secret scanning and push protection are enabled. Required CI adds a local
pattern check. Before publishing, inspect the staged diff and run validation.
If a real secret is exposed, revoke or rotate it first, then follow the provider's
incident process and remove it from history where appropriate. Avoid reproducing the
secret in issues, PRs, screenshots, wiki pages, or logs.

Report security concerns through GitHub private vulnerability reporting when enabled
on the repository Security tab. Do not open a public issue containing sensitive data.
