"""
GitHub Dataset Collection Script for Research Paper:
"Automated Migration of Legacy Windows Desktop Applications to WinUI 3 
 Using Hybrid Rule-Based and Multi-Agent LLM Framework"

Collects 100+ public GitHub repositories containing WinForms, WPF, and UWP applications.
Outputs: dataset.csv and dataset_stats.md

Usage:
    set GITHUB_TOKEN=your_token_here
    python collect_dataset.py
"""

import csv
import json
import os
import sys
import time
from datetime import datetime
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
BASE_URL = "https://api.github.com"
OUTPUT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.csv")
OUTPUT_STATS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset_stats.md")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

# --- Search queries for each framework ---
SEARCH_QUERIES = {
    "WinForms": [
        "topic:winforms language:C# fork:false stars:>0",
        "topic:windows-forms language:C# fork:false stars:>0",
        '"System.Windows.Forms" language:C# fork:false stars:>1',
    ],
    "WPF": [
        "topic:wpf language:C# fork:false stars:>0",
        '"PresentationFramework" language:C# fork:false stars:>1',
    ],
    "UWP": [
        "topic:uwp language:C# fork:false stars:>0",
        '"Windows.UI.Xaml" language:C# fork:false stars:>1',
    ],
}

# Target counts per framework
TARGETS = {"WinForms": 80, "WPF": 30, "UWP": 20}

CSV_FIELDS = [
    "repo_url", "repo_name", "owner", "framework", "stars", "forks",
    "last_commit", "language", "cs_file_count", "designer_cs_count",
    "xaml_count", "resx_count", "complexity_tier", "license",
    "description", "created_at",
]


def api_get(url):
    """Make an authenticated GET request to the GitHub API with rate-limit handling."""
    req = Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urlopen(req) as resp:
                remaining = resp.headers.get("X-RateLimit-Remaining", "?")
                if remaining != "?" and int(remaining) < 5:
                    reset = int(resp.headers.get("X-RateLimit-Reset", 0))
                    wait = max(reset - int(time.time()), 1)
                    print(f"  Rate limit low ({remaining}), waiting {wait}s...")
                    time.sleep(wait)
                return json.loads(resp.read().decode())
        except HTTPError as e:
            if e.code == 403:
                reset = int(e.headers.get("X-RateLimit-Reset", 0))
                wait = max(reset - int(time.time()), 10)
                print(f"  Rate limited (403). Waiting {wait}s...")
                time.sleep(wait)
            elif e.code == 422:
                print(f"  Unprocessable query (422), skipping: {url}")
                return None
            else:
                print(f"  HTTP {e.code} for {url}, retry {attempt+1}/3")
                time.sleep(5)
        except URLError as e:
            print(f"  Network error: {e}, retry {attempt+1}/3")
            time.sleep(5)
    return None


def search_repos(query, per_page=100, max_pages=5):
    """Search GitHub repos and return a list of repo dicts."""
    repos = []
    for page in range(1, max_pages + 1):
        encoded_q = quote(query)
        url = f"{BASE_URL}/search/repositories?q={encoded_q}&sort=stars&order=desc&per_page={per_page}&page={page}"
        data = api_get(url)
        if not data or "items" not in data:
            break
        repos.extend(data["items"])
        if len(data["items"]) < per_page:
            break
        time.sleep(2)  # Respect search API rate limit (30 req/min)
    return repos


def count_files_by_extension(owner, repo, extensions):
    """Count files matching given extensions using the GitHub Trees API."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    data = api_get(url)
    if not data or "tree" not in data:
        return {}
    counts = {ext: 0 for ext in extensions}
    for item in data["tree"]:
        if item["type"] != "blob":
            continue
        path = item["path"].lower()
        for ext in extensions:
            if path.endswith(ext.lower()):
                counts[ext] += 1
    return counts


def classify_complexity(designer_count, xaml_count, cs_count):
    """Assign complexity tier based on form/file counts."""
    ui_files = designer_count + xaml_count
    if ui_files <= 5:
        return "Small"
    elif ui_files <= 15:
        return "Medium"
    else:
        return "Large"


def collect_dataset():
    """Main collection loop."""
    if not GITHUB_TOKEN:
        print("WARNING: No GITHUB_TOKEN set. Rate limits will be very restrictive (10 req/min).")
        print("Set it with: set GITHUB_TOKEN=your_token_here\n")

    all_repos = {}  # keyed by full_name to deduplicate
    framework_counts = {"WinForms": 0, "WPF": 0, "UWP": 0}

    for framework, queries in SEARCH_QUERIES.items():
        print(f"\n{'='*60}")
        print(f"Searching for {framework} repositories...")
        print(f"{'='*60}")
        for qi, query in enumerate(queries):
            if framework_counts[framework] >= TARGETS[framework]:
                break
            print(f"  Query {qi+1}/{len(queries)}: {query}")
            repos = search_repos(query, per_page=100, max_pages=3)
            print(f"  Found {len(repos)} results")
            for repo in repos:
                if framework_counts[framework] >= TARGETS[framework]:
                    break
                full_name = repo["full_name"]
                if full_name in all_repos:
                    continue
                if repo["fork"]:
                    continue
                if repo["language"] != "C#":
                    continue
                if repo.get("stargazers_count", 0) < 1:
                    continue

                # Get file counts
                owner = repo["owner"]["login"]
                name = repo["name"]
                print(f"    Inspecting {full_name}...", end=" ")
                file_counts = count_files_by_extension(owner, name, [
                    ".cs", ".Designer.cs", ".xaml", ".resx", ".csproj", ".sln"
                ])

                cs_count = file_counts.get(".cs", 0)
                designer_count = file_counts.get(".Designer.cs", 0)
                xaml_count = file_counts.get(".xaml", 0)
                resx_count = file_counts.get(".resx", 0)
                has_project = file_counts.get(".csproj", 0) + file_counts.get(".sln", 0)

                # Apply inclusion filters
                if cs_count < 3:
                    print("SKIP (< 3 .cs files)")
                    continue
                if has_project == 0:
                    print("SKIP (no .csproj/.sln)")
                    continue

                # Framework-specific validation
                if framework == "WinForms" and designer_count == 0:
                    # For topic-based searches, allow repos without .Designer.cs
                    # as they may still be WinForms but use code-only approach
                    pass
                if framework in ("WPF", "UWP") and xaml_count == 0:
                    pass  # topic-based may still be valid

                complexity = classify_complexity(designer_count, xaml_count, cs_count)
                license_name = repo.get("license", {})
                license_str = license_name.get("spdx_id", "None") if license_name else "None"

                entry = {
                    "repo_url": repo["html_url"],
                    "repo_name": name,
                    "owner": owner,
                    "framework": framework,
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "last_commit": repo.get("pushed_at", "")[:10],
                    "language": repo.get("language", "C#"),
                    "cs_file_count": cs_count,
                    "designer_cs_count": designer_count,
                    "xaml_count": xaml_count,
                    "resx_count": resx_count,
                    "complexity_tier": complexity,
                    "license": license_str,
                    "description": (repo.get("description") or "")[:200],
                    "created_at": repo.get("created_at", "")[:10],
                }
                all_repos[full_name] = entry
                framework_counts[framework] += 1
                print(f"OK ({cs_count} .cs, {designer_count} .Designer.cs, {xaml_count} .xaml) [{framework_counts[framework]}]")
                time.sleep(1)  # Be respectful to API

    return list(all_repos.values())


def write_csv(repos):
    """Write collected repos to CSV."""
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for repo in sorted(repos, key=lambda r: (-r["stars"], r["repo_name"])):
            writer.writerow(repo)
    print(f"\nDataset written to: {OUTPUT_CSV}")
    print(f"Total repos: {len(repos)}")


def write_stats(repos):
    """Generate dataset statistics markdown."""
    fw_counts = {"WinForms": 0, "WPF": 0, "UWP": 0}
    tier_counts = {"Small": 0, "Medium": 0, "Large": 0}
    total_stars = 0
    total_cs = 0
    total_designer = 0
    total_xaml = 0

    for r in repos:
        fw = r["framework"]
        fw_counts[fw] = fw_counts.get(fw, 0) + 1
        tier_counts[r["complexity_tier"]] = tier_counts.get(r["complexity_tier"], 0) + 1
        total_stars += r["stars"]
        total_cs += r["cs_file_count"]
        total_designer += r["designer_cs_count"]
        total_xaml += r["xaml_count"]

    n = len(repos)
    avg_stars = total_stars / n if n else 0
    avg_cs = total_cs / n if n else 0

    with open(OUTPUT_STATS, "w", encoding="utf-8") as f:
        f.write("# Dataset Statistics\n\n")
        f.write(f"**Total Repositories:** {n}\n\n")
        f.write(f"**Collection Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("## Framework Distribution\n\n")
        f.write("| Framework | Count | Percentage |\n")
        f.write("|-----------|-------|------------|\n")
        for fw, count in fw_counts.items():
            pct = (count / n * 100) if n else 0
            f.write(f"| {fw} | {count} | {pct:.1f}% |\n")
        f.write(f"| **Total** | **{n}** | **100%** |\n\n")

        f.write("## Complexity Distribution\n\n")
        f.write("| Tier | Criteria | Count | Percentage |\n")
        f.write("|------|----------|-------|------------|\n")
        criteria = {"Small": "≤5 UI files", "Medium": "6–15 UI files", "Large": ">15 UI files"}
        for tier in ["Small", "Medium", "Large"]:
            count = tier_counts.get(tier, 0)
            pct = (count / n * 100) if n else 0
            f.write(f"| {tier} | {criteria[tier]} | {count} | {pct:.1f}% |\n")
        f.write("\n")

        f.write("## Summary Statistics\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Average Stars | {avg_stars:.1f} |\n")
        f.write(f"| Average .cs Files per Repo | {avg_cs:.1f} |\n")
        f.write(f"| Total .Designer.cs Files | {total_designer} |\n")
        f.write(f"| Total .xaml Files | {total_xaml} |\n")
        f.write(f"| Repos with Open License | {sum(1 for r in repos if r['license'] != 'None')} |\n")

    print(f"Statistics written to: {OUTPUT_STATS}")


if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Dataset Collector for WinForms/WPF/UWP Research")
    print("=" * 60)
    repos = collect_dataset()
    if repos:
        write_csv(repos)
        write_stats(repos)
    else:
        print("No repos collected. Check your token and network connection.")
        sys.exit(1)
