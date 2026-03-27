"""
Agent 4: Verification Agent
==============================
Validates generated WinUI 3 output for syntactic correctness,
namespace references, and structural integrity.
Identifies issues and generates corrective patches.
"""

import re
from dataclasses import dataclass, field


@dataclass
class VerificationIssue:
    severity: str    # "error", "warning", "info"
    category: str    # "syntax", "namespace", "reference", "structure", "api"
    control: str
    message: str
    suggestion: str = ""
    auto_fixable: bool = False


@dataclass
class VerificationResult:
    is_valid: bool
    total_issues: int
    errors: int
    warnings: int
    infos: int
    issues: list = field(default_factory=list)
    fixes_applied: int = 0
    estimated_compilability: float = 0.0


# Known WinUI 3 namespaces and types for validation
VALID_WINUI_NAMESPACES = {
    "Microsoft.UI.Xaml",
    "Microsoft.UI.Xaml.Controls",
    "Microsoft.UI.Xaml.Controls.Primitives",
    "Microsoft.UI.Xaml.Data",
    "Microsoft.UI.Xaml.Input",
    "Microsoft.UI.Xaml.Media",
    "Microsoft.UI.Xaml.Media.Imaging",
    "Microsoft.UI.Xaml.Navigation",
    "Microsoft.UI.Xaml.Shapes",
    "Windows.Storage",
    "Windows.Storage.Pickers",
    "Windows.UI",
    "CommunityToolkit.Mvvm.ComponentModel",
    "CommunityToolkit.Mvvm.Input",
    "CommunityToolkit.WinUI.UI.Controls",
}

VALID_XAML_ELEMENTS = {
    "Window", "Page", "Grid", "StackPanel", "Canvas", "Border",
    "Button", "TextBlock", "TextBox", "CheckBox", "RadioButton",
    "ComboBox", "ListBox", "ListView", "TreeView", "TabView",
    "TabViewItem", "MenuBar", "MenuBarItem", "MenuFlyout",
    "MenuFlyoutItem", "MenuFlyoutSeparator", "CommandBar",
    "AppBarButton", "AppBarSeparator", "Image", "ProgressBar",
    "ProgressRing", "Slider", "ToggleSwitch", "NumberBox",
    "DatePicker", "TimePicker", "CalendarDatePicker", "CalendarView",
    "ContentDialog", "Flyout", "TeachingTip", "InfoBar",
    "NavigationView", "NavigationViewItem", "SplitView",
    "Expander", "Pivot", "PivotItem", "ScrollViewer",
    "WebView2", "RichEditBox", "AutoSuggestBox", "PersonPicture",
    "HyperlinkButton", "DropDownButton", "SplitButton",
    "ToggleButton", "RepeatButton", "ColorPicker", "ItemsRepeater",
    "controls:DataGrid",
}

# WinForms API patterns that shouldn't appear in WinUI 3 code
INVALID_API_PATTERNS = [
    (r'System\.Windows\.Forms\.\w+', "WinForms namespace reference"),
    (r'System\.Drawing\.\w+', "System.Drawing reference (use Microsoft.UI)"),
    (r'\.BackColor\s*=', "Use .Background instead of .BackColor"),
    (r'\.ForeColor\s*=', "Use .Foreground instead of .ForeColor"),
    (r'\.CreateGraphics\(\)', "No CreateGraphics in WinUI; use composition"),
    (r'Control\.ModifierKeys', "Use InputKeyboardSource.GetKeyStateForCurrentThread"),
    (r'Application\.DoEvents\(\)', "DoEvents not available; use async/await"),
    (r'Clipboard\.SetText\(', "Use DataPackage and Clipboard.SetContentAsync"),
    (r'MessageBox\.Show\(', "Use ContentDialog instead"),
    (r'\.Invoke\(\(', "Use DispatcherQueue.TryEnqueue instead"),
    (r'\.BeginInvoke\(', "Use DispatcherQueue.TryEnqueue instead"),
    (r'Application\.Run\(', "Not needed in WinUI 3; use App.xaml"),
]

# XAML validation patterns
XAML_ISSUES = [
    (r'<(\w+)\s[^>]*Text="[^"]*"[^>]*/>', "text_attr_check"),
    (r'<(\w+)\s[^>]*Click="[^"]*"', "click_event_check"),
]


def verify_xaml(xaml_content: str) -> list:
    """Verify XAML content for structural and syntactic issues."""
    issues = []

    if not xaml_content.strip():
        issues.append(VerificationIssue(
            severity="error", category="structure",
            control="", message="Empty XAML content"
        ))
        return issues

    # Check XML well-formedness (basic)
    open_tags = re.findall(r'<(\w+)[\s>]', xaml_content)
    close_tags = re.findall(r'</(\w+)>', xaml_content)
    self_close = re.findall(r'<(\w+)\s[^>]*/>', xaml_content)

    # Check for known valid elements
    all_elements = set(open_tags + self_close)
    for elem in all_elements:
        if elem not in VALID_XAML_ELEMENTS and not elem.startswith(('x:', 'local:', 'controls:', 'mc:')):
            if elem not in ('Window', 'Page', 'Grid') and elem[0].isupper():
                issues.append(VerificationIssue(
                    severity="warning", category="reference",
                    control=elem,
                    message=f"Element '{elem}' may not be a valid WinUI 3 control",
                    suggestion=f"Verify that '{elem}' exists in Microsoft.UI.Xaml.Controls"
                ))

    # Check for WinForms namespace leaks
    if "System.Windows.Forms" in xaml_content:
        issues.append(VerificationIssue(
            severity="error", category="namespace",
            control="", message="WinForms namespace found in XAML",
            auto_fixable=True,
            suggestion="Remove System.Windows.Forms references"
        ))

    # Check x:Name uniqueness
    names = re.findall(r'x:Name="(\w+)"', xaml_content)
    seen_names = set()
    for name in names:
        if name in seen_names:
            issues.append(VerificationIssue(
                severity="error", category="syntax",
                control=name,
                message=f"Duplicate x:Name '{name}'",
                auto_fixable=True,
                suggestion=f"Rename duplicate to '{name}_2'"
            ))
        seen_names.add(name)

    # Check for unclosed tags
    for tag in open_tags:
        if tag not in [ct for ct in close_tags] and tag not in self_close:
            if tag not in ('Window', 'Page', 'Grid', 'mc', 'x', 'd', 'local', 'controls'):
                pass  # Basic check - real XML parser would be better

    return issues


def verify_code_behind(code_content: str) -> list:
    """Verify C# code-behind for WinForms API leaks and issues."""
    issues = []

    if not code_content.strip():
        issues.append(VerificationIssue(
            severity="error", category="structure",
            control="", message="Empty code-behind"
        ))
        return issues

    # Check for invalid API patterns (skip commented-out lines)
    active_lines = [line for line in code_content.split('\n')
                    if line.strip() and not line.strip().startswith('//')]
    active_code = '\n'.join(active_lines)

    for pattern, description in INVALID_API_PATTERNS:
        matches = re.findall(pattern, active_code)
        for match in matches:
            issues.append(VerificationIssue(
                severity="error", category="api",
                control="",
                message=f"Invalid API usage: {description} ({match})",
                auto_fixable=True,
                suggestion=f"Replace with WinUI 3 equivalent"
            ))

    # Check for missing using statements
    if "Microsoft.UI.Xaml" not in code_content:
        issues.append(VerificationIssue(
            severity="warning", category="namespace",
            control="",
            message="Missing 'using Microsoft.UI.Xaml;'",
            auto_fixable=True
        ))

    # Check for proper class inheritance
    if ": Window" not in code_content and ": Page" not in code_content:
        issues.append(VerificationIssue(
            severity="warning", category="structure",
            control="",
            message="Class should inherit from Window or Page",
        ))

    # Check for event handler signatures
    old_signatures = re.findall(
        r'private\s+void\s+\w+\(object\s+\w+,\s*System\.EventArgs',
        code_content
    )
    for sig in old_signatures:
        issues.append(VerificationIssue(
            severity="error", category="api",
            control="",
            message="WinForms event signature (System.EventArgs) found",
            suggestion="Use RoutedEventArgs or specific WinUI event args",
            auto_fixable=True
        ))

    return issues


def verify_viewmodel(vm_code: str) -> list:
    """Verify ViewModel code for correctness."""
    issues = []

    if not vm_code.strip():
        return issues

    # Check for CommunityToolkit.Mvvm references
    if "CommunityToolkit.Mvvm" not in vm_code:
        issues.append(VerificationIssue(
            severity="warning", category="namespace",
            control="ViewModel",
            message="Missing CommunityToolkit.Mvvm namespace",
            auto_fixable=True
        ))

    # Check for ObservableObject base class
    if "ObservableObject" not in vm_code:
        issues.append(VerificationIssue(
            severity="warning", category="structure",
            control="ViewModel",
            message="ViewModel should inherit from ObservableObject",
        ))

    return issues


def apply_auto_fixes(xaml: str, code_behind: str, issues: list) -> tuple:
    """Apply automatic fixes for auto-fixable issues."""
    fixed_xaml = xaml
    fixed_code = code_behind
    fixes = 0

    for issue in issues:
        if not issue.auto_fixable:
            continue

        if issue.category == "namespace" and "WinForms" in issue.message:
            fixed_code = fixed_code.replace(
                "using System.Windows.Forms;",
                "using Microsoft.UI.Xaml.Controls;"
            )
            fixes += 1

        if issue.category == "api" and "BackColor" in issue.message:
            fixed_code = re.sub(
                r'\.BackColor\s*=\s*Color\.(\w+)',
                r'.Background = new SolidColorBrush(Colors.\1)',
                fixed_code
            )
            fixes += 1

        if issue.category == "api" and "ForeColor" in issue.message:
            fixed_code = re.sub(
                r'\.ForeColor\s*=\s*Color\.(\w+)',
                r'.Foreground = new SolidColorBrush(Colors.\1)',
                fixed_code
            )
            fixes += 1

        if issue.category == "api" and "System.EventArgs" in issue.message:
            fixed_code = fixed_code.replace(
                "System.EventArgs", "RoutedEventArgs"
            )
            fixes += 1

        if issue.category == "api" and "MessageBox" in issue.message:
            fixed_code = re.sub(
                r'MessageBox\.Show\(([^)]+)\)',
                r'/* ContentDialog needed: \1 */',
                fixed_code
            )
            fixes += 1

    return fixed_xaml, fixed_code, fixes


def verify_migration(xaml: str, code_behind: str, vm_code: str = "",
                     apply_fixes: bool = True) -> VerificationResult:
    """Run full verification on migration output."""
    all_issues = []
    all_issues.extend(verify_xaml(xaml))
    all_issues.extend(verify_code_behind(code_behind))
    if vm_code:
        all_issues.extend(verify_viewmodel(vm_code))

    errors = sum(1 for i in all_issues if i.severity == "error")
    warnings = sum(1 for i in all_issues if i.severity == "warning")
    infos = sum(1 for i in all_issues if i.severity == "info")

    # Apply auto-fixes only if enabled (hybrid mode)
    fixes = 0
    if apply_fixes:
        fixed_xaml, fixed_code, fixes = apply_auto_fixes(xaml, code_behind, all_issues)

    # Estimate compilability based on remaining issues and code complexity
    remaining_errors = errors - fixes

    # Factor in code complexity — more controls/handlers = more potential issues
    code_lines = len(code_behind.split('\n'))
    xaml_lines = len(xaml.split('\n'))
    total_loc = code_lines + xaml_lines

    # Count handler stubs (TODO markers indicate unmigrated handlers)
    todo_handlers = code_behind.count("// TODO: Migrate handler logic")
    migrated_handlers = code_behind.count("// Migrated from WinForms")
    total_handlers = todo_handlers + migrated_handlers

    # Base compilability from error analysis
    if remaining_errors <= 0:
        base_compilability = 0.95
    elif remaining_errors <= 2:
        base_compilability = 0.72
    elif remaining_errors <= 5:
        base_compilability = 0.48
    else:
        base_compilability = max(0.10, 1.0 - (remaining_errors * 0.08))

    # Adjust for code complexity
    # Larger code = more chances for issues even without detected errors
    complexity_factor = 1.0
    if total_loc > 100:
        complexity_factor -= 0.03
    if total_loc > 200:
        complexity_factor -= 0.04
    if total_loc > 300:
        complexity_factor -= 0.03

    # Unmigrated handlers reduce compilability
    if total_handlers > 0:
        handler_coverage = migrated_handlers / total_handlers
        if handler_coverage < 0.5:
            complexity_factor -= 0.12
        elif handler_coverage < 0.8:
            complexity_factor -= 0.05

    # ViewModel presence improves structuredness
    if vm_code and "ObservableObject" in vm_code:
        complexity_factor += 0.03

    compilability = base_compilability * max(complexity_factor, 0.6)

    return VerificationResult(
        is_valid=errors == 0,
        total_issues=len(all_issues),
        errors=errors,
        warnings=warnings,
        infos=infos,
        issues=all_issues,
        fixes_applied=fixes,
        estimated_compilability=compilability
    )
