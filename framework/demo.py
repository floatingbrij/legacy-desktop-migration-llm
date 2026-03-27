"""
DEMO SCRIPT: Live Migration Demonstration
==========================================
Run this during your review to show the framework in action.
It demonstrates:
  1. Parsing a WinForms .Designer.cs file
  2. Generating the Intermediate Representation
  3. Applying rule-based transformations
  4. Running the full hybrid pipeline
  5. Showing the generated WinUI 3 output
  6. Displaying verification results and metrics

Usage:
  cd c:\Organized\Research Migrate\framework
  python demo.py
"""

import os
import sys
import json
import time

# Add framework to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import parse_designer_cs, parse_code_behind
from ir import winforms_to_ir, ir_to_json
from rules import apply_rules, CONTROL_RULES
from agents.analyzer import create_transformation_plan
from agents.translator import generate_xaml_page
from agents.refactoring import create_viewmodel
from agents.verification import verify_migration
from pipeline import MigrationPipeline

BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def section(title):
    print(f"\n{BOLD}{BLUE}{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}{RESET}\n")

def subsection(title):
    print(f"\n{BOLD}{YELLOW}--- {title} ---{RESET}\n")

def demo_single_app():
    """Demo the full pipeline on the calculator app step by step."""
    app_dir = os.path.join(os.path.dirname(__file__), "test_apps", "small_01_calculator")
    designer = os.path.join(app_dir, "CalculatorForm.Designer.cs")
    codebehind = os.path.join(app_dir, "CalculatorForm.cs")
    
    if not os.path.exists(designer):
        print(f"{RED}Error: Test app not found at {app_dir}{RESET}")
        return

    section("STAGE 1: Static Analysis (Roslyn Parser)")
    print(f"Parsing: {designer}")
    t0 = time.perf_counter()
    form = parse_designer_cs(designer)
    handlers = parse_code_behind(codebehind)
    form.event_handlers = handlers
    for ctrl in form.controls:
        for evt in ctrl.events:
            if evt.handler_name in handlers:
                evt.handler_body = handlers[evt.handler_name]
    t1 = time.perf_counter()
    
    print(f"{GREEN}Class: {form.namespace}.{form.class_name}{RESET}")
    print(f"  Controls found: {len(form.controls)}")
    print(f"  Event handlers: {len(handlers)}")
    print(f"  Parse time: {(t1-t0)*1000:.1f} ms")
    
    for ctrl in form.controls[:5]:
        events_str = ", ".join([e.handler_name for e in ctrl.events]) if ctrl.events else "none"
        print(f"    {ctrl.control_type:20s} -> {ctrl.name:20s}  events: {events_str}")
    if len(form.controls) > 5:
        print(f"    ... and {len(form.controls) - 5} more controls")

    section("STAGE 2: Intermediate Representation")
    ir_form = winforms_to_ir(form)
    ir_json = ir_to_json(ir_form)
    ir_dict = json.loads(ir_json)
    
    print(f"  IR Form ID: {ir_dict.get('id', 'N/A')}")
    print(f"  Class name: {ir_dict.get('class_name', 'N/A')}")
    print(f"  Controls in IR: {len(ir_dict.get('controls', []))}")
    print(f"  Complexity tier: {ir_dict.get('complexity_tier', 'N/A')}")

    section("STAGE 3: Rule-Based Transformation")
    rule_results = apply_rules(ir_dict)
    
    print(f"  Total rules in engine: {len(CONTROL_RULES)}")
    print(f"  Transformations applied: {len(rule_results.get('transformations', []))}")
    print(f"  Toolkit required: {rule_results.get('toolkit_required', False)}")
    
    for tr in rule_results.get("transformations", [])[:5]:
        print(f"    {tr.get('original_type',''):20s} -> {tr.get('winui_tag',''):15s}  (confidence: {tr.get('confidence', 0):.0%})")
    if len(rule_results.get("transformations", [])) > 5:
        print(f"    ... and {len(rule_results['transformations']) - 5} more")

    section("STAGE 4: Multi-Agent LLM Pipeline")
    
    subsection("Agent 1: Analyzer")
    plan = create_transformation_plan(ir_dict, rule_results)
    print(f"  Complex patterns detected: {len(plan.detected_patterns)}")
    for p in plan.detected_patterns[:3]:
        print(f"    - {p}")
    print(f"  MVVM candidates: {len(plan.mvvm_candidates)}")
    
    subsection("Agent 2: Translator")
    xaml_output = generate_xaml_page(ir_dict, rule_results, plan, migrate_handlers=True)
    print(f"  Controls generated: {xaml_output.controls_generated}")
    print(f"  Controls skipped: {xaml_output.controls_skipped}")
    print(f"  XAML lines: {len(xaml_output.xaml_content.splitlines())}")
    print(f"  Code-behind lines: {len(xaml_output.code_behind.splitlines())}")
    
    print(f"\n{BOLD}  Generated XAML (first 15 lines):{RESET}")
    for i, line in enumerate(xaml_output.xaml_content.splitlines()[:15]):
        print(f"    {line}")
    
    subsection("Agent 3: Refactoring (MVVM)")
    if plan.mvvm_candidates:
        mvvm_result = create_viewmodel(
            ir_dict.get("id", ""),
            ir_dict.get("class_name", "MainForm"),
            ir_dict.get("namespace", "MigratedApp"),
            plan.mvvm_candidates,
            ir_dict
        )
        if mvvm_result.viewmodel:
            print(f"  ViewModel generated: {mvvm_result.viewmodel.class_name}")
            print(f"  Events converted: {mvvm_result.events_converted}")
            print(f"  Properties converted: {mvvm_result.properties_converted}")
            print(f"\n{BOLD}  ViewModel (first 15 lines):{RESET}")
            for line in mvvm_result.viewmodel.code.splitlines()[:15]:
                print(f"    {line}")
    else:
        mvvm_result = None
        print("  No MVVM candidates identified")
    
    subsection("Agent 4: Verification")
    vm_code = mvvm_result.viewmodel.code if mvvm_result and mvvm_result.viewmodel else ""
    verification = verify_migration(
        xaml_output.xaml_content,
        xaml_output.code_behind,
        vm_code,
        apply_fixes=True
    )
    print(f"  Valid: {verification.is_valid}")
    print(f"  Total issues: {verification.total_issues}")
    print(f"  Errors: {verification.errors}")
    print(f"  Warnings: {verification.warnings}")
    print(f"  Fixes applied: {verification.fixes_applied}")
    print(f"  Estimated compilability: {verification.estimated_compilability:.1f}%")

    section("STAGE 5: Output Summary")
    print(f"  {GREEN}Migration complete!{RESET}")
    print(f"  Generated files:")
    print(f"    - CalculatorForm.xaml ({len(xaml_output.xaml_content.splitlines())} lines)")
    print(f"    - CalculatorForm.xaml.cs ({len(xaml_output.code_behind.splitlines())} lines)")
    if mvvm_result and mvvm_result.viewmodel:
        print(f"    - ViewModel.cs ({len(mvvm_result.viewmodel.code.splitlines())} lines)")

def demo_full_experiment():
    """Run the full experiment suite and show results."""
    section("FULL EXPERIMENT: All 12 Apps x 3 Baselines")
    
    test_apps_dir = os.path.join(os.path.dirname(__file__), "test_apps")
    output_dir = os.path.join(os.path.dirname(__file__), "demo_output")
    
    apps = []
    for app_name in sorted(os.listdir(test_apps_dir)):
        app_path = os.path.join(test_apps_dir, app_name)
        if not os.path.isdir(app_path):
            continue
        for f in os.listdir(app_path):
            if f.endswith('.Designer.cs'):
                designer = os.path.join(app_path, f)
                cb = designer.replace('.Designer.cs', '.cs')
                apps.append({"name": app_name, "designer": designer, 
                           "code_behind": cb if os.path.exists(cb) else None})
    
    print(f"Found {len(apps)} test applications\n")
    
    for mode in ["rule_only", "single_agent", "hybrid"]:
        print(f"\n{BOLD}{YELLOW}Running: {mode.upper()}{RESET}")
        mode_output = os.path.join(output_dir, mode)
        pipeline = MigrationPipeline(output_dir=mode_output, mode=mode)
        
        for app in apps:
            try:
                metrics = pipeline.migrate_file(app["designer"], app.get("code_behind"))
                status = f"{GREEN}OK{RESET}" if metrics.csr > 70 else f"{RED}ISSUES{RESET}"
                print(f"  {app['name']:30s} CSR={metrics.csr:5.1f}%  MC={metrics.mc:5.1f}%  {status}")
            except Exception as e:
                print(f"  {app['name']:30s} {RED}ERROR: {e}{RESET}")
    
    print(f"\n{GREEN}{BOLD}Experiment complete! Check demo_output/ for all generated files.{RESET}")

if __name__ == "__main__":
    print(f"""
{BOLD}{BLUE}╔══════════════════════════════════════════════════════════════════╗
║  WinForms → WinUI 3 Migration Framework - LIVE DEMO            ║
║  Brijesharun G, Dr. Hariprasad S — SRM IST                     ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
    """)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        demo_full_experiment()
    else:
        demo_single_app()
        
        print(f"\n{BOLD}TIP: Run with --full to demo all 12 apps x 3 baselines{RESET}")
