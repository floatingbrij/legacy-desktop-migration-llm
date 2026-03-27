"""
Experiment Runner
==================
Runs all three baselines (rule_only, single_agent, hybrid) on
the test dataset and generates result tables for the paper.
"""

import os
import sys
import json
import csv
import time
from dataclasses import asdict

# Add framework to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import parse_designer_cs, parse_code_behind
from ir import winforms_to_ir
from rules import apply_rules
from agents.analyzer import create_transformation_plan
from agents.translator import generate_xaml_page
from agents.refactoring import create_viewmodel
from agents.verification import verify_migration
from metrics import compute_metrics, aggregate_metrics, format_metrics_table, MigrationMetrics
from pipeline import MigrationPipeline


def discover_test_apps(test_dir: str) -> list:
    """Discover all test app directories."""
    apps = []
    if not os.path.exists(test_dir):
        return apps

    for entry in sorted(os.listdir(test_dir)):
        app_dir = os.path.join(test_dir, entry)
        if os.path.isdir(app_dir):
            # Find .Designer.cs files
            for f in os.listdir(app_dir):
                if f.endswith('.Designer.cs'):
                    tier = "small" if entry.startswith("small") else "medium" if entry.startswith("med") else "large"
                    apps.append({
                        "name": entry,
                        "dir": app_dir,
                        "designer": os.path.join(app_dir, f),
                        "code_behind": os.path.join(app_dir, f.replace('.Designer.cs', '.cs')),
                        "tier": tier,
                    })
    return apps


def run_experiment(apps: list, output_base: str) -> dict:
    """Run all three baselines on all apps."""
    results = {"rule_only": [], "single_agent": [], "hybrid": []}

    for mode in ["rule_only", "single_agent", "hybrid"]:
        print(f"\n{'='*60}")
        print(f"  Running baseline: {mode.upper()}")
        print(f"{'='*60}")

        mode_output = os.path.join(output_base, mode)
        pipeline = MigrationPipeline(output_dir=mode_output, mode=mode)

        for app in apps:
            try:
                print(f"  Migrating: {app['name']} ({app['tier']})...", end=" ")
                metrics = pipeline.migrate_file(
                    app["designer"],
                    app.get("code_behind")
                )
                # Override the tier from our knowledge
                metrics.complexity_tier = app["tier"]
                # Ensure form_name is set
                if not metrics.form_name:
                    metrics.form_name = app["name"]
                results[mode].append(metrics)
                print(f"Compile={metrics.csr:.0f}% Complete={metrics.mc:.0f}% UIParity={metrics.ups:.0f}%")
            except Exception as e:
                print(f"FAILED: {e}")
                # Create failed metrics entry
                failed = MigrationMetrics(
                    form_id=app["name"],
                    form_name=app["name"],
                    complexity_tier=app["tier"],
                    csr=0, mc=0, ups=0, trr=0, ed=100
                )
                results[mode].append(failed)

    return results


def generate_tables(results: dict) -> str:
    """Generate result tables for the paper."""
    output = []

    # Metric definitions
    output.append("=" * 80)
    output.append("METRIC DEFINITIONS")
    output.append("=" * 80)
    output.append("  Compilable%    - Compilation Success Rate: % of forms that produce")
    output.append("                   compilable WinUI 3 output (estimated)")
    output.append("  Complete%      - Migration Completeness: % of source controls")
    output.append("                   that were successfully migrated to WinUI 3")
    output.append("  UI Parity%     - UI Parity Score: % of UI properties (colors, fonts,")
    output.append("                   layout) correctly mapped to WinUI 3 equivalents")
    output.append("  Speedup        - Time Reduction Ratio: how many times faster the")
    output.append("                   automated migration is vs estimated manual effort")
    output.append("  Err/100LOC     - Error Density: number of remaining errors per")
    output.append("                   100 lines of generated code (lower is better)")

    # ==========================================
    # TABLE III: Results by Complexity Tier (Hybrid)
    # ==========================================
    output.append("\n" + "="*80)
    output.append("TABLE III: Migration Results by Complexity Tier (Hybrid Framework)")
    output.append("="*80)

    hybrid_metrics = results.get("hybrid", [])
    if hybrid_metrics:
        agg = aggregate_metrics(hybrid_metrics)

        output.append(f"\n{'Tier':<10} {'n':>3} {'Compilable%':>12} {'Complete%':>11} {'UI Parity%':>11} {'Speedup':>9} {'Err/100LOC':>11}")
        output.append("-" * 72)

        for tier in ["small", "medium", "large"]:
            tier_data = agg.get("by_tier", {}).get(tier, {})
            if tier_data:
                output.append(
                    f"{tier.capitalize():<10} {tier_data.get('count', 0):>3} "
                    f"{tier_data.get('avg_csr', 0):>10.1f}%  {tier_data.get('avg_mc', 0):>9.1f}%  "
                    f"{tier_data.get('avg_ups', 0):>9.1f}%  {tier_data.get('avg_trr', 0):>7.0f}x "
                    f"{tier_data.get('avg_ed', 0):>10.2f}"
                )

        output.append("-" * 72)
        output.append(
            f"{'Overall':<10} {agg.get('total_forms', 0):>3} "
            f"{agg.get('avg_csr', 0):>10.1f}%  {agg.get('avg_mc', 0):>9.1f}%  "
            f"{agg.get('avg_ups', 0):>9.1f}%  {agg.get('avg_trr', 0):>7.0f}x "
            f"{agg.get('avg_ed', 0):>10.2f}"
        )

    # ==========================================
    # TABLE IV: Baseline Comparison
    # ==========================================
    output.append("\n\n" + "="*80)
    output.append("TABLE IV: Baseline Comparison")
    output.append("="*80)

    output.append(f"\n{'Approach':<22} {'Compilable%':>12} {'Complete%':>11} {'UI Parity%':>11} {'Speedup':>9} {'Err/100LOC':>11}")
    output.append("-" * 80)

    for mode, label in [("rule_only", "Rule-Only"), ("single_agent", "Single-Agent LLM"), ("hybrid", "Full Hybrid (Ours)")]:
        metrics_list = results.get(mode, [])
        if metrics_list:
            agg = aggregate_metrics(metrics_list)
            output.append(
                f"{label:<22} {agg.get('avg_csr', 0):>10.1f}%  {agg.get('avg_mc', 0):>9.1f}%  "
                f"{agg.get('avg_ups', 0):>9.1f}%  {agg.get('avg_trr', 0):>7.0f}x "
                f"{agg.get('avg_ed', 0):>10.2f}"
            )

    # ==========================================
    # TABLE V: Per-App Results (Hybrid)
    # ==========================================
    output.append("\n\n" + "="*80)
    output.append("TABLE V: Per-Application Results (Hybrid Framework)")
    output.append("="*80)

    if hybrid_metrics:
        output.append(f"\n{'Application':<30} {'Tier':<8} {'Controls':>9} {'Events':>7} {'Compilable%':>12} {'Complete%':>11} {'UI Parity%':>11} {'Speedup':>9}")
        output.append("-" * 105)
        for m in hybrid_metrics:
            output.append(
                f"{m.form_name:<30} {m.complexity_tier:<8} "
                f"{m.total_controls:>9} {m.total_events:>7} "
                f"{m.csr:>10.1f}%  {m.mc:>9.1f}%  {m.ups:>9.1f}%  {m.trr:>7.0f}x"
            )

    # ==========================================
    # TABLE VI: Control Coverage Analysis
    # ==========================================
    output.append("\n\n" + "="*80)
    output.append("TABLE VI: Control-Level Migration Coverage (Hybrid)")
    output.append("="*80)

    # Aggregate control-level stats across all hybrid runs
    total_by_type = {}
    migrated_by_type = {}

    for m in hybrid_metrics:
        if hasattr(m, 'form_name'):
            # We need to re-analyze at control level
            pass

    output.append("\n(Control-level breakdown available in individual verification reports)")

    # ==========================================
    # SUMMARY STATISTICS
    # ==========================================
    output.append("\n\n" + "="*80)
    output.append("SUMMARY STATISTICS")
    output.append("="*80)

    for mode, label in [("rule_only", "Rule-Only"), ("single_agent", "Single-Agent"), ("hybrid", "Hybrid")]:
        metrics_list = results.get(mode, [])
        if metrics_list:
            agg = aggregate_metrics(metrics_list)
            output.append(f"\n{label}:")
            output.append(f"  Total forms processed: {agg.get('total_forms', 0)}")
            output.append(f"  Total controls: {agg.get('total_controls', 0)}")
            output.append(f"  Controls successfully migrated: {agg.get('total_controls_migrated', 0)}")
            output.append(f"  Avg Compilation Success Rate: {agg.get('avg_csr', 0):.1f}%")
            output.append(f"  Avg Migration Completeness: {agg.get('avg_mc', 0):.1f}%")
            output.append(f"  Compilation Success range: {agg.get('min_csr', 0):.1f}% - {agg.get('max_csr', 0):.1f}%")

    return "\n".join(output)


def save_results_csv(results: dict, output_path: str):
    """Save results to CSV for further analysis."""
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "mode", "app", "tier", "controls", "events",
            "compilation_success_rate", "migration_completeness", "ui_parity_score", "time_reduction_ratio", "error_density",
            "rule_mapped", "agent_needed", "unmapped",
            "xaml_loc", "code_behind_loc", "vm_loc",
            "errors", "warnings", "fixes",
            "time_ms"
        ])

        for mode, metrics_list in results.items():
            for m in metrics_list:
                writer.writerow([
                    mode, m.form_name, m.complexity_tier,
                    m.total_controls, m.total_events,
                    f"{m.csr:.1f}", f"{m.mc:.1f}", f"{m.ups:.1f}",
                    f"{m.trr:.1f}", f"{m.ed:.2f}",
                    m.rule_mapped, m.agent_needed, m.unmapped,
                    m.xaml_loc, m.code_behind_loc, m.viewmodel_loc,
                    m.verification_errors, m.verification_warnings, m.auto_fixes,
                    f"{m.total_time_ms:.1f}"
                ])


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(base_dir, "test_apps")
    output_dir = os.path.join(base_dir, "experiments")

    # Step 1: Generate test apps if needed
    print("Step 1: Generating test applications...")
    from generate_test_apps import generate_all
    generate_all()

    # Step 2: Discover apps
    print("\nStep 2: Discovering test applications...")
    apps = discover_test_apps(test_dir)
    print(f"  Found {len(apps)} test applications:")
    for app in apps:
        print(f"    {app['name']} ({app['tier']})")

    if not apps:
        print("No test apps found!")
        return

    # Step 3: Run experiments
    print("\nStep 3: Running experiments...")
    results = run_experiment(apps, output_dir)

    # Step 4: Generate tables
    print("\nStep 4: Generating result tables...")
    tables = generate_tables(results)
    print(tables)

    # Save results
    tables_path = os.path.join(output_dir, "experiment_results.txt")
    with open(tables_path, 'w') as f:
        f.write(tables)
    print(f"\nResults saved to: {tables_path}")

    csv_path = os.path.join(output_dir, "experiment_results.csv")
    save_results_csv(results, csv_path)
    print(f"CSV saved to: {csv_path}")

    # Save JSON summary
    summary = {}
    for mode, metrics_list in results.items():
        if metrics_list:
            agg = aggregate_metrics(metrics_list)
            summary[mode] = agg
    summary_path = os.path.join(output_dir, "experiment_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()
