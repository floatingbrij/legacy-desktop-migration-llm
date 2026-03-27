"""
Agent 3: Refactoring Agent
============================
Converts WinForms event-driven patterns to MVVM architecture
using CommunityToolkit.MVVM (ObservableObject, RelayCommand, etc.)
"""

from dataclasses import dataclass, field
import re


@dataclass
class ViewModelClass:
    class_name: str
    namespace: str
    observable_properties: list = field(default_factory=list)
    commands: list = field(default_factory=list)
    code: str = ""


@dataclass
class ObservableProperty:
    name: str
    property_type: str
    initial_value: str = ""
    source_control: str = ""
    source_event: str = ""


@dataclass
class CommandDef:
    name: str
    execute_body: str
    can_execute_body: str = ""
    source_handler: str = ""
    is_async: bool = False


@dataclass
class MVVMRefactorResult:
    viewmodel: ViewModelClass = None
    binding_updates: list = field(default_factory=list)
    events_converted: int = 0
    events_kept: int = 0
    properties_converted: int = 0


def infer_property_type(handler_body: str, control_type: str) -> str:
    """Infer the property type from the handler body and control."""
    if not handler_body:
        return "string"

    if any(kw in handler_body for kw in [".Checked", "IsChecked", "bool "]):
        return "bool"
    if any(kw in handler_body for kw in [".Value", "int.", "Convert.ToInt"]):
        return "int"
    if any(kw in handler_body for kw in ["double.", "Convert.ToDouble", "decimal"]):
        return "double"
    if any(kw in handler_body for kw in ["DateTime", ".Date"]):
        return "DateTime"
    if "List<" in handler_body or "Collection<" in handler_body:
        return "ObservableCollection<object>"

    return "string"


def handler_to_command_body(handler_body: str) -> str:
    """Transform a WinForms event handler body into a command body."""
    if not handler_body:
        return "// TODO: Implement command logic"

    body = handler_body

    # Remove sender/e casts
    body = re.sub(r'\(\w+\)\s*sender', '', body)
    body = re.sub(r'var\s+\w+\s*=\s*sender\s+as\s+\w+;?\s*', '', body)

    # Replace direct control access with ViewModel property access
    body = re.sub(r'(\w+)\.Text\b', r'\1Text', body)
    body = re.sub(r'(\w+)\.Checked\b', r'Is\1Checked', body)
    body = re.sub(r'(\w+)\.SelectedIndex\b', r'\1SelectedIndex', body)
    body = re.sub(r'(\w+)\.Value\b', r'\1Value', body)

    # Replace Visible/Enabled
    body = body.replace('.Visible = true', 'IsVisible = true')
    body = body.replace('.Visible = false', 'IsVisible = false')
    body = body.replace('.Enabled = true', 'IsEnabled = true')
    body = body.replace('.Enabled = false', 'IsEnabled = false')

    # MessageBox → ContentDialog pattern
    body = re.sub(
        r'MessageBox\.Show\(([^)]+)\)',
        r'await ShowDialogAsync(\1)',
        body
    )

    return body


def handler_needs_async(handler_body: str) -> bool:
    """Check if handler should become async command."""
    if not handler_body:
        return False
    return any(kw in handler_body for kw in [
        "async", "await", "Task.", "MessageBox.Show(", "ShowDialog(",
        "File.ReadAll", "File.WriteAll", "HttpClient", "WebClient",
        "Stream", "Thread."
    ])


def create_viewmodel(form_id: str, class_name: str, namespace: str,
                     mvvm_candidates: list, ir_form: dict) -> MVVMRefactorResult:
    """Create a ViewModel class from MVVM candidates."""
    vm_name = f"{class_name}ViewModel"
    vm = ViewModelClass(class_name=vm_name, namespace=namespace)

    result = MVVMRefactorResult(viewmodel=vm)
    binding_updates = []

    # Track created properties to avoid duplicates
    created_props = set()
    created_commands = set()

    for candidate in mvvm_candidates:
        handler = candidate.get("handler", "")
        control = candidate.get("control", "")
        event = candidate.get("event", "")
        mvvm_type = candidate.get("mvvm_type", "")
        body = candidate.get("body", "")

        if mvvm_type == "RelayCommand":
            # Create command
            cmd_name = handler.replace("_Click", "").replace("_", "")
            if not cmd_name.endswith("Command"):
                cmd_name += "Command"

            if cmd_name not in created_commands:
                is_async = handler_needs_async(body)
                cmd_body = handler_to_command_body(body)

                cmd = CommandDef(
                    name=cmd_name,
                    execute_body=cmd_body,
                    source_handler=handler,
                    is_async=is_async,
                )
                vm.commands.append(cmd)
                created_commands.add(cmd_name)
                result.events_converted += 1

                binding_updates.append({
                    "control": control,
                    "old_event": event,
                    "new_binding": f'Command="{{Binding {cmd_name}}}"',
                    "type": "command"
                })

        elif mvvm_type == "ObservableProperty":
            # Create observable property
            prop_name = f"{control}Value"
            if prop_name not in created_props:
                prop_type = infer_property_type(body, control)
                prop = ObservableProperty(
                    name=prop_name,
                    property_type=prop_type,
                    source_control=control,
                    source_event=event,
                )
                vm.observable_properties.append(prop)
                created_props.add(prop_name)
                result.properties_converted += 1

                binding_updates.append({
                    "control": control,
                    "old_event": event,
                    "new_binding": f'Text="{{Binding {prop_name}, Mode=TwoWay}}"',
                    "type": "property"
                })

    result.binding_updates = binding_updates

    # Generate ViewModel code
    vm.code = generate_viewmodel_code(vm)

    return result


def generate_viewmodel_code(vm: ViewModelClass) -> str:
    """Generate C# code for the ViewModel."""
    lines = [
        "using CommunityToolkit.Mvvm.ComponentModel;",
        "using CommunityToolkit.Mvvm.Input;",
        "using System;",
        "using System.Collections.ObjectModel;",
        "using System.Threading.Tasks;",
        "",
        f"namespace {vm.namespace}",
        "{",
        f"    public partial class {vm.class_name} : ObservableObject",
        "    {",
    ]

    # Generate observable properties
    for prop in vm.observable_properties:
        lines.append(f"        [ObservableProperty]")
        lines.append(f"        private {prop.property_type} _{prop.name[0].lower()}{prop.name[1:]};")
        lines.append("")

    # Generate commands
    for cmd in vm.commands:
        if cmd.is_async:
            lines.append(f"        [RelayCommand]")
            lines.append(f"        private async Task {cmd.name.replace('Command', '')}Async()")
            lines.append("        {")
            for body_line in cmd.execute_body.split('\n'):
                lines.append(f"            {body_line.strip()}")
            lines.append("        }")
        else:
            lines.append(f"        [RelayCommand]")
            lines.append(f"        private void {cmd.name.replace('Command', '')}()")
            lines.append("        {")
            for body_line in cmd.execute_body.split('\n'):
                lines.append(f"            {body_line.strip()}")
            lines.append("        }")
        lines.append("")

    lines.append("    }")
    lines.append("}")

    return "\n".join(lines)
