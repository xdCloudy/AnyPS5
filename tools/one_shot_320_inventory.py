#!/usr/bin/env python3
"""Inventory PS5 3.20 callable exports without modifying AnyPS5 source files."""

import argparse
import collections
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

NID = r"[A-Za-z0-9+\-]{11}"
DLSYM = re.compile(r'\bsprx_dlsym\s*\(\s*__handle\s*,\s*"(' + NID + r')"\s*,\s*&__ptr_([A-Za-z_]\w*)\s*\)')
ALL_DLSYM = re.compile(r'\bsprx_dlsym\s*\(\s*__handle\s*,')
NAME = re.compile(r'^[A-Za-z_]\w*$')
ALIAS = re.compile(r'\bAPS5_EXPORT\s*\(\s*"(' + NID + r')"\s*,')
FUNCTION = re.compile(r'\bAPS5_VABI\s+([A-Za-z_]\w*)\s*\(')
ASM = re.compile(r'\bAPS5_(?:SIGNAL_)?ASM_FUNCTION\s*\(\s*"([A-Za-z_]\w*)"')
UNSAFE = re.compile(r'\bAPS5_(?:EXPORT|VABI|ASM_FUNCTION|SIGNAL_ASM_FUNCTION)\b')
LIBRARY = re.compile(r'^core/libs/prx/([^/]+)/')


def load_nid_module(repo):
    path = repo / 'tools' / 'nid_names.py'
    spec = importlib.util.spec_from_file_location('anyps5_nid_names_oneshot', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_inventory(root, compute_nid):
    if not root.is_dir():
        raise ValueError(f'inventory folder not found: {root}')
    records = {}
    counts = collections.Counter()
    files = sorted(root.glob('*.c'))
    if not files:
        raise ValueError(f'no 3.20 .c files in {root}')
    for path in files:
        source = path.read_text(encoding='utf-8')
        matches = list(DLSYM.finditer(source))
        if len(matches) != len(ALL_DLSYM.findall(source)):
            raise ValueError(f'unsupported sprx_dlsym syntax in {path.name}: matched {len(matches)} of {len(ALL_DLSYM.findall(source))}')
        module = path.stem
        for match in matches:
            nid, name = match.groups()
            key = (module, nid)
            counts['observations'] += 1
            if key in records:
                if records[key]['name'] != name:
                    raise ValueError(f'conflicting names for {module}/{nid}')
                counts['duplicates'] += 1
                continue
            records[key] = dict(module=module, nid=nid, name=name, source=path.name,
                                name_verified=(bool(NAME.fullmatch(name)) and compute_nid(name) == nid))
    if not records:
        raise ValueError('3.20 inventory contains no callable exports')
    return records, counts, len(files)


def existing_exports(repo, nid_module):
    """Index direct exports; mark unknown expansion providers for manual review."""
    providers = collections.defaultdict(set)
    risk_providers = set()
    lib_root = repo / 'core' / 'libs' / 'prx'
    if not lib_root.is_dir():
        raise ValueError(f'AnyPS5 PRX folder missing: {lib_root}')
    for path in sorted((repo / 'core' / 'libs').rglob('*.cpp')):
        if 'tests' in path.parts or 'test' in path.parts:
            continue
        source = path.read_text(encoding='utf-8', errors='replace')
        rel = path.relative_to(repo).as_posix()
        m = LIBRARY.match(rel)
        owner = m.group(1) if m else None
        for nid, _ in nid_module.source_aliases(source):
            providers[nid].add(owner or rel)
        for match in nid_module.source_definitions(source):
            name = nid_module.strip_nid_postfix(match.group(1))
            if name.endswith(('_nid_no_patch', '_nid_no_patch_cut')):
                continue
            providers[nid_module.compute_nid(name)].add(owner or rel)
        for name in nid_module.source_assembly_definitions(source):
            providers[nid_module.compute_nid(nid_module.strip_nid_postfix(name))].add(owner or rel)
        # Macro-generated exports and other unexpanded patterns cannot be disproved by a text scan.
        if owner and (re.search(r'^\s*#\s*define\s+\w+\([^\n]+', source, re.M)
                      and re.search(r'\bAPS5_(?:VABI|EXPORT|ASM_FUNCTION|SIGNAL_ASM_FUNCTION)\b', source)):
            risk_providers.add(owner)
    return providers, risk_providers, {p.name for p in lib_root.iterdir() if p.is_dir()}


class GitHubAPI:
    def __init__(self, token, repo):
        self.token = token
        self.repo = repo
        self.requests = 0

    def request(self, route):
        url = 'https://api.github.com/' + route.lstrip('/')
        headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28',
                   'User-Agent': 'AnyPS5-one-shot-3.20-import'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as resp:
            self.requests += 1
            return json.load(resp)

    def open_pr_files(self):
        """Fetch all open PR patches, aborting on incomplete pagination."""
        pulls = []
        page = 1
        while True:
            chunk = self.request(f'repos/{self.repo}/pulls?state=open&base=main&per_page=100&page={page}')
            if not isinstance(chunk, list):
                raise ValueError('unexpected GitHub PR list response')
            pulls.extend(chunk)
            if len(chunk) < 100:
                break
            page += 1
            if page > 100:
                raise ValueError('too many PR pages; aborting safely')

        def load_files(pr):
            number = pr['number']
            files = []
            file_page = 1
            while True:
                part = self.request(f'repos/{self.repo}/pulls/{number}/files?per_page=100&page={file_page}')
                if not isinstance(part, list):
                    raise ValueError(f'bad file list for PR #{number}')
                files.extend(part)
                if len(part) < 100:
                    break
                file_page += 1
                if file_page > 30:
                    raise ValueError(f'PR #{number} has too many changed files; aborting safely')
            return number, files

        # Bounded concurrency avoids thousands of serial network round trips.
        with ThreadPoolExecutor(max_workers=5) as executor:
            yield from executor.map(load_files, pulls)


def pending_exports(api, compute_nid, relevant_modules):
    """Index NIDs from added export lines, and library changes that cannot be ruled out."""
    claimed = collections.defaultdict(set)
    uncertain = collections.defaultdict(set)
    scanned = 0
    for number, files in api.open_pr_files():
        scanned += 1
        for file in files:
            path = file.get('filename', '')
            m = LIBRARY.match(path)
            module = m.group(1) if m else None
            if not module or module not in relevant_modules:
                continue
            patch = file.get('patch')
            if not isinstance(patch, str) or file.get('status') in ('renamed', 'removed'):
                uncertain[module].add(number)
                continue
            added = '\n'.join(line[1:] for line in patch.splitlines() if line.startswith('+') and not line.startswith('+++'))
            nids = set(ALIAS.findall(added))
            for name in FUNCTION.findall(added):
                if not name.endswith(('_nid_no_patch', '_nid_no_patch_cut')):
                    nids.add(compute_nid(re.sub(r'_nid_disambig\d+$', '', name.removesuffix('_nid_postfix'))))
            for name in ASM.findall(added):
                nids.add(compute_nid(name))
            for nid in nids:
                claimed[(module, nid)].add(number)
            if (UNSAFE.search(added) and not nids) or file.get('changes', 0) > len(patch.splitlines()):
                uncertain[module].add(number)
            if re.search(r'^\s*#\s*define\b', added, re.M):
                uncertain[module].add(number)
    return claimed, uncertain, scanned


def write_report(out, records, source_counts, file_count, existing, macro_risk, available_modules, claimed,
                 uncertain, scanned, api_requests, batch_size, repo_sha, source_sha):
    out.mkdir(parents=True, exist_ok=True)
    statuses = collections.Counter()
    module_summaries = collections.defaultdict(collections.Counter)
    batches = collections.defaultdict(list)
    report = []
    for (module, nid), entry in sorted(records.items()):
        state = None
        reason = None
        if not entry['name_verified']:
            state, reason = 'invalid_identity', 'NID does not match computed symbol hash'
        elif nid in existing:
            state, reason = 'already_present', ', '.join(sorted(existing[nid]))
        elif claimed.get((module, nid)):
            state, reason = 'pending_pr', ', '.join(f'#{n}' for n in sorted(claimed[(module, nid)]))
        elif module not in available_modules:
            state, reason = 'needs_review', 'no same-name PRX provider; confirm module ownership before generation'
        elif module in macro_risk:
            state, reason = 'needs_review', 'macro-defined exports cannot be fully expanded by source scan'
        elif uncertain.get(module):
            state, reason = 'needs_review', 'relevant open PR had unparseable or ambiguous changes: ' + ', '.join(f'#{n}' for n in sorted(uncertain[module])[:15])
        elif not module.startswith('lib'):
            state, reason = 'needs_review', 'nonstandard provider requires manual module mapping'
        else:
            state, reason = 'candidate', 'verified name and NID; no detected main/open-PR overlap'
        entry = {**entry, 'status': state, 'reason': reason}
        report.append(entry)
        statuses[state] += 1
        module_summaries[module][state] += 1
        if state == 'candidate':
            batches[module].append(entry)
    files_written = 0
    for module, entries in sorted(batches.items()):
        # Only writing NID input lists; no unverified declarations enter the source tree.
        for offset in range(0, len(entries), batch_size):
            batch = entries[offset:offset + batch_size]
            filename = f'{module}-{offset // batch_size + 1:03d}'
            target = out / 'batches'
            target.mkdir(exist_ok=True)
            (target / f'{filename}.nids').write_text('\n'.join(row['nid'] for row in batch) + '\n', encoding='utf-8')
            (target / f'{filename}.json').write_text(json.dumps(batch, indent=2) + '\n', encoding='utf-8')
            files_written += 1
    summary = {'source': 'DNNDHH/PS5-3.20_Libs', 'source_commit': source_sha,
               'target': 'boykopovar/AnyPS5', 'target_commit': repo_sha,
               'source_files': file_count, 'unique_exports': len(records),
               'raw_observations': source_counts['observations'],
               'duplicate_observations': source_counts['duplicates'], 'open_prs_checked': scanned,
               'api_requests': api_requests, 'status_counts': dict(sorted(statuses.items())),
               'candidate_batches': files_written, 'batch_size_limit': batch_size}
    (out / 'inventory.json').write_text(json.dumps({'summary': summary, 'exports': report}, indent=2) + '\n', encoding='utf-8')
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    lines = ['# One-time PS5 3.20 export inventory', '',
             f"Source: `DNNDHH/PS5-3.20_Libs@{source_sha}`",
             f"Target: `boykopovar/AnyPS5@{repo_sha}`", '',
             '**Read-only report. No stubs, source edits, or PRs were automatically submitted.**', '',
             '| Classification | Functions |', '|---|---:|']
    for key, value in sorted(statuses.items()):
        lines.append(f'| {key} | {value} |')
    lines += ['', f'Open PRs checked: {scanned}. Candidate batch files: {files_written}.', '',
              'Candidate means name/NID matched and no overlap was detected in this snapshot. It does not establish ABI, behaviour, or acceptance upstream.',
              'Run `tools/pr_overlap.py` again against current upstream immediately before opening each implementation PR.', '',
              '## Modules', '', '| Module | Total | Candidate | Pending PR | Already | Review | Invalid |',
              '|---|---:|---:|---:|---:|---:|---:|']
    for module, counts in sorted(module_summaries.items()):
        lines.append(f"| `{module}` | {sum(counts.values())} | {counts['candidate']} | {counts['pending_pr']} | {counts['already_present']} | {counts['needs_review']} | {counts['invalid_identity']} |")
    (out / 'summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--upstream', default='boykopovar/AnyPS5')
    parser.add_argument('--batch-size', type=int, default=150)
    parser.add_argument('--repo-sha', required=True)
    parser.add_argument('--source-sha', required=True)
    parser.add_argument('--no-pr-scan', action='store_true', help='development only; candidates are withheld')
    args = parser.parse_args(argv)
    if not 1 <= args.batch_size <= 150:
        parser.error('batch size must be 1 to 150')
    nid_module = load_nid_module(args.repo)
    records, counts, count_files = read_inventory(args.source, nid_module.compute_nid)
    existing, risk, available_modules = existing_exports(args.repo, nid_module)
    claimed, uncertain, scanned, api_requests = {}, {}, 0, 0
    if args.no_pr_scan:
        uncertain = {module: {-1} for module, _ in records}
    else:
        token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if not token:
            parser.error('GH_TOKEN or GITHUB_TOKEN is required for open PR overlap checking')
        api = GitHubAPI(token, args.upstream)
        claimed, uncertain, scanned = pending_exports(api, nid_module.compute_nid, {module for module, _ in records})
        api_requests = api.requests
    report = write_report(args.out, records, counts, count_files, existing, risk, available_modules, claimed,
                          uncertain, scanned, api_requests, args.batch_size, args.repo_sha, args.source_sha)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, urllib.error.HTTPError, urllib.error.URLError) as exc:
        print(f'one-shot importer aborted (no validated candidate report): {exc}', file=sys.stderr)
        sys.exit(1)
