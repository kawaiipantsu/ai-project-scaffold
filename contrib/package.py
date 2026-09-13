#!/usr/bin/env python3
"""Build a reproducible ZIP of the tracked ai-scaffold tree."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from validate import ROOT, tracked_files, validate


def package(root, output):
    errors = validate(root, json.loads((root / 'contrib/requirements.json').read_text()))
    if errors:
        raise ValueError('\n'.join(errors))
    files = sorted(p for p in tracked_files(root) if p.parts[0] == 'ai-scaffold')
    output.mkdir(parents=True, exist_ok=True)
    archive = output / 'scaffold.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        directory = zipfile.ZipInfo('ai-scaffold/', date_time=(2020, 1, 1, 0, 0, 0))
        directory.create_system = 3
        directory.external_attr = (0o40755 << 16) | 0x10
        bundle.writestr(directory, b'')
        for path in files:
            if (root / path).is_symlink() or not (root / path).is_file():
                raise ValueError('Payload archive entries must be regular files')
            info = zipfile.ZipInfo(path.as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, (root / path).read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / 'scaffold.zip.sha256').write_text(f'{digest}  scaffold.zip\n')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    print(f'Built {package(ROOT, args.output).name} and SHA-256 checksum.')
