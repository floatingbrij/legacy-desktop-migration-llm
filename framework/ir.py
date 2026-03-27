"""
Intermediate Representation (IR) Module
=========================================
Converts parsed WinForms structures into a framework-independent
JSON IR that decouples source framework from target.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class IRProperty:
    name: str
    value: str
    category: str  # "layout", "appearance", "behavior", "data"


@dataclass
class IREvent:
    event_type: str    # "click", "text_changed", "selection_changed", etc.
    handler_name: str
    handler_body: str
    complexity: str    # "simple", "moderate", "complex"


@dataclass
class IRControl:
    id: str
    control_category: str   # "button", "text_input", "label", "container", "list", etc.
    original_type: str      # WinForms type name
    name: str
    parent_id: str
    properties: list = field(default_factory=list)
    events: list = field(default_factory=list)
    children: list = field(default_factory=list)
    layout: dict = field(default_factory=dict)  # {x, y, width, height, anchor, dock}
    migration_difficulty: str = "simple"  # "simple", "moderate", "complex"


@dataclass
class IRForm:
    id: str
    class_name: str
    namespace: str
    title: str
    width: int
    height: int
    controls: list = field(default_factory=list)
    total_controls: int = 0
    total_events: int = 0
    complexity_tier: str = "small"  # "small", "medium", "large"


# WinForms control type → abstract category mapping
CONTROL_CATEGORIES = {
    "Button": "button",
    "Label": "text_display",
    "TextBox": "text_input",
    "RichTextBox": "text_input",
    "MaskedTextBox": "text_input",
    "ComboBox": "dropdown",
    "ListBox": "list",
    "ListView": "list",
    "TreeView": "tree",
    "DataGridView": "data_grid",
    "CheckBox": "checkbox",
    "RadioButton": "radio",
    "Panel": "container",
    "GroupBox": "container",
    "SplitContainer": "container",
    "TabControl": "tab_container",
    "TabPage": "tab_page",
    "FlowLayoutPanel": "flow_container",
    "TableLayoutPanel": "grid_container",
    "MenuStrip": "menu",
    "ToolStrip": "toolbar",
    "StatusStrip": "status_bar",
    "ContextMenuStrip": "context_menu",
    "PictureBox": "image",
    "ProgressBar": "progress",
    "TrackBar": "slider",
    "NumericUpDown": "numeric_input",
    "DateTimePicker": "date_picker",
    "MonthCalendar": "calendar",
    "Timer": "timer",
    "NotifyIcon": "notification",
    "ToolTip": "tooltip",
    "OpenFileDialog": "file_dialog",
    "SaveFileDialog": "file_dialog",
    "FolderBrowserDialog": "folder_dialog",
    "ColorDialog": "color_dialog",
    "FontDialog": "font_dialog",
    "PrintDialog": "print_dialog",
    "WebBrowser": "web_view",
    "Splitter": "splitter",
    "HScrollBar": "scrollbar",
    "VScrollBar": "scrollbar",
    "LinkLabel": "hyperlink",
    "CheckedListBox": "checked_list",
}

# Event type normalization
EVENT_TYPES = {
    "Click": "click",
    "DoubleClick": "double_click",
    "TextChanged": "text_changed",
    "SelectedIndexChanged": "selection_changed",
    "SelectedValueChanged": "selection_changed",
    "CheckedChanged": "checked_changed",
    "ValueChanged": "value_changed",
    "Scroll": "scroll",
    "KeyDown": "key_down",
    "KeyUp": "key_up",
    "KeyPress": "key_press",
    "MouseClick": "mouse_click",
    "MouseDown": "mouse_down",
    "MouseUp": "mouse_up",
    "MouseMove": "mouse_move",
    "MouseEnter": "mouse_enter",
    "MouseLeave": "mouse_leave",
    "Enter": "focus_enter",
    "Leave": "focus_leave",
    "GotFocus": "got_focus",
    "LostFocus": "lost_focus",
    "Load": "loaded",
    "FormClosing": "closing",
    "FormClosed": "closed",
    "Shown": "shown",
    "Resize": "resize",
    "Paint": "paint",
    "DragDrop": "drag_drop",
    "DragEnter": "drag_enter",
    "DragOver": "drag_over",
    "Tick": "timer_tick",
    "CellClick": "cell_click",
    "CellValueChanged": "cell_value_changed",
    "ColumnHeaderMouseClick": "column_header_click",
    "SelectionChanged": "selection_changed",
}


def classify_handler_complexity(handler_body: str) -> str:
    """Classify event handler complexity based on code content."""
    if not handler_body:
        return "simple"

    lines = [l.strip() for l in handler_body.split('\n') if l.strip() and not l.strip().startswith('//')]
    loc = len(lines)

    # Check for complex patterns
    has_db_access = any(kw in handler_body for kw in [
        "SqlConnection", "SqlCommand", "ExecuteReader", "DataAdapter",
        "DbContext", "Repository", "Entity"
    ])
    has_file_io = any(kw in handler_body for kw in [
        "File.Read", "File.Write", "StreamReader", "StreamWriter",
        "FileStream", "Directory."
    ])
    has_threading = any(kw in handler_body for kw in [
        "Thread", "Task.Run", "async", "await", "BackgroundWorker",
        "Invoke(", "BeginInvoke"
    ])
    has_ui_manipulation = any(kw in handler_body for kw in [
        "Controls.Add", "Controls.Remove", "new Form", "ShowDialog",
        "dynamic", "Reflection"
    ])
    has_loops = any(kw in handler_body for kw in [
        "for ", "foreach", "while ", "do {"
    ])

    complexity_score = 0
    if loc > 20:
        complexity_score += 2
    elif loc > 5:
        complexity_score += 1
    if has_db_access:
        complexity_score += 2
    if has_file_io:
        complexity_score += 1
    if has_threading:
        complexity_score += 2
    if has_ui_manipulation:
        complexity_score += 2
    if has_loops:
        complexity_score += 1

    if complexity_score >= 4:
        return "complex"
    elif complexity_score >= 2:
        return "moderate"
    return "simple"


def classify_migration_difficulty(ctrl_type: str, events: list, properties: list) -> str:
    """Classify how difficult a control is to migrate."""
    short_type = ctrl_type.split('.')[-1]

    # Controls with no direct WinUI 3 equivalent
    complex_types = {"DataGridView", "WebBrowser", "PropertyGrid", "DomainUpDown",
                     "MaskedTextBox", "PrintPreviewControl"}
    moderate_types = {"ListView", "TreeView", "TabControl", "SplitContainer",
                      "MenuStrip", "ToolStrip", "StatusStrip", "ContextMenuStrip",
                      "FlowLayoutPanel", "TableLayoutPanel"}

    if short_type in complex_types:
        return "complex"
    if short_type in moderate_types:
        return "moderate"

    # Check event complexity
    has_complex_events = any(
        classify_handler_complexity(e.handler_body) == "complex"
        for e in events if hasattr(e, 'handler_body')
    )
    if has_complex_events:
        return "complex"

    has_moderate_events = any(
        classify_handler_complexity(e.handler_body) == "moderate"
        for e in events if hasattr(e, 'handler_body')
    )
    if has_moderate_events:
        return "moderate"

    return "simple"


def winforms_to_ir(form) -> IRForm:
    """Convert a parsed WinForms FormInfo to IR."""
    ir_controls = []
    total_events = 0

    # Extract form dimensions
    form_width, form_height = 800, 600
    for prop in form.form_properties:
        if prop.name == "ClientSize" or prop.name == "Size":
            parts = prop.value.split(',')
            if len(parts) == 2:
                form_width, form_height = int(parts[0]), int(parts[1])

    form_title = ""
    for prop in form.form_properties:
        if prop.name == "Text":
            form_title = prop.value

    for ctrl in form.controls:
        short_type = ctrl.control_type.split('.')[-1]
        category = CONTROL_CATEGORIES.get(short_type, "unknown")

        # Extract layout info
        layout = {}
        ir_props = []
        for prop in ctrl.properties:
            if prop.name == "Location":
                parts = prop.value.split(',')
                if len(parts) == 2:
                    layout["x"] = int(parts[0])
                    layout["y"] = int(parts[1])
            elif prop.name == "Size":
                parts = prop.value.split(',')
                if len(parts) == 2:
                    layout["width"] = int(parts[0])
                    layout["height"] = int(parts[1])
            elif prop.name == "Anchor":
                layout["anchor"] = prop.value
            elif prop.name == "Dock":
                layout["dock"] = prop.value
            else:
                cat = "appearance"
                if prop.name in ("Text", "Name", "Tag"):
                    cat = "data"
                elif prop.name in ("Enabled", "Visible", "ReadOnly", "TabIndex"):
                    cat = "behavior"
                ir_props.append(IRProperty(prop.name, prop.value, cat))

        # Convert events
        ir_events = []
        for evt in ctrl.events:
            event_type = EVENT_TYPES.get(evt.event_name, evt.event_name.lower())
            body = getattr(evt, 'handler_body', '')
            complexity = classify_handler_complexity(body)
            ir_events.append(IREvent(event_type, evt.handler_name, body, complexity))
            total_events += 1

        difficulty = classify_migration_difficulty(
            ctrl.control_type,
            ctrl.events,
            ctrl.properties
        )

        ir_ctrl = IRControl(
            id=f"{form.class_name}_{ctrl.name}",
            control_category=category,
            original_type=ctrl.control_type,
            name=ctrl.name,
            parent_id=ctrl.parent or form.class_name,
            properties=ir_props,
            events=ir_events,
            children=ctrl.children,
            layout=layout,
            migration_difficulty=difficulty
        )
        ir_controls.append(ir_ctrl)

    # Determine complexity tier
    num_controls = len(ir_controls)
    if num_controls <= 5:
        tier = "small"
    elif num_controls <= 15:
        tier = "medium"
    else:
        tier = "large"

    return IRForm(
        id=f"{form.namespace}.{form.class_name}",
        class_name=form.class_name,
        namespace=form.namespace,
        title=form_title,
        width=form_width,
        height=form_height,
        controls=ir_controls,
        total_controls=num_controls,
        total_events=total_events,
        complexity_tier=tier
    )


def ir_to_json(ir_form: IRForm) -> str:
    """Serialize IR to JSON."""
    return json.dumps(asdict(ir_form), indent=2)


def ir_from_json(json_str: str) -> dict:
    """Deserialize IR from JSON (returns dict for flexibility)."""
    return json.loads(json_str)
