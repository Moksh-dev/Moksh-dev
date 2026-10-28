"""Refresh only marked README regions from GitHub's public repository API."""
import argparse
from collections import Counter
import html
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'Moksh-dev'
API = 'https://api.github.com'

def get_json(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Moksh-dev-profile',
               'X-GitHub-Api-Version': '2022-11-28'}
    token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    for attempt in range(3):
        try:
            with urlopen(Request(API + path, headers=headers), timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(min(int(error.headers.get('Retry-After', '3')), 30))
                continue
            raise RuntimeError(f'GitHub API returned HTTP {error.code}; README was not changed.') from error
    raise RuntimeError('GitHub API unavailable')

def discover(fetch=get_json):
    repos, page = [], 1
    # Continue through the empty page; never assume a single response is complete.
    while True:
        batch = fetch(f'/users/{OWNER}/repos?type=owner&sort=full_name&per_page=100&page={page}')
        if not isinstance(batch, list):
            raise ValueError('Expected a repository list')
        if not batch:
            break
        repos.extend(batch)
        page += 1
        if page > 1000:
            raise ValueError('Unexpected pagination loop')
    repos = [r for r in repos if not r.get('private', False)
             and r['owner']['login'].lower() == OWNER.lower()]
    names = [r['name'].lower() for r in repos]
    if not repos or len(names) != len(set(names)):
        raise ValueError('Empty or duplicate discovery result; refusing to overwrite')
    profile = fetch(f'/users/{OWNER}')
    if profile['public_repos'] != len(repos):
        raise ValueError('Public repository count changed or discovery is incomplete; retry later')
    return repos

def safe(value):
    value = ' '.join(str(value or '').split())
    value = html.escape(value, quote=True)
    # Repository descriptions are untrusted Markdown, never executable markup.
    return re.sub(r'([\\`*_{}\[\]()#+.!|~])', r'\\\1', value)

def region(text, name, content):
    start, end = f'<!-- {name}:START -->', f'<!-- {name}:END -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f'Expected exactly one {name} marker pair')
    a, b = text.index(start) + len(start), text.index(end)
    if b < a:
        raise ValueError(f'Reversed {name} markers')
    return text[:a] + '\n\n' + content.strip() + '\n\n' + text[b:]

def render_index(repos, curated):
    groups = {}
    for repo in repos:
        name = repo['name']
        entry = curated.get(name, {})
        category = entry.get('category', 'Experiments / Newly discovered')
        description = entry.get('description') or repo.get('description')
        if not description:
            description = (f"{repo['language']} repository; project description not provided."
                           if repo.get('language') else 'Public repository; project description not provided.')
        tech = entry.get('technologies') or repo.get('language') or 'Not reported by GitHub'
        # Only API-validated repository names are used to construct links.
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', name):
            raise ValueError('Invalid repository name')
        status = ' (archived)' if repo.get('archived') else ''
        status += ' (fork)' if repo.get('fork') else ''
        row = f'| [{safe(name)}](https://github.com/{OWNER}/{name}){status} | {safe(description)} | {safe(tech)} |'
        groups.setdefault(category, []).append((name.lower(), row))
    lines = [f'**{len(repos)} public repositories** · refreshed automatically from GitHub.']
    for category, rows in sorted(groups.items()):
        lines += ['', f'### {safe(category)}', '', '| Repository | What it does | Technologies |',
                  '| :--- | :--- | :--- |'] + [row for _, row in sorted(rows)]
    return '\n'.join(lines)

def render_activity(repos):
    projects = [r for r in repos if r['name'].lower() != OWNER.lower()]
    languages = Counter(r['language'] for r in projects if r.get('language'))
    language_text = ' · '.join(f'{safe(k)} {v}' for k,v in sorted(languages.items(), key=lambda x:(-x[1], x[0])))
    latest = max((r.get('pushed_at') or '' for r in projects), default='')[:10] or 'Not available'
    return (f'**{len(repos)} public repositories** &nbsp; / &nbsp; **{len(projects)} projects**\n\n'
            f'Latest project push: **{latest}** (UTC).\n\n'
            f'Primary language by project count: {language_text or "Not reported"}.\n\n'
            '<sub>Source: GitHub repository metadata. One primary language per project; '
            'these counts are not a proficiency score. The profile repository is excluded from project activity.</sub>')

def update(text, repos, curated):
    # Compute both replacements before writing anything; malformed markers fail closed.
    return region(region(text, 'REPOSITORIES', render_index(repos, curated)),
                  'ACTIVITY', render_activity(repos))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, help='Use an audited local API snapshot instead of the network')
    parser.add_argument('--check', action='store_true', help='Exit 1 if generated sections need updating')
    args = parser.parse_args()
    repos = json.loads(args.snapshot.read_text(encoding='utf-8-sig')) if args.snapshot else discover()
    if not repos:
        raise ValueError('Refusing an empty snapshot')
    curated = json.loads((ROOT/'scripts/curated.json').read_text(encoding='utf-8'))
    target = ROOT/'README.md'
    before = target.read_text(encoding='utf-8')
    after = update(before, repos, curated)
    if args.check:
        raise SystemExit(0 if before == after else 1)
    if before != after:
        temporary = target.with_suffix('.md.tmp')
        temporary.write_text(after, encoding='utf-8', newline='\n')
        temporary.replace(target)
        print(f'Updated {len(repos)} public repositories')
    else:
        print('No changes')

if __name__ == '__main__':
    main()
