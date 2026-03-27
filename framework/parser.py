"""
WinForms Static Analysis Parser
================================
Parses .Designer.cs files to extract control hierarchy, properties,
event bindings, and layout information from WinForms source code.
Also parses code-behind (.cs) files for event handler implementations.
"""

import re
import os
import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ControlProperty:
    name: str
    value: str
    value_type: str  # "string", "int", "point", "size", "enum", "color", "bool", "font"


@dataclass
class EventBinding:
    event_name: str       # e.g., "Click"
    handler_name: str     # e.g., "button1_Click"
    handler_body: str = ""  # actual method implementation from .cs


@dataclass
class WinFormsControl:
    control_type: str          # e.g., "System.Windows.Forms.Button"
    name: str                  # e.g., "button1"
    parent: str = ""           # parent control name
    properties: list = field(default_factory=list)
    events: list = field(default_factory=list)
    children: list = field(default_factory=list)


@dataclass
class FormInfo:
    class_name: str
    namespace: str
    base_class: str  # e.g., "Form"
    controls: list = field(default_factory=list)
    form_properties: list = field(default_factory=list)
    resources: list = field(default_factory=list)
    event_handlers: dict = field(default_factory=dict)


# Regex patterns for parsing .Designer.cs files
PATTERNS = {
    "namespace": re.compile(r'namespace\s+([\w.]+)'),
    "class_decl": re.compile(r'partial\s+class\s+(\w+)(?:\s*:\s*(\w+))?'),
    "control_decl": re.compile(r'this\.(\w+)\s*=\s*new\s+([\w.]+)\s*\(\s*\)'),
    "property_string": re.compile(r'this\.(\w+)\.(\w+)\s*=\s*"([^"]*)"'),
    "property_bool": re.compile(r'this\.(\w+)\.(\w+)\s*=\s*(true|false)'),
    "property_int": re.compile(r'this\.(\w+)\.(\w+)\s*=\s*(\d+)'),
    "property_point": re.compile(r'this\.(\w+)\.(\w+)\s*=\s*new\s+System\.Drawing\.Point\((\d+),\s*(\d+)\)'),
    "property_size": re.compile(r'this\.(\w+)\.(\w+)\s*=\s*new\s+System\.Drawing\.Size\((\d+),\s*(\d+)\)'),
    "property_enum": re.compile(r'this\.(\w+)\.(\w+)\s*=\s*([\w.]+\.[\w.]+)'),
    "property_color": re.compile(r'this\.(\w+)\.(\w+)\s*=\s*System\.Drawing\.Color\.(\w+)'),
    "property_font": re.compile(r'this\.(\w+)\.(\w+)\s*=\s*new\s+System\.Drawing\.Font\("([^"]+)",\s*(\d+\.?\d*)F?'),
    "event_binding": re.compile(r'this\.(\w+)\.(\w+)\s*\+=\s*new\s+[\w.]+\(this\.(\w+)\)'),
    "event_binding_short": re.compile(r'this\.(\w+)\.(\w+)\s*\+=\s*(?:new\s+[\w.]+\()?\s*this\.(\w+)\)?'),
    "controls_add": re.compile(r'this\.(\w+)\.Controls\.Add\(this\.(\w+)\)'),
    "suspend_layout": re.compile(r'this\.(\w+)\.SuspendLayout'),
    "tab_index": re.compile(r'this\.(\w+)\.TabIndex\s*=\s*(\d+)'),
    "anchor": re.compile(r'this\.(\w+)\.Anchor\s*=\s*(.+?);'),
    "dock": re.compile(r'this\.(\w+)\.Dock\s*=\s*(.+?);'),
    "items_add": re.compile(r'this\.(\w+)\.\w*Items\.AddRange\(new\s+object\[\]'),
}

# Regex for parsing code-behind event handlers
EVENT_HANDLER_PATTERN = re.compile(
    r'private\s+void\s+(\w+)\s*\(object\s+\w+,\s*\w+\s+\w+\)\s*\{',
    re.MULTILINE
)


def parse_designer_cs(file_path: str) -> FormInfo:
    """Parse a .Designer.cs file and extract all WinForms UI structure."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    form = FormInfo(class_name="", namespace="", base_class="Form")
    controls = {}  # name -> WinFormsControl
    parent_map = {}  # child -> parent

    # Extract namespace
    ns_match = PATTERNS["namespace"].search(content)
    if ns_match:
        form.namespace = ns_match.group(1)

    # Extract class declaration
    cls_match = PATTERNS["class_decl"].search(content)
    if cls_match:
        form.class_name = cls_match.group(1)
        form.base_class = cls_match.group(2) or "Form"

    # Extract control declarations (this.X = new Type())
    for m in PATTERNS["control_decl"].finditer(content):
        ctrl_name = m.group(1)
        ctrl_type = m.group(2)
        controls[ctrl_name] = WinFormsControl(
            control_type=ctrl_type,
            name=ctrl_name
        )

    # Extract string properties
    for m in PATTERNS["property_string"].finditer(content):
        ctrl_name, prop_name, value = m.group(1), m.group(2), m.group(3)
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty(prop_name, value, "string")
            )
        elif ctrl_name == form.class_name or ctrl_name == "":
            form.form_properties.append(
                ControlProperty(prop_name, value, "string")
            )

    # Extract boolean properties
    for m in PATTERNS["property_bool"].finditer(content):
        ctrl_name, prop_name, value = m.group(1), m.group(2), m.group(3)
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty(prop_name, value, "bool")
            )

    # Extract integer properties
    for m in PATTERNS["property_int"].finditer(content):
        ctrl_name, prop_name, value = m.group(1), m.group(2), m.group(3)
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty(prop_name, value, "int")
            )

    # Extract Point properties (Location)
    for m in PATTERNS["property_point"].finditer(content):
        ctrl_name, prop_name = m.group(1), m.group(2)
        x, y = m.group(3), m.group(4)
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty(prop_name, f"{x},{y}", "point")
            )

    # Extract Size properties
    for m in PATTERNS["property_size"].finditer(content):
        ctrl_name, prop_name = m.group(1), m.group(2)
        w, h = m.group(3), m.group(4)
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty(prop_name, f"{w},{h}", "size")
            )

    # Extract enum properties
    for m in PATTERNS["property_enum"].finditer(content):
        ctrl_name, prop_name, value = m.group(1), m.group(2), m.group(3)
        if ctrl_name in controls and prop_name not in ("SuspendLayout", "ResumeLayout"):
            controls[ctrl_name].properties.append(
                ControlProperty(prop_name, value, "enum")
            )

    # Extract Color properties
    for m in PATTERNS["property_color"].finditer(content):
        ctrl_name, prop_name, value = m.group(1), m.group(2), m.group(3)
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty(prop_name, value, "color")
            )

    # Extract Font properties
    for m in PATTERNS["property_font"].finditer(content):
        ctrl_name, prop_name, font_name, font_size = (
            m.group(1), m.group(2), m.group(3), m.group(4)
        )
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty(prop_name, f"{font_name},{font_size}", "font")
            )

    # Extract event bindings
    for m in PATTERNS["event_binding_short"].finditer(content):
        ctrl_name, event_name, handler_name = m.group(1), m.group(2), m.group(3)
        if ctrl_name in controls:
            controls[ctrl_name].events.append(
                EventBinding(event_name, handler_name)
            )

    # Extract parent-child relationships (Controls.Add)
    for m in PATTERNS["controls_add"].finditer(content):
        parent_name, child_name = m.group(1), m.group(2)
        parent_map[child_name] = parent_name

    # Assign parents
    for child_name, parent_name in parent_map.items():
        if child_name in controls:
            controls[child_name].parent = parent_name
        if parent_name in controls:
            controls[parent_name].children.append(child_name)

    # Extract Anchor and Dock properties
    for m in PATTERNS["anchor"].finditer(content):
        ctrl_name, value = m.group(1), m.group(2).strip()
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty("Anchor", value, "enum")
            )

    for m in PATTERNS["dock"].finditer(content):
        ctrl_name, value = m.group(1), m.group(2).strip()
        if ctrl_name in controls:
            controls[ctrl_name].properties.append(
                ControlProperty("Dock", value, "enum")
            )

    form.controls = list(controls.values())
    return form


def parse_code_behind(file_path: str) -> dict:
    """Parse a .cs code-behind file to extract event handler implementations."""
    handlers = {}
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except (FileNotFoundError, PermissionError):
        return handlers

    # Find all event handler methods
    for m in EVENT_HANDLER_PATTERN.finditer(content):
        handler_name = m.group(1)
        start = m.end()
        # Extract method body by tracking braces
        brace_count = 1
        pos = start
        while pos < len(content) and brace_count > 0:
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
            pos += 1
        handlers[handler_name] = content[start:pos - 1].strip()

    return handlers


def parse_project(project_dir: str) -> list:
    """Parse all forms in a WinForms project directory."""
    forms = []
    designer_files = []

    for root, dirs, files in os.walk(project_dir):
        for f in files:
            if f.endswith('.Designer.cs'):
                designer_files.append(os.path.join(root, f))

    for designer_path in designer_files:
        form = parse_designer_cs(designer_path)

        # Find matching code-behind
        code_behind = designer_path.replace('.Designer.cs', '.cs')
        if os.path.exists(code_behind):
            handlers = parse_code_behind(code_behind)
            form.event_handlers = handlers
            # Attach handler bodies to event bindings
            for ctrl in form.controls:
                for evt in ctrl.events:
                    if evt.handler_name in handlers:
                        evt.handler_body = handlers[evt.handler_name]

        forms.append(form)

    return forms


def count_controls(forms: list) -> dict:
    """Count control types across all forms."""
    counts = {}
    for form in forms:
        for ctrl in form.controls:
            short_type = ctrl.control_type.split('.')[-1]
            counts[short_type] = counts.get(short_type, 0) + 1
    return counts


def count_events(forms: list) -> int:
    """Count total event bindings across all forms."""
    total = 0
    for form in forms:
        for ctrl in form.controls:
            total += len(ctrl.events)
    return total


def count_properties(forms: list) -> int:
    """Count total properties across all forms."""
    total = 0
    for form in forms:
        for ctrl in form.controls:
            total += len(ctrl.properties)
    return total


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parser.py <designer_cs_file_or_directory>")
        sys.exit(1)

    path = sys.argv[1]
    if os.path.isdir(path):
        forms = parse_project(path)
        for form in forms:
            print(f"\nForm: {form.namespace}.{form.class_name} (base: {form.base_class})")
            print(f"  Controls: {len(form.controls)}")
            print(f"  Event handlers: {len(form.event_handlers)}")
            for ctrl in form.controls:
                print(f"    {ctrl.control_type} '{ctrl.name}' - {len(ctrl.properties)} props, {len(ctrl.events)} events")
        print(f"\nControl type counts: {count_controls(forms)}")
    else:
        form = parse_designer_cs(path)
        print(json.dumps(asdict(form), indent=2))
