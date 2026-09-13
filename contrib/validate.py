#!/usr/bin/env python3
"""Validate the scaffold contract without printing sensitive matched content."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'email address': re.compile(r'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b'),
    'private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'provider token': re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9]{32,})'),
    'credential assignment': re.compile(r'''(?im)^\s*(?:password|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*["']?(?!TBD\b|PLACEHOLDER\b|\$|<)[A-Za-z0-9/+_=.-]{8,}'''),
}


def tracked_files(root):
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'],
                            check=True, capture_output=True)
    return [Path(p.decode()) for p in result.stdout.split(b'\0') if p]


def validate(root, contract):
    errors = []
    for name, markers in contract['required_files'].items():
        path = root / name
        if not path.is_file() or path.is_symlink():
            errors.append(f'{name}: required regular file missing')
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'{name}: invalid UTF-8')
            continue
        if not content.strip():
            errors.append(f'{name}: required file is empty')
        for marker in markers:
            if marker not in content:
                errors.append(f'{name}: required rule missing (index {markers.index(marker)})')
    for relative in tracked_files(root):
        path = root / relative
        if not path.exists():
            errors.append(f'{relative}: tracked file missing')
            continue
        if path.is_symlink() or not path.is_file():
            errors.append(f'{relative}: only regular files are allowed')
            continue
        if relative.name.startswith('.env') and relative.name != '.env.example':
            errors.append(f'{relative}: environment file is prohibited')
        if path.suffix.lower() in {'.pem', '.key', '.p12', '.pfx'}:
            errors.append(f'{relative}: credential file type is prohibited')
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'{relative}: binary files require an explicit policy review')
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                errors.append(f'{relative}: possible {label}; inspect privately')
        if path.suffix == '.md':
            for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', content):
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                destination = (path.parent / unquote(target.split('#')[0])).resolve()
                if not destination.is_relative_to(root.resolve()) or not destination.exists():
                    errors.append(f'{relative}: local Markdown link does not resolve')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--contract', type=Path)
    args = parser.parse_args()
    contract_path = args.contract or args.root / 'contrib/requirements.json'
    contract = json.loads(contract_path.read_text())
    errors = validate(args.root, contract)
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print('Scaffold contract, links, and sensitive-content checks passed.')


if __name__ == '__main__':
    main()
