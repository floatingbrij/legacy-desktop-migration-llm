"""
Agent 1: Analyzer Agent
========================
Identifies complex patterns in parsed WinForms code and creates
a transformation plan specifying which components need LLM-assisted
generation vs. rule-based mapping.
"""

from dataclasses import dataclass, field


@dataclass
class AnalysisResult:
    control_name: str
    original_type: str
    patterns_detected: list = field(default_factory=list)
    transformation_strategy: str = "rule"  # "rule", "template", "llm"
    difficulty: str = "simple"
    notes: str = ""


@dataclass
class TransformationPlan:
    form_id: str
    total_controls: int
    rule_controls: int
    template_controls: int
    llm_controls: int
    analyses: list = field(default_factory=list)
    detected_patterns: list = field(default_factory=list)
    mvvm_candidates: list = field(default_factory=list)


# Complex pattern detectors
COMPLEX_PATTERNS = {
    "dynamic_ui": [
        "Controls.Add(", "Controls.Remove(", "new Panel(", "new Button(",
        "Controls.Clear(", "SuspendLayout()", "ResumeLayout("
    ],
    "custom_painting": [
        "OnPaint(", "CreateGraphics()", "Graphics ", "DrawString(",
        "DrawImage(", "FillRectangle(", "DrawLine(", "e.Graphics"
    ],
    "data_binding": [
        "DataSource", "BindingSource", "DataMember", "DataBindings.Add(",
        "BindingContext", "CurrencyManager"
    ],
    "threading": [
        "Thread(", "Task.Run(", "BackgroundWorker", "async ", "await ",
        "Invoke((", "BeginInvoke(", "InvokeRequired"
    ],
    "file_io": [
        "File.Read", "File.Write", "StreamReader", "StreamWriter",
        "FileStream", "Directory.", "Path.Combine("
    ],
    "dialog_interaction": [
        "ShowDialog()", "DialogResult", "MessageBox.Show(",
        "OpenFileDialog", "SaveFileDialog", "FolderBrowserDialog"
    ],
    "mdi": [
        "IsMdiContainer", "MdiParent", "MdiChildren", "LayoutMdi("
    ],
    "drag_drop": [
        "DoDragDrop(", "DragEnter(", "DragDrop(", "AllowDrop",
        "DataFormats", "e.Data.GetData("
    ],
    "serialization": [
        "Serialize(", "Deserialize(", "BinaryFormatter", "XmlSerializer",
        "JsonConvert", "JsonSerializer"
    ],
    "interop": [
        "[DllImport(", "Marshal.", "IntPtr", "extern ",
        "SendMessage(", "FindWindow("
    ],
}


def detect_patterns(handler_body: str) -> list:
    """Detect complex code patterns in an event handler body."""
    detected = []
    if not handler_body:
        return detected

    for pattern_name, keywords in COMPLEX_PATTERNS.items():
        for kw in keywords:
            if kw in handler_body:
                detected.append(pattern_name)
                break

    return detected


def analyze_control(ctrl: dict, rule_result: dict) -> AnalysisResult:
    """Analyze a single control and determine transformation strategy."""
    control_name = ctrl.get("name", "")
    original_type = ctrl.get("original_type", "")
    short_type = original_type.split('.')[-1]

    all_patterns = []
    for evt in ctrl.get("events", []):
        patterns = detect_patterns(evt.get("handler_body", ""))
        all_patterns.extend(patterns)

    # Determine strategy
    rule_status = rule_result.get("status", "unmapped") if rule_result else "unmapped"
    difficulty = ctrl.get("migration_difficulty", "simple")

    if rule_status == "unmapped":
        strategy = "llm"
        difficulty = "complex"
    elif rule_status == "agent_needed" or "dynamic_ui" in all_patterns or "custom_painting" in all_patterns:
        strategy = "llm"
        if difficulty == "simple":
            difficulty = "moderate"
    elif all_patterns:
        strategy = "template"
        if difficulty == "simple":
            difficulty = "moderate"
    else:
        strategy = "rule"

    return AnalysisResult(
        control_name=control_name,
        original_type=original_type,
        patterns_detected=list(set(all_patterns)),
        transformation_strategy=strategy,
        difficulty=difficulty,
        notes=f"Rule status: {rule_status}"
    )


def analyze_mvvm_candidates(ir_form: dict) -> list:
    """Identify event handlers that should be converted to MVVM commands."""
    candidates = []

    for ctrl in ir_form.get("controls", []):
        for evt in ctrl.get("events", []):
            event_type = evt.get("event_type", "")
            handler_name = evt.get("handler_name", "")
            handler_body = evt.get("handler_body", "")

            # Click events → RelayCommand
            if event_type in ("click", "double_click"):
                candidates.append({
                    "handler": handler_name,
                    "control": ctrl.get("name"),
                    "event": event_type,
                    "mvvm_type": "RelayCommand",
                    "body": handler_body,
                    "complexity": evt.get("complexity", "simple"),
                })
            # TextChanged → Observable property
            elif event_type in ("text_changed", "value_changed"):
                candidates.append({
                    "handler": handler_name,
                    "control": ctrl.get("name"),
                    "event": event_type,
                    "mvvm_type": "ObservableProperty",
                    "body": handler_body,
                    "complexity": evt.get("complexity", "simple"),
                })
            # SelectionChanged → Observable + Command
            elif event_type in ("selection_changed", "checked_changed"):
                candidates.append({
                    "handler": handler_name,
                    "control": ctrl.get("name"),
                    "event": event_type,
                    "mvvm_type": "ObservableProperty",
                    "body": handler_body,
                    "complexity": evt.get("complexity", "simple"),
                })

    return candidates


def create_transformation_plan(ir_form: dict, rule_results: dict) -> TransformationPlan:
    """Create a comprehensive transformation plan for a form."""
    analyses = []
    rule_count = 0
    template_count = 0
    llm_count = 0
    all_patterns = set()

    # Build lookup for rule results
    rule_lookup = {}
    for tr in rule_results.get("transformations", []):
        rule_lookup[tr.get("control_name", "")] = tr

    for ctrl in ir_form.get("controls", []):
        ctrl_name = ctrl.get("name", "")
        rule_result = rule_lookup.get(ctrl_name, {})
        analysis = analyze_control(ctrl, rule_result)
        analyses.append(analysis)

        if analysis.transformation_strategy == "rule":
            rule_count += 1
        elif analysis.transformation_strategy == "template":
            template_count += 1
        else:
            llm_count += 1

        all_patterns.update(analysis.patterns_detected)

    mvvm_candidates = analyze_mvvm_candidates(ir_form)

    return TransformationPlan(
        form_id=ir_form.get("id", ""),
        total_controls=len(analyses),
        rule_controls=rule_count,
        template_controls=template_count,
        llm_controls=llm_count,
        analyses=analyses,
        detected_patterns=list(all_patterns),
        mvvm_candidates=mvvm_candidates
    )
