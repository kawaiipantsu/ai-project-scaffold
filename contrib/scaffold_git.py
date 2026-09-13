"""Small Git helpers for the develop-to-main scaffold workflow."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args, capture=False, check=True):
    return subprocess.run(args, cwd=ROOT, text=True, check=check,
                          stdout=subprocess.PIPE if capture else None)


def git(*args, capture=False, check=True):
    return run('git', *args, capture=capture, check=check)


def require_develop():
    if git('branch', '--show-current', capture=True).stdout.strip() != 'develop':
        raise ValueError('Switch to develop first: git switch develop')


def commit_scaffold(note):
    if not note.strip() or '\n' in note or '\r' in note:
        raise ValueError('Supply one non-empty, single-line change note.')
    require_develop()
    staged = git('diff', '--cached', '--name-only', '-z', capture=True).stdout.split('\0')
    if any(name and not name.startswith('ai-scaffold/') for name in staged):
        raise ValueError('Unstage changes outside ai-scaffold/ before using this helper.')
    # Only stage the payload, including deletions; a never-populated folder is valid.
    tracked = git('ls-files', '--', 'ai-scaffold/', capture=True).stdout
    if (ROOT / 'ai-scaffold').exists() or tracked:
        git('add', '-A', '--', 'ai-scaffold/')
    if git('diff', '--cached', '--quiet', check=False).returncode == 0:
        raise ValueError('No scaffold changes to commit.')
    git('commit', '-m', f'New scaffold change: {note.strip()}')
    git('push', '--set-upstream', 'origin', 'develop')


def pr_scaffold():
    require_develop()
    if git('status', '--porcelain', capture=True).stdout.strip():
        raise ValueError('Commit or stash pending changes before preparing a PR.')
    run('gh', 'api', 'user', '--silent')
    git('fetch', 'origin', 'main', 'develop')
    # Preserve individual commits when remote develop or main has moved forward.
    for branch in ('origin/develop', 'origin/main'):
        result = git('merge', '--no-edit', branch, check=False)
        if result.returncode:
            git('merge', '--abort', check=False)
            raise ValueError(f'Could not merge {branch}; resolve it manually and rerun.')
    if not git('rev-list', 'origin/main..HEAD', capture=True).stdout.strip():
        print('No commits to propose: develop is already included in main.')
        return
    git('push', '--set-upstream', 'origin', 'develop')
    existing = json.loads(run('gh', 'pr', 'list', '--base', 'main', '--head', 'develop',
                              '--state', 'open', '--json', 'url,number', capture=True).stdout)
    commits = git('log', '--reverse', '--format=- %h %s', 'origin/main..HEAD',
                  capture=True).stdout
    changes = git('diff', '--stat', 'origin/main...HEAD', capture=True).stdout
    files = git('diff', '--name-status', 'origin/main...HEAD', capture=True).stdout
    body = ('## Overview\n\n'
            'Proposes the commits on `develop` that are not yet in `main`. '
            'The change notes below describe the author’s intent; review the diff '
            'against those notes before merging.\n\n'
            '## Change notes\n\n' + commits + '\n'
            '## Affected files\n\n```text\n' + files + '```\n\n'
            '## Diff summary\n\n```text\n' + changes + '```\n\n'
            '## What to review and why\n\n'
            '- [ ] Confirm each change matches its note and the desired scaffold. '
            'These files become the starting point for future projects.\n'
            '- [ ] Inspect added, renamed, and deleted files. Check hidden files and '
            'release contents so required material is not accidentally lost.\n'
            '- [ ] Review any AI instructions, requirements, or prompts for intended '
            'behavior. They influence how consuming projects are built.\n'
            '- [ ] Check for credentials, personal data, and private logs before '
            'publishing reusable files.\n'
            '- [ ] Review maintenance or automation changes, if present, for effects '
            'on validation, packaging, and branch protection.\n\n'
            '## Validation and manual merge\n\n'
            '- [ ] Required GitHub Actions checks pass for the latest commit.\n'
            '- [ ] Manually review payload content: payload lint and required-content '
            'policy are currently deferred, so green CI does not validate its meaning.\n'
            '- [ ] Resolve review feedback, then merge manually on GitHub with a merge '
            'commit to preserve individual history.\n\n'
            'This helper pushes develop and prepares the PR; it does not approve, '
            'merge, or enable auto-merge. Rerunning it refreshes this description.\n')
    with tempfile.TemporaryDirectory(prefix='scaffold-pr-') as directory:
        if existing:
            path = Path(directory) / 'update.json'
            path.write_text(json.dumps({'title': 'Scaffold changes', 'body': body}))
            run('gh', 'api', '--method', 'PATCH',
                'repos/{owner}/{repo}/pulls/' + str(existing[0]['number']),
                '--input', str(path), '--silent')
            print(f"Updated PR: {existing[0]['url']}")
        else:
            path = Path(directory) / 'body.md'
            path.write_text(body)
            run('gh', 'pr', 'create', '--base', 'main', '--head', 'develop',
                '--title', 'Scaffold changes', '--body-file', str(path))


def main(command):
    try:
        if command == 'commit' and len(sys.argv) == 2:
            commit_scaffold(sys.argv[1])
        elif command == 'pr' and len(sys.argv) == 1:
            pr_scaffold()
        else:
            raise ValueError('Usage: contrib/commit-scaffold "<change note>" '
                             'or contrib/pr-scaffold')
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'Error: {error}', file=sys.stderr)
        print('No history is force-pushed. If a push failed, local commits remain; '
              'resolve the remote divergence before retrying the push.', file=sys.stderr)
        raise SystemExit(1) from None
