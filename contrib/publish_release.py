"""Publish merged scaffold changes using the existing release workflow."""
import argparse
import json
import re
import subprocess
import sys
import time

from scaffold_git import git, require_develop, run

VERSION = re.compile(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)')


def next_version(version, bump):
    parts = list(version)
    index = ('major', 'minor', 'patch').index(bump)
    parts[index] += 1
    parts[index + 1:] = [0] * (2 - index)
    return 'v' + '.'.join(map(str, parts))


def wait_for_release(tag, target):
    print(f'Waiting for {tag}. If interrupted, rerun this helper to check the release.',
          flush=True)
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        runs = json.loads(run('gh', 'run', 'list', '--workflow', 'release.yml',
                              '--branch', tag, '--commit', target, '--event', 'push',
                              '--limit', '1', '--json', 'databaseId', capture=True).stdout)
        if runs:
            run('gh', 'run', 'watch', str(runs[0]['databaseId']), '--exit-status')
            release = json.loads(run('gh', 'release', 'view', tag, '--json',
                                     'url,isDraft,assets', capture=True).stdout)
            assets = {asset['name'] for asset in release['assets']}
            if release['isDraft'] or not {'scaffold.zip', 'scaffold.zip.sha256'} <= assets:
                raise ValueError(f'{tag} is missing published ZIP assets.')
            print(f"Published: {release['url']}")
            return
        time.sleep(3)
    raise ValueError(f'No release workflow appeared for {tag} within 120 seconds. '
                     'Check GitHub Actions; rerun this helper after resolving the issue.')


def publish_release(bump):
    require_develop()
    if git('status', '--porcelain', capture=True).stdout.strip():
        raise ValueError('Commit or stash pending changes before publishing a release.')
    run('gh', 'api', 'user', '--silent')
    git('fetch', 'origin', '+refs/heads/main:refs/remotes/origin/main', '--tags')
    target = git('rev-parse', 'origin/main', capture=True).stdout.strip()
    # Only remote version tags count; unpublished local tags must not advance versions.
    refs = git('ls-remote', '--tags', '--refs', 'origin', capture=True).stdout
    versions = []
    for line in refs.splitlines():
        tag = line.split()[1].removeprefix('refs/tags/')
        match = VERSION.fullmatch(tag)
        if match:
            versions.append((tuple(map(int, match.groups())), tag))
    version, latest = max(versions) if versions else ((0, 0, 0), None)
    if latest:
        previous = git('rev-parse', f'refs/tags/{latest}^{{commit}}', capture=True).stdout.strip()
        if previous == target:
            print(f'origin/main already has {latest}; checking its publication.', flush=True)
            wait_for_release(latest, target)
            return
        if git('merge-base', '--is-ancestor', previous, target, check=False).returncode:
            raise ValueError(f'Latest version {latest} is not an ancestor of origin/main.')
    tag = next_version(version, bump)
    if git('show-ref', '--verify', '--quiet', f'refs/tags/{tag}', check=False).returncode == 0:
        raise ValueError(f'Local tag {tag} already exists. Inspect it and resolve the '
                         'previous push before retrying; no tag will be overwritten.')
    print(f'Publishing {tag} from origin/main ({target[:12]}).', flush=True)
    git('tag', '-a', tag, target, '-m', f'Release {tag}')
    print(f'Created {tag}. If pushing fails, inspect it and retry: '
          f'git push origin refs/tags/{tag}', flush=True)
    git('push', 'origin', f'refs/tags/{tag}')
    wait_for_release(tag, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bump', nargs='?', choices=('patch', 'minor', 'major'), default='patch',
                        help='version component to increment (default: patch)')
    args = parser.parse_args()
    try:
        publish_release(args.bump)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'Error: {error}', file=sys.stderr)
        print('Existing tags are never moved or deleted. If the workflow failed, '
              'inspect and rerun it in GitHub Actions.', file=sys.stderr)
        raise SystemExit(1) from None
