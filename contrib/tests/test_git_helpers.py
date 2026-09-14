"""Exercise Git mutations against disposable local repositories, never GitHub."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class GitHelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        self.remote = self.base / 'origin.git'
        self.repo.mkdir()
        subprocess.run(['git', 'init', '--bare', '-q', str(self.remote)], check=True)
        self.git('init', '-q', '-b', 'main')
        # Synthetic identity applies only to the disposable fixture repository.
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture' + '@' + 'example.invalid')
        (self.repo / '.gitignore').write_text('__pycache__/\n')
        (self.repo / 'contrib').mkdir()
        for name in ('commit-scaffold', 'pr-scaffold', 'scaffold_git.py',
                     'publish-release', 'publish_release.py'):
            shutil.copy2(ROOT / 'contrib' / name, self.repo / 'contrib' / name)
        self.git('add', '.')
        self.git('commit', '-qm', 'Initial fixture')
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', '-q', 'origin', 'main')
        self.git('switch', '-qc', 'develop')
        self.git('push', '-q', 'origin', 'develop')
        self.env = os.environ.copy()
        mock = self.base / 'bin'
        mock.mkdir()
        self.log = self.base / 'gh-calls.jsonl'
        self.env['PATH'] = str(mock) + os.pathsep + self.env['PATH']
        self.env['SCAFFOLD_TEST_LOG'] = str(self.log)
        gh = mock / 'gh'
        gh.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
with open(os.environ['SCAFFOLD_TEST_LOG'], 'a') as log:
    log.write(json.dumps(args) + '\\n')
if args[:2] == ['pr', 'list']:
    print(os.environ.get('SCAFFOLD_TEST_EXISTING', '[]'))
elif args[:2] == ['pr', 'create']:
    body = Path(args[args.index('--body-file') + 1]).read_text()
    Path(os.environ['SCAFFOLD_TEST_LOG'] + '.body').write_text(body)
    print('https://github.com/example/scaffold/pull/1')
elif args[:3] == ['api', '--method', 'PATCH']:
    update = json.loads(Path(args[args.index('--input') + 1]).read_text())
    Path(os.environ['SCAFFOLD_TEST_LOG'] + '.body').write_text(update['body'])
elif args[:2] == ['run', 'list']:
    print('[{"databaseId": 123}]')
elif args[:2] == ['run', 'watch']:
    sys.exit(int(os.environ.get('SCAFFOLD_TEST_RUN_FAILURE', '0')))
elif args[:2] == ['release', 'view']:
    print(json.dumps({'url': 'https://github.com/example/scaffold/releases/tag/' + args[2],
                      'isDraft': False,
                      'assets': [{'name': 'scaffold.zip'}, {'name': 'scaffold.zip.sha256'}]}))
elif args != ['api', 'user', '--silent']:
    sys.exit(2)
''')
        gh.chmod(0o755)

    def git(self, *args, check=True):
        return subprocess.run(['git', *args], cwd=self.repo, check=check,
                              text=True, capture_output=True)

    def helper(self, name, *args):
        return subprocess.run([str(self.repo / 'contrib' / name), *args],
                              cwd=self.base, env=self.env, text=True, capture_output=True)

    def payload(self, text='Owner content'):
        directory = self.repo / 'ai-scaffold'
        directory.mkdir(exist_ok=True)
        (directory / 'notes.md').write_text(text)

    def test_commit_message_scope_and_push(self):
        self.payload()
        (self.repo / 'unrelated.txt').write_text('Leave untracked')
        result = self.helper('commit-scaffold', 'add notes $(literal)')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git('log', '-1', '--format=%s').stdout.strip(),
                         'New scaffold change: add notes $(literal)')
        self.assertEqual(self.git('rev-parse', 'HEAD').stdout,
                         self.git('rev-parse', 'origin/develop').stdout)
        self.assertNotIn('unrelated.txt', self.git('ls-files').stdout)

    def test_reject_wrong_branch_and_unrelated_staged_files(self):
        self.payload()
        self.git('switch', 'main')
        self.assertNotEqual(self.helper('commit-scaffold', 'notes').returncode, 0)
        self.git('switch', 'develop')
        (self.repo / 'unrelated.txt').write_text('Staged maintenance')
        self.git('add', 'unrelated.txt')
        before = self.git('rev-parse', 'HEAD').stdout
        self.assertNotEqual(self.helper('commit-scaffold', 'notes').returncode, 0)
        self.assertEqual(self.git('rev-parse', 'HEAD').stdout, before)
        self.assertEqual(self.git('diff', '--cached', '--name-only').stdout.strip(),
                         'unrelated.txt')

    def test_deletion_and_no_change(self):
        self.payload()
        self.assertEqual(self.helper('commit-scaffold', 'add').returncode, 0)
        shutil.rmtree(self.repo / 'ai-scaffold')
        self.assertEqual(self.helper('commit-scaffold', 'remove').returncode, 0)
        self.assertNotEqual(self.helper('commit-scaffold', 'empty').returncode, 0)

    def test_pr_pushes_commits_and_never_merges_main(self):
        self.payload()
        self.git('add', 'ai-scaffold')
        self.git('commit', '-qm', 'New scaffold change: owner notes')
        main = self.git('rev-parse', 'origin/main').stdout
        result = self.helper('pr-scaffold')
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertTrue(any(call[:2] == ['pr', 'create'] for call in calls))
        self.assertFalse(any(call[:2] == ['pr', 'merge'] for call in calls))
        body = Path(str(self.log) + '.body').read_text()
        for section in ['owner notes', '## Overview', '## Affected files',
                        '## What to review and why', '## Validation and manual merge']:
            self.assertIn(section, body)
        self.assertEqual(self.git('rev-parse', 'origin/main').stdout, main)
        self.assertEqual(self.git('rev-parse', 'origin/develop').stdout,
                         self.git('rev-parse', 'HEAD').stdout)

    def test_reuse_open_pr_and_refuse_dirty_tree(self):
        self.payload()
        self.assertNotEqual(self.helper('pr-scaffold').returncode, 0)
        self.assertEqual(self.helper('commit-scaffold', 'add').returncode, 0)
        self.env['SCAFFOLD_TEST_EXISTING'] = json.dumps([{'url': 'https://github.com/example/scaffold/pull/1', 'number': 1}])
        self.assertEqual(self.helper('pr-scaffold').returncode, 0)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertFalse(any(call[:2] == ['pr', 'create'] for call in calls))
        self.assertTrue(any(call[:3] == ['api', '--method', 'PATCH'] for call in calls))
        self.assertIn('## What to review and why', Path(str(self.log) + '.body').read_text())

    def test_main_update_is_merged_into_develop(self):
        self.payload()
        self.assertEqual(self.helper('commit-scaffold', 'add').returncode, 0)
        self.git('switch', 'main')
        (self.repo / 'maintenance.md').write_text('Remote main update')
        self.git('add', '.')
        self.git('commit', '-qm', 'Main maintenance')
        self.git('push', '-q', 'origin', 'main')
        self.git('switch', 'develop')
        self.assertEqual(self.helper('pr-scaffold').returncode, 0)
        self.assertEqual(self.git('merge-base', '--is-ancestor', 'origin/main', 'HEAD').returncode, 0)

    def test_merge_conflict_restores_clean_tree(self):
        self.payload('Develop version')
        self.assertEqual(self.helper('commit-scaffold', 'add').returncode, 0)
        self.git('switch', 'main')
        self.payload('Main version')
        self.git('add', '.')
        self.git('commit', '-qm', 'Conflicting main update')
        self.git('push', '-q', 'origin', 'main')
        self.git('switch', 'develop')
        before = self.git('rev-parse', 'HEAD').stdout
        self.assertNotEqual(self.helper('pr-scaffold').returncode, 0)
        self.assertEqual(self.git('rev-parse', 'HEAD').stdout, before)
        self.assertEqual(self.git('status', '--porcelain').stdout, '')

    def test_rejected_push_keeps_local_commit(self):
        hook = self.remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        before = self.git('rev-parse', 'origin/develop').stdout
        self.payload()
        result = self.helper('commit-scaffold', 'preserve on rejection')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotEqual(self.git('rev-parse', 'HEAD').stdout, before)
        self.assertEqual(self.git('rev-parse', 'origin/develop').stdout, before)
        self.assertIn('local commits remain', result.stderr)

    def test_release_defaults_to_patch_and_reuses_existing_release(self):
        target = self.git('rev-parse', 'origin/main').stdout.strip()
        # Develop-only commits must never become the release target.
        self.payload()
        self.assertEqual(self.helper('commit-scaffold', 'unmerged').returncode, 0)
        result = self.helper('publish-release')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git('rev-parse', 'v0.0.1^{commit}').stdout.strip(), target)
        self.assertIn('refs/tags/v0.0.1', self.git('ls-remote', '--tags', 'origin').stdout)
        self.assertEqual(self.git('branch', '--show-current').stdout.strip(), 'develop')
        result = self.helper('publish-release')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git('tag').stdout.strip(), 'v0.0.1')
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertIn(['run', 'watch', '123', '--exit-status'], calls)

    def test_release_minor_major_and_numeric_version_order(self):
        for bump, expected in [('minor', 'v1.11.0'), ('major', 'v2.0.0')]:
            with self.subTest(bump=bump):
                for tag in ('v1.9.0', 'v1.10.3'):
                    self.git('tag', tag, 'origin/main')
                    self.git('push', '-q', 'origin', tag)
                self.git('commit', '--allow-empty', '-qm', 'Merged change')
                self.git('push', '-q', 'origin', 'HEAD:main')
                result = self.helper('publish-release', bump)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.git('rev-parse', expected + '^{commit}').stdout,
                                 self.git('rev-parse', 'origin/main').stdout)
                for tag in ('v1.9.0', 'v1.10.3', expected):
                    self.git('push', '-q', 'origin', '--delete', tag)
                    self.git('tag', '-d', tag)

    def test_release_refuses_dirty_tree_wrong_branch_and_invalid_bump(self):
        self.assertNotEqual(self.helper('publish-release', 'bogus').returncode, 0)
        self.git('switch', 'main')
        self.assertNotEqual(self.helper('publish-release').returncode, 0)
        self.git('switch', 'develop')
        self.payload()
        self.assertNotEqual(self.helper('publish-release').returncode, 0)
        self.assertEqual(self.git('tag').stdout, '')

    def test_release_push_failure_preserves_tag_and_blocks_duplicate(self):
        hook = self.remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        result = self.helper('publish-release')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git('tag').stdout.strip(), 'v0.0.1')
        self.assertEqual(self.git('ls-remote', '--tags', 'origin').stdout, '')
        result = self.helper('publish-release')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Local tag v0.0.1 already exists', result.stderr)

    def test_release_reports_workflow_failure_without_new_tag_on_retry(self):
        self.env['SCAFFOLD_TEST_RUN_FAILURE'] = '1'
        self.assertNotEqual(self.helper('publish-release').returncode, 0)
        self.assertNotEqual(self.helper('publish-release').returncode, 0)
        self.assertEqual(self.git('tag').stdout.strip(), 'v0.0.1')
