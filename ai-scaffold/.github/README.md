# GitHub setup notes

Create develop and main branches. Require pull requests and passing checks on main.
Disable force pushes, branch deletion, squash merges, and rebase merges to preserve
individual commits. Enable secret scanning and push protection where supported.

Add technology-specific CI after selecting the stack. Require meaningful lint, test,
and build jobs; do not use a successful placeholder job as proof of correctness.
Configure repository permissions and release credentials with least privilege.
