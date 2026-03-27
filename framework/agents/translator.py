"""
Agent 2: Translator Agent
===========================
Generates WinUI 3 XAML layouts and code-behind from the transformation plan.
Uses rule mappings for simple controls, template-based generation for
moderate complexity, and structured prompts for complex controls.
"""

import re
from dataclasses import dataclass, field

# Import from sibling modules
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules import CONTROL_RULES, transform_color, ANCHOR_TO_ALIGNMENT, DOCK_TO_ALIGNMENT


@dataclass
class XamlOutput:
    xaml_content: str
    code_behind: str
    controls_generated: int
    controls_skipped: int
    xaml_warnings: list = field(default_factory=list)


# XAML templates for WinUI 3 controls
XAML_TEMPLATES = {
    "Button": '<Button x:Name="{name}" Content="{text}" {layout} {events}/>',
    "TextBlock": '<TextBlock x:Name="{name}" Text="{text}" {layout}/>',
    "TextBox": '<TextBox x:Name="{name}" Text="{text}" PlaceholderText="{placeholder}" {layout} {events}/>',
    "CheckBox": '<CheckBox x:Name="{name}" Content="{text}" IsChecked="{checked}" {layout} {events}/>',
    "RadioButton": '<RadioButton x:Name="{name}" Content="{text}" IsChecked="{checked}" {layout} {events}/>',
    "ComboBox": '<ComboBox x:Name="{name}" {layout} {events}>\n{items}\n</ComboBox>',
    "ListBox": '<ListBox x:Name="{name}" {layout} {events}>\n{items}\n</ListBox>',
    "Image": '<Image x:Name="{name}" {layout}/>',
    "ProgressBar": '<ProgressBar x:Name="{name}" Value="{value}" Maximum="{max}" Minimum="{min}" {layout}/>',
    "Slider": '<Slider x:Name="{name}" Value="{value}" Maximum="{max}" Minimum="{min}" {layout}/>',
    "NumberBox": '<NumberBox x:Name="{name}" Value="{value}" Maximum="{max}" Minimum="{min}" {layout}/>',
    "DatePicker": '<DatePicker x:Name="{name}" {layout}/>',
    "HyperlinkButton": '<HyperlinkButton x:Name="{name}" Content="{text}" {layout} {events}/>',
    "RichEditBox": '<RichEditBox x:Name="{name}" {layout}/>',
    "Grid": None,  # Special handling
    "StackPanel": None,  # Special handling
    "TabView": None,  # Special handling
    "MenuBar": None,  # Special handling
    "CommandBar": None,  # Special handling
    "WebView2": '<WebView2 x:Name="{name}" {layout}/>',
    "InfoBar": '<InfoBar x:Name="{name}" {layout}/>',
    "Expander": '<Expander x:Name="{name}" Header="{text}" {layout}>\n    <Grid/>\n</Expander>',
    "SplitView": '<SplitView x:Name="{name}" {layout}>\n    <SplitView.Pane>\n        <Grid/>\n    </SplitView.Pane>\n    <Grid/>\n</SplitView>',
}

# WinUI 3 event names for code-behind wiring
EVENT_MAP = {
    "click": "Click",
    "double_click": "DoubleTapped",
    "text_changed": "TextChanged",
    "selection_changed": "SelectionChanged",
    "checked_changed": "Checked",
    "value_changed": "ValueChanged",
    "key_down": "KeyDown",
    "key_up": "KeyUp",
    "mouse_click": "Tapped",
    "mouse_enter": "PointerEntered",
    "mouse_leave": "PointerExited",
    "focus_enter": "GotFocus",
    "focus_leave": "LostFocus",
    "loaded": "Loaded",
    "closing": "Closed",
    "resize": "SizeChanged",
}


def get_property_value(ctrl: dict, prop_name: str, default: str = "") -> str:
    """Extract a property value from an IR control."""
    for prop in ctrl.get("properties", []):
        if prop.get("name") == prop_name:
            return prop.get("value", default)
    return default


def generate_layout_attrs(ctrl: dict) -> str:
    """Generate XAML layout attributes from IR layout info."""
    layout = ctrl.get("layout", {})
    attrs = []

    x = layout.get("x", 0)
    y = layout.get("y", 0)
    w = layout.get("width", 0)
    h = layout.get("height", 0)

    if w > 0:
        attrs.append(f'Width="{w}"')
    if h > 0:
        attrs.append(f'Height="{h}"')

    # Convert anchor to alignment
    anchor = layout.get("anchor", "")
    dock = layout.get("dock", "")

    if dock:
        ha, va = DOCK_TO_ALIGNMENT.get(dock, ("Left", "Top"))
        attrs.append(f'HorizontalAlignment="{ha}"')
        attrs.append(f'VerticalAlignment="{va}"')
    elif anchor:
        ha, va = ANCHOR_TO_ALIGNMENT.get(anchor, ("Left", "Top"))
        attrs.append(f'HorizontalAlignment="{ha}"')
        attrs.append(f'VerticalAlignment="{va}"')

    if x > 0 or y > 0:
        attrs.append(f'Margin="{x},{y},0,0"')

    return " ".join(attrs)


def generate_event_attrs(ctrl: dict) -> str:
    """Generate XAML event attributes."""
    attrs = []
    for evt in ctrl.get("events", []):
        event_type = evt.get("event_type", "")
        handler = evt.get("handler_name", "")
        winui_event = EVENT_MAP.get(event_type, event_type)
        if winui_event and handler:
            attrs.append(f'{winui_event}="{handler}"')
    return " ".join(attrs)


def generate_control_xaml(ctrl: dict, rule_result: dict, indent: int = 2) -> str:
    """Generate XAML for a single control."""
    prefix = "    " * indent
    original_type = ctrl.get("original_type", "")
    short_type = original_type.split('.')[-1]
    name = ctrl.get("name", "")

    rule = CONTROL_RULES.get(short_type)
    if not rule or not rule.xaml_tag:
        return f'{prefix}<!-- TODO: {short_type} "{name}" needs manual migration -->'

    xaml_tag = rule.xaml_tag

    text = get_property_value(ctrl, "Text", "")
    layout_attrs = generate_layout_attrs(ctrl)
    event_attrs = generate_event_attrs(ctrl)

    # Container controls with children
    if short_type in ("Panel", "GroupBox", "FlowLayoutPanel", "TableLayoutPanel"):
        children_xaml = []
        for child_name in ctrl.get("children", []):
            children_xaml.append(f'{prefix}    <!-- child: {child_name} -->')

        if short_type == "FlowLayoutPanel":
            orientation = "Horizontal"
            flow_dir = get_property_value(ctrl, "FlowDirection", "")
            if "TopDown" in flow_dir:
                orientation = "Vertical"
            inner = "\n".join(children_xaml) if children_xaml else ""
            return f'{prefix}<StackPanel x:Name="{name}" Orientation="{orientation}" {layout_attrs}>\n{inner}\n{prefix}</StackPanel>'

        if short_type == "GroupBox":
            inner = "\n".join(children_xaml) if children_xaml else f"{prefix}    <Grid/>"
            return f'{prefix}<Expander x:Name="{name}" Header="{text}" {layout_attrs}>\n{inner}\n{prefix}</Expander>'

        inner = "\n".join(children_xaml) if children_xaml else ""
        return f'{prefix}<Grid x:Name="{name}" {layout_attrs}>\n{inner}\n{prefix}</Grid>'

    # TabControl
    if short_type == "TabControl":
        return f'{prefix}<TabView x:Name="{name}" {layout_attrs}>\n{prefix}    <!-- TabViewItems -->\n{prefix}</TabView>'

    # MenuStrip
    if short_type == "MenuStrip":
        return f'{prefix}<MenuBar x:Name="{name}" {layout_attrs}>\n{prefix}    <!-- MenuBarItems -->\n{prefix}</MenuBar>'

    # ToolStrip
    if short_type == "ToolStrip":
        return f'{prefix}<CommandBar x:Name="{name}" {layout_attrs}>\n{prefix}    <!-- AppBarButtons -->\n{prefix}</CommandBar>'

    # Simple controls with templates
    template = XAML_TEMPLATES.get(xaml_tag)
    if template:
        # Build substitution dict
        subs = {
            "name": name,
            "text": text,
            "layout": layout_attrs,
            "events": event_attrs,
            "checked": get_property_value(ctrl, "Checked", "False"),
            "value": get_property_value(ctrl, "Value", "0"),
            "max": get_property_value(ctrl, "Maximum", "100"),
            "min": get_property_value(ctrl, "Minimum", "0"),
            "placeholder": "",
            "items": "",
        }
        # Clean up empty attributes
        result = template.format(**subs)
        result = re.sub(r'\s+/>', '/>', result)  # Clean trailing spaces before />
        result = re.sub(r'\s{2,}', ' ', result)
        return prefix + result.strip()

    # Fallback
    attrs = f'x:Name="{name}" {layout_attrs} {event_attrs}'.strip()
    return f'{prefix}<{xaml_tag} {attrs}/>'


def generate_xaml_page(ir_form: dict, rule_results: dict, plan=None,
                      migrate_handlers: bool = True) -> XamlOutput:
    """Generate a complete WinUI 3 XAML page from IR."""
    class_name = ir_form.get("class_name", "MainWindow")
    namespace = ir_form.get("namespace", "MigratedApp")
    title = ir_form.get("title", class_name)
    width = ir_form.get("width", 800)
    height = ir_form.get("height", 600)

    needs_toolkit = rule_results.get("toolkit_required", False)

    # Build XAML header
    xaml_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        f'<Window',
        f'    x:Class="{namespace}.{class_name}"',
        f'    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"',
        f'    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"',
        f'    xmlns:local="using:{namespace}"',
        f'    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"',
        f'    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"',
    ]
    if needs_toolkit:
        xaml_lines.append('    xmlns:controls="using:CommunityToolkit.WinUI.UI.Controls"')
    xaml_lines.append(f'    mc:Ignorable="d"')
    xaml_lines.append(f'    Title="{title}">')
    xaml_lines.append('')
    xaml_lines.append(f'    <Grid x:Name="RootGrid">')

    # Generate controls
    controls_generated = 0
    controls_skipped = 0
    warnings = []

    # Build rule results lookup
    rule_lookup = {}
    for tr in rule_results.get("transformations", []):
        rule_lookup[tr.get("control_name", "")] = tr

    # Get top-level controls (no parent or parent is form)
    top_level = []
    child_map = {}  # parent -> [children]
    for ctrl in ir_form.get("controls", []):
        parent = ctrl.get("parent_id", "")
        if not parent or parent == class_name:
            top_level.append(ctrl)
        else:
            child_map.setdefault(parent, []).append(ctrl)

    for ctrl in ir_form.get("controls", []):
        ctrl_name = ctrl.get("name", "")
        rule_result = rule_lookup.get(ctrl_name, {})
        original_type = ctrl.get("original_type", "").split('.')[-1]

        # Skip non-visual controls
        if original_type in ("Timer", "ToolTip", "NotifyIcon", "ImageList",
                           "BindingSource", "ErrorProvider"):
            continue

        try:
            xaml = generate_control_xaml(ctrl, rule_result, indent=2)
            xaml_lines.append(xaml)
            controls_generated += 1
        except Exception as e:
            xaml_lines.append(f'        <!-- ERROR: Could not generate {ctrl_name}: {e} -->')
            controls_skipped += 1
            warnings.append(f"Failed to generate {ctrl_name}: {e}")

    xaml_lines.append('    </Grid>')
    xaml_lines.append('</Window>')

    # Generate code-behind
    code_behind = generate_code_behind(ir_form, rule_results, namespace, class_name,
                                       migrate_handlers=migrate_handlers)

    return XamlOutput(
        xaml_content="\n".join(xaml_lines),
        code_behind=code_behind,
        controls_generated=controls_generated,
        controls_skipped=controls_skipped,
        xaml_warnings=warnings
    )


def generate_code_behind(ir_form: dict, rule_results: dict,
                         namespace: str, class_name: str,
                         migrate_handlers: bool = True) -> str:
    """Generate WinUI 3 code-behind (.xaml.cs) file."""
    lines = [
        "using Microsoft.UI.Xaml;",
        "using Microsoft.UI.Xaml.Controls;",
        "using Microsoft.UI.Xaml.Input;",
        "using Microsoft.UI.Xaml.Media;",
        "using System;",
        "using System.Collections.Generic;",
        "using System.Linq;",
        "",
        f"namespace {namespace}",
        "{",
        f"    public sealed partial class {class_name} : Window",
        "    {",
        f"        public {class_name}()",
        "        {",
        "            this.InitializeComponent();",
        "        }",
    ]

    # Generate event handler stubs (deduplicate shared handlers)
    seen_handlers = set()
    for ctrl in ir_form.get("controls", []):
        for evt in ctrl.get("events", []):
            handler_name = evt.get("handler_name", "")
            event_type = evt.get("event_type", "")
            body = evt.get("handler_body", "")

            if not handler_name or handler_name in seen_handlers:
                continue
            seen_handlers.add(handler_name)

            # Determine parameter types based on event
            if event_type in ("click",):
                params = "object sender, RoutedEventArgs e"
            elif event_type in ("text_changed",):
                params = "object sender, TextChangedEventArgs e"
            elif event_type in ("selection_changed",):
                params = "object sender, SelectionChangedEventArgs e"
            elif event_type in ("key_down", "key_up"):
                params = "object sender, KeyRoutedEventArgs e"
            elif event_type in ("mouse_click", "mouse_enter", "mouse_leave"):
                params = "object sender, PointerRoutedEventArgs e"
            elif event_type in ("loaded",):
                params = "object sender, RoutedEventArgs e"
            elif event_type in ("timer_tick",):
                params = "object sender, object e"
            else:
                params = "object sender, RoutedEventArgs e"

            lines.append("")
            if body and migrate_handlers:
                lines.append(f"        // Migrated from WinForms event handler")
                lines.append(f"        private void {handler_name}({params})")
                lines.append("        {")
                # Add migrated body (simplified - real LLM would transform API calls)
                migrated = migrate_handler_body(body)
                for ml in migrated.split('\n'):
                    lines.append(f"            {ml}")
                lines.append("        }")
            else:
                lines.append(f"        private void {handler_name}({params})")
                lines.append("        {")
                lines.append(f'            // TODO: Migrate handler logic')
                lines.append("        }")

    lines.append("    }")
    lines.append("}")

    return "\n".join(lines)


def migrate_handler_body(body: str) -> str:
    """Migrate WinForms API calls in handler body to WinUI 3 equivalents."""
    migrated = body

    # Common API transformations
    replacements = [
        ("MessageBox.Show(", "await ShowDialogAsync("),
        (".Text = ", ".Text = "),  # Same for TextBox
        (".Visible = true", ".Visibility = Visibility.Visible"),
        (".Visible = false", ".Visibility = Visibility.Collapsed"),
        (".Enabled = true", ".IsEnabled = true"),
        (".Enabled = false", ".IsEnabled = false"),
        ("this.Close()", "this.Close()"),
        (".BackColor = ", ".Background = new SolidColorBrush("),
        (".ForeColor = ", ".Foreground = new SolidColorBrush("),
        ("DialogResult.", "ContentDialogResult."),
    ]

    for old, new in replacements:
        migrated = migrated.replace(old, new)

    return migrated
