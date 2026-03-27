"""
Rule-Based Transformation Engine
==================================
Deterministic control mapping rules for WinForms → WinUI 3 conversion.
Handles the 20 core control mappings and property transformations.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TransformResult:
    winui3_type: str           # WinUI 3 control type
    winui3_namespace: str      # WinUI 3 namespace
    xaml_tag: str              # XAML element name
    property_maps: dict = field(default_factory=dict)  # old_prop -> new_prop
    property_transforms: dict = field(default_factory=dict)  # prop -> transform func name
    requires_toolkit: bool = False
    requires_agent: bool = False  # Needs LLM agent for complex transformation
    notes: str = ""
    confidence: float = 1.0    # 0-1, how confident the rule mapping is


# === CORE CONTROL MAPPING RULES ===
CONTROL_RULES = {
    "Button": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.Button",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="Button",
        property_maps={"Text": "Content", "FlatStyle": None, "DialogResult": None},
        confidence=0.95,
        notes="Text→Content; FlatStyle/DialogResult dropped"
    ),
    "Label": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.TextBlock",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="TextBlock",
        property_maps={"Text": "Text", "AutoSize": None, "BorderStyle": None},
        confidence=0.95,
        notes="Direct mapping; AutoSize not needed in XAML"
    ),
    "TextBox": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.TextBox",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="TextBox",
        property_maps={"Text": "Text", "Multiline": None, "ScrollBars": None,
                       "ReadOnly": "IsReadOnly", "MaxLength": "MaxLength",
                       "PasswordChar": None},
        property_transforms={"Multiline": "check_multiline"},
        confidence=0.90,
        notes="Multiline TextBox → TextBox with AcceptsReturn; PasswordChar → PasswordBox"
    ),
    "RichTextBox": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.RichEditBox",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="RichEditBox",
        property_maps={"Text": None, "ReadOnly": "IsReadOnly"},
        confidence=0.70,
        requires_agent=True,
        notes="API differences significant; text manipulation needs agent"
    ),
    "ComboBox": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.ComboBox",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="ComboBox",
        property_maps={"Items": "Items", "SelectedIndex": "SelectedIndex",
                       "DropDownStyle": None, "Text": None},
        confidence=0.85,
        notes="Items need ItemsSource binding in MVVM; DropDownStyle→IsEditable"
    ),
    "ListBox": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.ListBox",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="ListBox",
        property_maps={"Items": "Items", "SelectedIndex": "SelectedIndex",
                       "SelectionMode": "SelectionMode"},
        confidence=0.85,
    ),
    "CheckBox": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.CheckBox",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="CheckBox",
        property_maps={"Text": "Content", "Checked": "IsChecked",
                       "CheckState": "IsChecked"},
        confidence=0.95,
    ),
    "RadioButton": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.RadioButton",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="RadioButton",
        property_maps={"Text": "Content", "Checked": "IsChecked"},
        confidence=0.95,
    ),
    "Panel": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.Grid",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="Grid",
        property_maps={"AutoScroll": None, "BorderStyle": "BorderBrush"},
        property_transforms={"children_layout": "position_to_grid"},
        confidence=0.80,
        notes="Absolute positioning → Grid rows/columns"
    ),
    "GroupBox": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.Expander",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="Expander",
        property_maps={"Text": "Header"},
        confidence=0.70,
        notes="No direct equivalent; Expander or Border with Header"
    ),
    "FlowLayoutPanel": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.StackPanel",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="StackPanel",
        property_maps={"FlowDirection": "Orientation"},
        confidence=0.85,
    ),
    "TableLayoutPanel": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.Grid",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="Grid",
        property_maps={},
        property_transforms={"rows_cols": "table_to_grid_defs"},
        confidence=0.80,
    ),
    "TabControl": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.TabView",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="TabView",
        property_maps={"TabPages": "TabItems"},
        confidence=0.75,
        notes="TabPages→TabViewItem; content restructuring needed"
    ),
    "SplitContainer": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.SplitView",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="SplitView",
        property_maps={"Orientation": "PanePlacement", "SplitterDistance": "OpenPaneLength"},
        confidence=0.65,
        requires_agent=True,
        notes="Significant API differences"
    ),
    "ListView": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.ListView",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="ListView",
        property_maps={"View": None, "Columns": None},
        requires_agent=True,
        confidence=0.60,
        notes="WinForms ListView (Details view with columns) very different from WinUI ListView"
    ),
    "TreeView": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.TreeView",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="TreeView",
        property_maps={"Nodes": "RootNodes"},
        confidence=0.70,
        requires_agent=True,
    ),
    "DataGridView": TransformResult(
        winui3_type="CommunityToolkit.WinUI.UI.Controls.DataGrid",
        winui3_namespace="CommunityToolkit.WinUI.UI.Controls",
        xaml_tag="controls:DataGrid",
        property_maps={"DataSource": "ItemsSource", "Columns": "Columns"},
        requires_toolkit=True,
        requires_agent=True,
        confidence=0.55,
        notes="Requires CommunityToolkit; column definition restructuring"
    ),
    "MenuStrip": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.MenuBar",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="MenuBar",
        property_maps={"Items": "Items"},
        confidence=0.75,
        notes="ToolStripMenuItem→MenuBarItem/MenuFlyoutItem"
    ),
    "ToolStrip": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.CommandBar",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="CommandBar",
        property_maps={"Items": "PrimaryCommands"},
        confidence=0.70,
    ),
    "StatusStrip": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.InfoBar",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="InfoBar",
        confidence=0.50,
        requires_agent=True,
        notes="No direct equivalent; custom implementation needed"
    ),
    "PictureBox": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.Image",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="Image",
        property_maps={"Image": "Source", "SizeMode": "Stretch"},
        confidence=0.80,
    ),
    "ProgressBar": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.ProgressBar",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="ProgressBar",
        property_maps={"Value": "Value", "Maximum": "Maximum", "Minimum": "Minimum",
                       "Style": None},
        confidence=0.95,
    ),
    "TrackBar": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.Slider",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="Slider",
        property_maps={"Value": "Value", "Maximum": "Maximum", "Minimum": "Minimum",
                       "TickFrequency": "TickFrequency"},
        confidence=0.90,
    ),
    "NumericUpDown": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.NumberBox",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="NumberBox",
        property_maps={"Value": "Value", "Maximum": "Maximum", "Minimum": "Minimum",
                       "DecimalPlaces": None, "Increment": "SmallChange"},
        confidence=0.85,
    ),
    "DateTimePicker": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.DatePicker",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="DatePicker",
        property_maps={"Value": "Date", "Format": None},
        confidence=0.75,
        notes="Time component → TimePicker; custom format needs agent"
    ),
    "Timer": TransformResult(
        winui3_type="Microsoft.UI.Xaml.DispatcherTimer",
        winui3_namespace="Microsoft.UI.Xaml",
        xaml_tag=None,  # Not a XAML element
        property_maps={"Interval": "Interval", "Enabled": None},
        confidence=0.90,
        notes="Namespace change; Interval int→TimeSpan"
    ),
    "ToolTip": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.ToolTip",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="ToolTip",
        property_maps={},
        confidence=0.85,
        notes="Attached property pattern: ToolTipService.ToolTip"
    ),
    "LinkLabel": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.HyperlinkButton",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="HyperlinkButton",
        property_maps={"Text": "Content"},
        confidence=0.80,
    ),
    "NotifyIcon": TransformResult(
        winui3_type=None,
        winui3_namespace=None,
        xaml_tag=None,
        confidence=0.20,
        requires_agent=True,
        notes="No WinUI 3 equivalent; needs Windows API (H.NotifyIcon or AppNotificationManager)"
    ),
    "WebBrowser": TransformResult(
        winui3_type="Microsoft.UI.Xaml.Controls.WebView2",
        winui3_namespace="Microsoft.UI.Xaml.Controls",
        xaml_tag="WebView2",
        property_maps={"Url": "Source"},
        confidence=0.65,
        requires_agent=True,
        notes="WebBrowser→WebView2; significant API differences"
    ),
}

# Property value transformations
COLOR_MAP = {
    "Control": "Transparent",
    "Window": "White",
    "WindowText": "Black",
    "ControlText": "Black",
    "ActiveCaption": "{ThemeResource SystemAccentColor}",
    "Highlight": "{ThemeResource SystemAccentColor}",
    "GrayText": "Gray",
    "ButtonFace": "Transparent",
    "ButtonHighlight": "{ThemeResource SystemAccentColor}",
    "Red": "Red", "Blue": "Blue", "Green": "Green",
    "White": "White", "Black": "Black", "Gray": "Gray",
    "Yellow": "Yellow", "Orange": "Orange", "Purple": "Purple",
}

ANCHOR_TO_ALIGNMENT = {
    "Top, Left": ("Left", "Top"),
    "Top, Right": ("Right", "Top"),
    "Bottom, Left": ("Left", "Bottom"),
    "Bottom, Right": ("Right", "Bottom"),
    "Top, Left, Right": ("Stretch", "Top"),
    "Bottom, Left, Right": ("Stretch", "Bottom"),
    "Top, Bottom, Left": ("Left", "Stretch"),
    "Top, Bottom, Right": ("Right", "Stretch"),
    "Top, Bottom, Left, Right": ("Stretch", "Stretch"),
}

DOCK_TO_ALIGNMENT = {
    "System.Windows.Forms.DockStyle.Top": ("Stretch", "Top"),
    "System.Windows.Forms.DockStyle.Bottom": ("Stretch", "Bottom"),
    "System.Windows.Forms.DockStyle.Left": ("Left", "Stretch"),
    "System.Windows.Forms.DockStyle.Right": ("Right", "Stretch"),
    "System.Windows.Forms.DockStyle.Fill": ("Stretch", "Stretch"),
    "DockStyle.Top": ("Stretch", "Top"),
    "DockStyle.Bottom": ("Stretch", "Bottom"),
    "DockStyle.Left": ("Left", "Stretch"),
    "DockStyle.Right": ("Right", "Stretch"),
    "DockStyle.Fill": ("Stretch", "Stretch"),
}

EVENT_TO_WINUI = {
    "click": "Click",
    "double_click": "DoubleTapped",
    "text_changed": "TextChanged",
    "selection_changed": "SelectionChanged",
    "checked_changed": "Checked",  # + Unchecked
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
    "timer_tick": "Tick",
}


def get_rule(control_type: str) -> Optional[TransformResult]:
    """Look up rule for a WinForms control type."""
    short_type = control_type.split('.')[-1]
    return CONTROL_RULES.get(short_type)


def transform_property(prop_name: str, prop_value: str, rule: TransformResult) -> tuple:
    """Transform a WinForms property to WinUI 3 equivalent.
    Returns (new_name, new_value) or (None, None) if property is dropped."""
    mapped_name = rule.property_maps.get(prop_name)
    if mapped_name is None and prop_name in rule.property_maps:
        return (None, None)  # Explicitly dropped

    if mapped_name:
        return (mapped_name, prop_value)

    # Default: keep same name
    return (prop_name, prop_value)


def transform_color(color_name: str) -> str:
    """Transform WinForms system color to WinUI 3 equivalent."""
    return COLOR_MAP.get(color_name, color_name)


def transform_event(event_type: str) -> str:
    """Transform WinForms event to WinUI 3 equivalent."""
    return EVENT_TO_WINUI.get(event_type, event_type)


def apply_rules(ir_form: dict) -> dict:
    """Apply rule-based transformations to an IR form.
    Returns transformation results with statistics."""
    results = {
        "form_id": ir_form.get("id", ""),
        "total_controls": 0,
        "rule_mapped": 0,
        "agent_needed": 0,
        "unmapped": 0,
        "total_properties": 0,
        "properties_mapped": 0,
        "properties_dropped": 0,
        "total_events": 0,
        "events_mapped": 0,
        "toolkit_required": False,
        "transformations": [],
    }

    for ctrl in ir_form.get("controls", []):
        results["total_controls"] += 1
        original_type = ctrl.get("original_type", "")
        rule = get_rule(original_type)

        ctrl_result = {
            "control_name": ctrl.get("name", ""),
            "original_type": original_type,
            "status": "unmapped",
            "winui3_type": None,
            "xaml_tag": None,
            "property_mappings": [],
            "event_mappings": [],
            "confidence": 0,
            "notes": "",
        }

        if rule:
            ctrl_result["status"] = "agent_needed" if rule.requires_agent else "rule_mapped"
            ctrl_result["winui3_type"] = rule.winui3_type
            ctrl_result["xaml_tag"] = rule.xaml_tag
            ctrl_result["confidence"] = rule.confidence
            ctrl_result["notes"] = rule.notes

            if rule.requires_toolkit:
                results["toolkit_required"] = True

            if rule.requires_agent:
                results["agent_needed"] += 1
            else:
                results["rule_mapped"] += 1

            # Map properties
            for prop in ctrl.get("properties", []):
                results["total_properties"] += 1
                new_name, new_value = transform_property(
                    prop.get("name", ""), prop.get("value", ""), rule
                )
                if new_name:
                    results["properties_mapped"] += 1
                    ctrl_result["property_mappings"].append({
                        "old": prop.get("name"), "new": new_name,
                        "old_value": prop.get("value"), "new_value": new_value
                    })
                else:
                    results["properties_dropped"] += 1

            # Map events
            for evt in ctrl.get("events", []):
                results["total_events"] += 1
                new_event = transform_event(evt.get("event_type", ""))
                results["events_mapped"] += 1
                ctrl_result["event_mappings"].append({
                    "old": evt.get("event_type"), "new": new_event,
                    "handler": evt.get("handler_name"),
                    "complexity": evt.get("complexity", "simple")
                })
        else:
            results["unmapped"] += 1
            ctrl_result["notes"] = "No mapping rule available"

        results["transformations"].append(ctrl_result)

    return results
