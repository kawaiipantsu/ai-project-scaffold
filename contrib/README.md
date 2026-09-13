# Maintenance tools

Run tools from the repository root with Python 3.12 or newer.

- `validate.py`: check required structure, rule text, links, and sensitive patterns.
- `requirements.json`: explicit minimum content contract.
- `package.py`: build the tracked scaffold ZIP and SHA-256 checksum in `dist/`.
- `tests/`: regression and negative tests for validation and packaging.

Development lint dependencies are pinned in `requirements-dev.txt`.
