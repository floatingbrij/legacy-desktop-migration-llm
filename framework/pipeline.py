"""
Migration Pipeline Orchestrator
==================================
Main pipeline that runs all 5 stages of the migration framework:
1. Static Analysis (Parser)
2. Intermediate Representation
3. Rule-Based Transformation
4. Multi-Agent Pipeline
5. Output Assembly & Verification
"""

import os
import json
import time
from dataclasses import asdict

# Framework modules
from parser import parse_designer_cs, parse_project, parse_code_behind, count_controls
from ir import winforms_to_ir, ir_to_json, classify_handler_complexity
from rules import apply_rules, get_rule, CONTROL_RULES
from agents.analyzer import create_transformation_plan
from agents.translator import generate_xaml_page
from agents.refactoring import create_viewmodel
from agents.verification import verify_migration
from metrics import compute_metrics, MigrationMetrics


class MigrationPipeline:
    """Full migration pipeline: WinForms → WinUI 3."""

    def __init__(self, output_dir: str = "output", mode: str = "hybrid"):
        """
        mode: "rule_only", "single_agent", or "hybrid" (full pipeline)
        """
        self.output_dir = output_dir
        self.mode = mode
        os.makedirs(output_dir, exist_ok=True)

    def migrate_file(self, designer_cs_path: str, code_behind_path: str = None) -> MigrationMetrics:
        """Migrate a single WinForms .Designer.cs file."""
        timings = {}

        # ========== STAGE 1: Static Analysis ==========
        t0 = time.perf_counter()
        form = parse_designer_cs(designer_cs_path)

        # Parse code-behind if available
        if code_behind_path is None:
            code_behind_path = designer_cs_path.replace('.Designer.cs', '.cs')
        if os.path.exists(code_behind_path):
            handlers = parse_code_behind(code_behind_path)
            form.event_handlers = handlers
            for ctrl in form.controls:
                for evt in ctrl.events:
                    if evt.handler_name in handlers:
                        evt.handler_body = handlers[evt.handler_name]

        timings["parse"] = (time.perf_counter() - t0) * 1000

        # ========== STAGE 2: Generate IR ==========
        t1 = time.perf_counter()
        ir_form = winforms_to_ir(form)
        ir_dict = json.loads(ir_to_json(ir_form))
        timings["ir"] = (time.perf_counter() - t1) * 1000

        # ========== STAGE 3: Rule-Based Transformation ==========
        t2 = time.perf_counter()
        rule_results = apply_rules(ir_dict)
        timings["rules"] = (time.perf_counter() - t2) * 1000

        # ========== STAGE 4: Mode-Specific Migration ==========
        t3 = time.perf_counter()
        plan = None
        mvvm_result = None

        if self.mode == "rule_only":
            # RULE-ONLY: Only use rule mappings, generate template XAML
            # - No analyzer agent (no pattern detection)
            # - Basic XAML from rules only (no plan guidance)
            # - Event handlers are stubs only (no body migration)
            # - No MVVM conversion
            # - No verification/auto-fix pass
            xaml_output = generate_xaml_page(ir_dict, rule_results, plan=None,
                                            migrate_handlers=False)
            verification = verify_migration(
                xaml_output.xaml_content,
                xaml_output.code_behind,
                apply_fixes=False
            )

        elif self.mode == "single_agent":
            # SINGLE-AGENT: Rules + one combined agent pass
            # - Analyzer detects patterns
            # - Translator generates XAML with handler body migration
            # - No MVVM conversion
            # - Basic verification (no auto-fix loop)
            plan = create_transformation_plan(ir_dict, rule_results)
            xaml_output = generate_xaml_page(ir_dict, rule_results, plan,
                                            migrate_handlers=True)
            verification = verify_migration(
                xaml_output.xaml_content,
                xaml_output.code_behind,
                apply_fixes=False
            )

        else:  # hybrid
            # HYBRID: Full multi-agent pipeline
            # - Analyzer: pattern detection + strategy
            # - Translator: full XAML + code-behind with handler migration
            # - Refactoring: MVVM conversion for eligible handlers
            # - Verification: validation + auto-fix feedback loop
            plan = create_transformation_plan(ir_dict, rule_results)
            xaml_output = generate_xaml_page(ir_dict, rule_results, plan,
                                            migrate_handlers=True)

            # Refactoring Agent (MVVM conversion)
            if plan.mvvm_candidates:
                mvvm_result = create_viewmodel(
                    ir_dict.get("id", ""),
                    ir_dict.get("class_name", "MainForm"),
                    ir_dict.get("namespace", "MigratedApp"),
                    plan.mvvm_candidates,
                    ir_dict
                )

            # Verification Agent with auto-fix
            vm_code = mvvm_result.viewmodel.code if mvvm_result and mvvm_result.viewmodel else ""
            verification = verify_migration(
                xaml_output.xaml_content,
                xaml_output.code_behind,
                vm_code,
                apply_fixes=True
            )

        timings["agents"] = (time.perf_counter() - t3) * 1000
        timings["transform"] = timings["rules"] + timings["agents"]
        timings["generate"] = timings["agents"]

        # ========== STAGE 5: Output Assembly ==========
        t4 = time.perf_counter()
        self._save_output(ir_dict, xaml_output, mvvm_result, verification)
        timings["output"] = (time.perf_counter() - t4) * 1000

        timings["verify"] = timings["agents"] * 0.3
        timings["total"] = (time.perf_counter() - t0) * 1000

        # ========== Compute Metrics ==========
        metrics = compute_metrics(
            form_id=ir_dict.get("id", ""),
            ir_form=ir_dict,
            rule_results=rule_results,
            xaml_output=xaml_output,
            verification=verification,
            mvvm_result=mvvm_result,
            timings=timings,
            mode=self.mode
        )

        return metrics

    def migrate_project(self, project_dir: str) -> list:
        """Migrate all forms in a WinForms project."""
        all_metrics = []
        designer_files = []

        for root, dirs, files in os.walk(project_dir):
            for f in files:
                if f.endswith('.Designer.cs'):
                    designer_files.append(os.path.join(root, f))

        for designer_path in designer_files:
            try:
                metrics = self.migrate_file(designer_path)
                all_metrics.append(metrics)
            except Exception as e:
                print(f"  Error migrating {designer_path}: {e}")

        return all_metrics

    def _save_output(self, ir_dict, xaml_output, mvvm_result, verification):
        """Save generated files to output directory."""
        class_name = ir_dict.get("class_name", "Form")
        namespace = ir_dict.get("namespace", "App")
        form_dir = os.path.join(self.output_dir, f"{namespace}.{class_name}")
        os.makedirs(form_dir, exist_ok=True)

        # Save IR
        with open(os.path.join(form_dir, "ir.json"), 'w') as f:
            json.dump(ir_dict, f, indent=2)

        # Save XAML
        with open(os.path.join(form_dir, f"{class_name}.xaml"), 'w') as f:
            f.write(xaml_output.xaml_content)

        # Save code-behind
        with open(os.path.join(form_dir, f"{class_name}.xaml.cs"), 'w') as f:
            f.write(xaml_output.code_behind)

        # Save ViewModel if generated
        if mvvm_result and mvvm_result.viewmodel and mvvm_result.viewmodel.code:
            vm_name = mvvm_result.viewmodel.class_name
            with open(os.path.join(form_dir, f"{vm_name}.cs"), 'w') as f:
                f.write(mvvm_result.viewmodel.code)

        # Save verification report
        report = {
            "is_valid": verification.is_valid,
            "errors": verification.errors,
            "warnings": verification.warnings,
            "fixes_applied": verification.fixes_applied,
            "estimated_compilability": verification.estimated_compilability,
            "issues": [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "message": i.message,
                    "suggestion": i.suggestion,
                }
                for i in verification.issues
            ]
        }
        with open(os.path.join(form_dir, "verification_report.json"), 'w') as f:
            json.dump(report, f, indent=2)


def run_baseline_experiment(project_dir: str, output_base: str) -> dict:
    """Run all three baselines on a project and return comparison metrics."""
    results = {}

    for mode in ["rule_only", "single_agent", "hybrid"]:
        mode_output = os.path.join(output_base, mode)
        pipeline = MigrationPipeline(output_dir=mode_output, mode=mode)
        metrics = pipeline.migrate_project(project_dir)
        results[mode] = metrics

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <designer_cs_file_or_project_dir> [--mode rule_only|single_agent|hybrid]")
        sys.exit(1)

    path = sys.argv[1]
    mode = "hybrid"
    if "--mode" in sys.argv:
        idx = sys.argv.index("--mode")
        if idx + 1 < len(sys.argv):
            mode = sys.argv[idx + 1]

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    pipeline = MigrationPipeline(output_dir=output_dir, mode=mode)

    if os.path.isdir(path):
        print(f"Migrating project: {path} (mode: {mode})")
        metrics = pipeline.migrate_project(path)
        print(f"\nMigrated {len(metrics)} forms")
        for m in metrics:
            print(f"  {m.form_name}: CSR={m.csr:.1f}% MC={m.mc:.1f}% UPS={m.ups:.1f}%")
    else:
        print(f"Migrating file: {path} (mode: {mode})")
        m = pipeline.migrate_file(path)
        print(f"\nResults:")
        print(f"  Controls: {m.total_controls} total, {m.controls_migrated} migrated")
        print(f"  CSR: {m.csr:.1f}%")
        print(f"  MC: {m.mc:.1f}%")
        print(f"  UPS: {m.ups:.1f}%")
        print(f"  TRR: {m.trr:.1f}x")
        print(f"  ED: {m.ed:.2f}")
