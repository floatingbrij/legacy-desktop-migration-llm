"""
Expanded GitHub Dataset Collector — targets 500+ WinForms/WPF/UWP repositories.

Broadens search with many query variations, star ranges, and keyword searches.
Deduplicates by full_name. Appends to existing dataset.csv.

Usage:
    set GITHUB_TOKEN=ghp_...
    python collect_dataset_large.py
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
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "dataset.csv")
OUTPUT_STATS = os.path.join(SCRIPT_DIR, "dataset_stats.md")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

CSV_FIELDS = [
    "repo_url", "repo_name", "owner", "framework", "stars", "forks",
    "last_commit", "language", "cs_file_count", "designer_cs_count",
    "xaml_count", "resx_count", "complexity_tier", "license",
    "description", "created_at",
]

# Broadened search queries with star range segmentation to bypass GitHub 1000-result limit
SEARCH_QUERIES = {
    "WinForms": [
        # Topic-based
        "topic:winforms language:C# fork:false stars:>100",
        "topic:winforms language:C# fork:false stars:10..100",
        "topic:winforms language:C# fork:false stars:1..9",
        "topic:windows-forms language:C# fork:false stars:>10",
        "topic:windows-forms language:C# fork:false stars:1..10",
        # Code-based searches
        '"System.Windows.Forms" language:C# fork:false stars:>50',
        '"System.Windows.Forms" language:C# fork:false stars:10..50',
        '"System.Windows.Forms" language:C# fork:false stars:3..9',
        '"System.Windows.Forms" language:C# fork:false stars:1..2',
        # Keyword searches
        '"InitializeComponent" "Designer.cs" language:C# fork:false stars:>5',
        '"WinForms" "csproj" language:C# fork:false stars:>5',
        '"WindowsFormsApplication" language:C# fork:false stars:>3',
        "winforms application language:C# fork:false stars:>10",
        "windows forms app language:C# fork:false stars:>5",
        # UI-specific
        '"System.Windows.Forms.Button" language:C# fork:false stars:>5',
        '"System.Windows.Forms.DataGridView" language:C# fork:false stars:>3',
        # Additional topic combos
        "topic:desktop-application language:C# topic:winforms fork:false",
        "topic:csharp topic:winforms fork:false stars:>0",
    ],
    "WPF": [
        # Topic-based with star ranges
        "topic:wpf language:C# fork:false stars:>100",
        "topic:wpf language:C# fork:false stars:10..100",
        "topic:wpf language:C# fork:false stars:1..9",
        "topic:xaml topic:wpf language:C# fork:false stars:>5",
        # Code-based
        '"PresentationFramework" language:C# fork:false stars:>20',
        '"PresentationFramework" language:C# fork:false stars:3..20',
        '"PresentationFramework" language:C# fork:false stars:1..2',
        # Keyword searches
        '"wpf" "mvvm" language:C# fork:false stars:>10',
        '"wpf" "xaml" language:C# fork:false stars:>5',
        "wpf application language:C# fork:false stars:>10",
        "wpf desktop language:C# fork:false stars:>5",
        '"Window x:Class" language:C# fork:false stars:>5',
        "topic:wpf-application language:C# fork:false",
        "topic:wpf-app language:C# fork:false stars:>0",
        # MVVM combos
        '"wpf" "ObservableCollection" language:C# fork:false stars:>5',
        '"wpf" "ICommand" language:C# fork:false stars:>3',
    ],
    "UWP": [
        # Topic-based with star ranges
        "topic:uwp language:C# fork:false stars:>50",
        "topic:uwp language:C# fork:false stars:10..50",
        "topic:uwp language:C# fork:false stars:1..9",
        "topic:uwp-app language:C# fork:false stars:>0",
        "topic:universal-windows-platform language:C# fork:false",
        # Code-based
        '"Windows.UI.Xaml" language:C# fork:false stars:>10',
        '"Windows.UI.Xaml" language:C# fork:false stars:1..10',
        # Keyword searches
        "uwp application language:C# fork:false stars:>5",
        "uwp app language:C# fork:false stars:>3",
        '"uwp" "package.appxmanifest" language:C# fork:false stars:>3',
        "topic:windows-10 topic:uwp language:C# fork:false",
        "topic:uwp-apps language:C# fork:false stars:>0",
    ],
}

# Higher targets
TARGETS = {"WinForms": 300, "WPF": 150, "UWP": 80}
GRAND_TARGET = 500


def api_get(url):
    """Authenticated GET with rate-limit handling."""
    req = Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urlopen(req, timeout=30) as resp:
                remaining = resp.headers.get("X-RateLimit-Remaining", "?")
                if remaining != "?" and int(remaining) < 5:
                    reset = int(resp.headers.get("X-RateLimit-Reset", 0))
                    wait = max(reset - int(time.time()), 1) + 2
                    print(f"  [Rate limit low ({remaining}), waiting {wait}s]")
                    time.sleep(wait)
                return json.loads(resp.read().decode())
        except HTTPError as e:
            if e.code == 403:
                reset = int(e.headers.get("X-RateLimit-Reset", 0))
                wait = max(reset - int(time.time()), 10) + 2
                print(f"  [Rate limited, waiting {wait}s]")
                time.sleep(wait)
            elif e.code == 422:
                return None
            else:
                print(f"  [HTTP {e.code}, retry {attempt+1}]")
                time.sleep(5)
        except (URLError, TimeoutError):
            print(f"  [Network error, retry {attempt+1}]")
            time.sleep(5)
    return None


def search_repos(query, per_page=100, max_pages=10):
    """Search GitHub repos, paginating up to max_pages."""
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
        time.sleep(2.5)  # Search API: 30 req/min
    return repos


def count_files(owner, repo):
    """Count files by extension using Trees API."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    data = api_get(url)
    if not data or "tree" not in data:
        return {}
    counts = {".cs": 0, ".Designer.cs": 0, ".xaml": 0, ".resx": 0, ".csproj": 0, ".sln": 0}
    for item in data["tree"]:
        if item["type"] != "blob":
            continue
        path = item["path"]
        pl = path.lower()
        if pl.endswith(".designer.cs"):
            counts[".Designer.cs"] += 1
            counts[".cs"] += 1
        elif pl.endswith(".cs"):
            counts[".cs"] += 1
        elif pl.endswith(".xaml"):
            counts[".xaml"] += 1
        elif pl.endswith(".resx"):
            counts[".resx"] += 1
        elif pl.endswith(".csproj"):
            counts[".csproj"] += 1
        elif pl.endswith(".sln"):
            counts[".sln"] += 1
    return counts


def classify_complexity(designer_count, xaml_count):
    ui_files = designer_count + xaml_count
    if ui_files <= 5:
        return "Small"
    elif ui_files <= 15:
        return "Medium"
    else:
        return "Large"


def load_existing():
    """Load existing dataset to avoid re-inspecting."""
    existing = {}
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row['owner']}/{row['repo_name']}"
                existing[key] = row
    return existing


def collect():
    if not GITHUB_TOKEN:
        print("ERROR: Set GITHUB_TOKEN environment variable first.")
        sys.exit(1)

    existing = load_existing()
    print(f"Loaded {len(existing)} existing repos from dataset.csv")

    all_repos = dict(existing)  # Start from existing
    framework_counts = {"WinForms": 0, "WPF": 0, "UWP": 0}
    for r in existing.values():
        fw = r.get("framework", "")
        if fw in framework_counts:
            framework_counts[fw] += 1

    print(f"Current counts: {framework_counts}")
    print(f"Grand target: {GRAND_TARGET} repos\n")

    inspected = 0
    added = 0

    for framework, queries in SEARCH_QUERIES.items():
        target = TARGETS[framework]
        print(f"\n{'='*60}")
        print(f"  {framework} — have {framework_counts[framework]}, target {target}")
        print(f"{'='*60}")

        for qi, query in enumerate(queries):
            if framework_counts[framework] >= target:
                print(f"  Target reached for {framework}, moving on")
                break

            print(f"\n  Query {qi+1}/{len(queries)}: {query}")
            repos = search_repos(query, per_page=100, max_pages=10)
            print(f"  Got {len(repos)} results")

            for repo in repos:
                if framework_counts[framework] >= target:
                    break
                if len(all_repos) >= GRAND_TARGET + 50:  # buffer
                    break

                full_name = repo["full_name"]
                if full_name in all_repos:
                    continue
                if repo.get("fork"):
                    continue
                if repo.get("language") != "C#":
                    continue
                if repo.get("stargazers_count", 0) < 1:
                    continue

                owner = repo["owner"]["login"]
                name = repo["name"]

                inspected += 1
                sys.stdout.write(f"    [{inspected}] {full_name}... ")
                sys.stdout.flush()

                fc = count_files(owner, name)
                cs = fc.get(".cs", 0)
                des = fc.get(".Designer.cs", 0)
                xaml = fc.get(".xaml", 0)
                proj = fc.get(".csproj", 0) + fc.get(".sln", 0)

                if cs < 3:
                    print("skip (<3 .cs)")
                    continue
                if proj == 0:
                    print("skip (no project)")
                    continue

                complexity = classify_complexity(des, xaml)
                lic = repo.get("license") or {}
                lic_str = lic.get("spdx_id", "None") if lic else "None"

                entry = {
                    "repo_url": repo["html_url"],
                    "repo_name": name,
                    "owner": owner,
                    "framework": framework,
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "last_commit": (repo.get("pushed_at") or "")[:10],
                    "language": "C#",
                    "cs_file_count": cs,
                    "designer_cs_count": des,
                    "xaml_count": xaml,
                    "resx_count": fc.get(".resx", 0),
                    "complexity_tier": complexity,
                    "license": lic_str,
                    "description": (repo.get("description") or "")[:200],
                    "created_at": (repo.get("created_at") or "")[:10],
                }
                all_repos[full_name] = entry
                framework_counts[framework] += 1
                added += 1
                print(f"OK  cs={cs} des={des} xaml={xaml} [{framework_counts[framework]}/{target}]  total={len(all_repos)}")
                time.sleep(0.5)

    # Write final CSV
    repo_list = list(all_repos.values())
    # Convert numeric fields
    for r in repo_list:
        for k in ["stars", "forks", "cs_file_count", "designer_cs_count", "xaml_count", "resx_count"]:
            r[k] = int(r[k])

    repo_list.sort(key=lambda r: (-r["stars"], r["repo_name"]))

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for r in repo_list:
            writer.writerow(r)

    # Write stats
    write_stats(repo_list)

    print(f"\n{'='*60}")
    print(f"  DONE: {len(repo_list)} total repos ({added} newly added)")
    print(f"  WinForms: {framework_counts['WinForms']}")
    print(f"  WPF:      {framework_counts['WPF']}")
    print(f"  UWP:      {framework_counts['UWP']}")
    print(f"  Written to: {OUTPUT_CSV}")
    print(f"{'='*60}")


def write_stats(repos):
    fw_counts = {"WinForms": 0, "WPF": 0, "UWP": 0}
    tier_counts = {"Small": 0, "Medium": 0, "Large": 0}
    total_stars = total_cs = total_designer = total_xaml = 0

    for r in repos:
        fw_counts[r["framework"]] = fw_counts.get(r["framework"], 0) + 1
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
        for fw in ["WinForms", "WPF", "UWP"]:
            count = fw_counts.get(fw, 0)
            pct = (count / n * 100) if n else 0
            f.write(f"| {fw} | {count} | {pct:.1f}% |\n")
        f.write(f"| **Total** | **{n}** | **100%** |\n\n")

        f.write("## Complexity Distribution\n\n")
        f.write("| Tier | Criteria | Count | Percentage |\n")
        f.write("|------|----------|-------|------------|\n")
        criteria = {"Small": "<=5 UI files", "Medium": "6-15 UI files", "Large": ">15 UI files"}
        for tier in ["Small", "Medium", "Large"]:
            count = tier_counts.get(tier, 0)
            pct = (count / n * 100) if n else 0
            f.write(f"| {tier} | {criteria[tier]} | {count} | {pct:.1f}% |\n")

        f.write("\n## Summary Statistics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Average Stars | {avg_stars:.1f} |\n")
        f.write(f"| Average .cs Files per Repo | {avg_cs:.1f} |\n")
        f.write(f"| Total .Designer.cs Files | {total_designer:,} |\n")
        f.write(f"| Total .xaml Files | {total_xaml:,} |\n")
        f.write(f"| Repos with Open License | {sum(1 for r in repos if r.get('license','None') != 'None')} |\n")

    print(f"Statistics written to: {OUTPUT_STATS}")


if __name__ == "__main__":
    collect()
