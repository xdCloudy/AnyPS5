#!/usr/bin/env python3
"""Delete only explicitly audited, merged AnyPS5 fork PR branches."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

FORK = "xdCloudy/AnyPS5"
UPSTREAM = "boykopovar/AnyPS5"
PROTECTED = {"main", "one-shot/ps5-320-inventory", "research/all-system-export-stubs-20261021"}


def api(method, path, token):
    url = "https://api.github.com/" + path
    req = urllib.request.Request(url, method=method,
                                 headers={"Accept": "application/vnd.github+json",
                                          "Authorization": "Bearer " + token,
                                          "X-GitHub-Api-Version": "2022-11-28",
                                          "User-Agent": "AnyPS5-merged-branch-cleanup"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            return response.status, json.loads(content) if content else None
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return 404, None
        raise


def prune(entries, token, dry_run=False):
    results = []
    seen = set()
    for entry in entries:
        branch, sha, number = entry["branch"], entry["sha"], entry["pr"]
        if branch in seen:
            raise ValueError("duplicate branch in audit manifest: " + branch)
        seen.add(branch)
        if branch in PROTECTED or not branch or not isinstance(number, int):
            raise ValueError("unsafe branch in audit manifest: " + branch)
        if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError("invalid recorded SHA for " + branch)

        result = {"branch": branch, "pr": number, "expected_sha": sha}
        try:
            encoded = urllib.parse.quote(branch, safe="/")
            code, current = api("GET", f"repos/{FORK}/branches/{encoded}", token)
            if code == 404:
                result["status"] = "already_deleted"
            elif code != 200 or not current or current.get("protected") or current["commit"]["sha"] != sha:
                result["status"] = "skipped_branch_moved_or_protected"
            else:
                status, pr = api("GET", f"repos/{UPSTREAM}/pulls/{number}", token)
                if status != 200 or not pr:
                    result["status"] = "skipped_pr_not_found"
                elif not pr.get("merged_at"):
                    result["status"] = "skipped_not_merged"
                elif pr.get("head", {}).get("ref") != branch:
                    result["status"] = "skipped_pr_branch_changed"
                elif (pr.get("head", {}).get("repo") or {}).get("full_name") != FORK:
                    result["status"] = "skipped_pr_owner_changed"
                elif pr.get("head", {}).get("sha") != sha:
                    result["status"] = "skipped_pr_head_changed"
                elif dry_run:
                    result["status"] = "eligible_dry_run"
                else:
                    code, _ = api("DELETE", f"repos/{FORK}/git/refs/heads/{encoded}", token)
                    result["status"] = "deleted" if code == 204 else f"unexpected_delete_status_{code}"
        except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
            result["status"] = "error"
            result["error"] = str(exc)
        results.append(result)
        print(f"PR #{number}: {branch}: {result['status']}", flush=True)
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if os.environ.get("GITHUB_REPOSITORY") != FORK:
        ap.error(f"will only operate in {FORK}")
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        ap.error("run only from the fork's default main branch")
    token = os.environ.get("GH_TOKEN")
    if not token:
        ap.error("GH_TOKEN must be set")
    entries = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(entries, list) or not entries:
        ap.error("manifest must be a non-empty list")
    results = prune(entries, token, args.dry_run)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    counts = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    print(json.dumps({"counts": counts, "results": str(args.out)}, indent=2))
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as stream:
            stream.write("\n## Merged fork branch cleanup\n\n")
            stream.write("| Outcome | Branches |\n|---|---:|\n")
            for label, count in sorted(counts.items()):
                stream.write(f"| {label} | {count} |\n")
            stream.write("\nUnmerged, open, unmatched, and protected branches were not targeted.\n")
    if any(result["status"] in ("error", "skipped_branch_moved_or_protected",
                                "skipped_pr_branch_changed", "skipped_pr_owner_changed",
                                "skipped_pr_head_changed") or
           result["status"].startswith("unexpected_") for result in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
