"""Negative contract tests and release archive integration tests."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from package import package  # noqa: E402
from validate import ROOT, tracked_files, validate  # noqa: E402


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        for relative in tracked_files(ROOT):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', '.'], check=True)
        self.contract = json.loads((self.root / 'contrib/requirements.json').read_text())

    def clear_scaffold(self):
        subprocess.run(['git', '-C', str(self.root), 'rm', '-r', '-f',
                        '--ignore-unmatch', 'ai-scaffold'], check=True, capture_output=True)
        shutil.rmtree(self.root / 'ai-scaffold', ignore_errors=True)

    def test_empty_scaffold_archive(self):
        self.clear_scaffold()
        output = Path(self.temp.name) / 'empty-dist'
        archive = package(self.root, output)
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(bundle.namelist(), ['ai-scaffold/'])
            self.assertTrue(bundle.getinfo('ai-scaffold/').is_dir())
            extracted = Path(self.temp.name) / 'empty-extract'
            bundle.extractall(extracted)
            self.assertTrue((extracted / 'ai-scaffold').is_dir())
            self.assertEqual(list((extracted / 'ai-scaffold').iterdir()), [])

    def test_current_contract(self):
        self.assertEqual(validate(self.root, self.contract), [])

    def test_missing_key_file(self):
        (self.root / 'AGENTS.md').unlink()
        self.assertTrue(validate(self.root, self.contract))

    def test_removed_rule_even_if_new_contract_is_weakened(self):
        key = 'AGENTS.md'
        marker = self.contract['required_files'][key][0]
        path = self.root / key
        path.write_text(path.read_text().replace(marker, ''))
        altered = json.loads(json.dumps(self.contract))
        altered['required_files'][key] = []
        (self.root / 'contrib/requirements.json').write_text(json.dumps(altered))
        self.assertTrue(any('required rule missing' in e for e in validate(self.root, self.contract)))

    def test_sensitive_values_are_rejected_without_echo(self):
        for value in ['person' + '@' + 'example.invalid', 'ghp_' + 'A' * 36,
                      'password' + '=' + 'synthetic-value-123']:
            path = self.root / 'docs/SECURITY.md'
            path.write_text(path.read_text() + '\n' + value)
            errors = validate(self.root, self.contract)
            self.assertTrue(any('possible' in e for e in errors))
            self.assertNotIn(value, '\n'.join(errors))

    def test_broken_local_link(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text() + '\n[Missing](does-not-exist.md)\n')
        self.assertTrue(any('link' in e for e in validate(self.root, self.contract)))

    def test_symlink_rejected(self):
        path = self.root / 'docs/SECURITY.md'
        path.unlink()
        path.symlink_to('VALIDATION.md')
        self.assertTrue(validate(self.root, self.contract))

    def test_archive_exact_tree_hidden_files_and_reproducibility(self):
        self.clear_scaffold()
        for name in ['ai-scaffold/owner-notes.md', 'ai-scaffold/.gitignore',
                     'ai-scaffold/.github/README.md']:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# Synthetic packaging fixture\n')
        subprocess.run(['git', '-C', str(self.root), 'add', 'ai-scaffold'], check=True)
        (self.root / 'ai-scaffold/untracked.txt').write_text('Must not ship')
        output = Path(self.temp.name) / 'dist'
        archive = package(self.root, output)
        original = archive.read_bytes()
        with zipfile.ZipFile(archive) as bundle:
            expected = {p.as_posix() for p in tracked_files(self.root) if p.parts[0] == 'ai-scaffold'}
            self.assertEqual(set(bundle.namelist()), expected | {'ai-scaffold/'})
            self.assertIn('ai-scaffold/.gitignore', bundle.namelist())
            self.assertIn('ai-scaffold/.github/README.md', bundle.namelist())
            self.assertIsNone(bundle.testzip())
            extracted = Path(self.temp.name) / 'extract'
            bundle.extractall(extracted)
            for name in expected:
                self.assertEqual((extracted / name).read_bytes(), (self.root / name).read_bytes())
        self.assertEqual(package(self.root, output).read_bytes(), original)
        checksum = (output / 'scaffold.zip.sha256').read_text().split()[0]
        self.assertEqual(checksum, hashlib.sha256(original).hexdigest())


if __name__ == '__main__':
    unittest.main()
