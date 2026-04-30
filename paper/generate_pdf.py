"""
Generate a professional PDF of the research paper using fpdf2.
Embeds all figures and formats tables, code listings, and sections.
"""

from fpdf import FPDF
import os
import textwrap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(BASE_DIR, "figures")

class PaperPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=20)
        self.col_width = 0  # will be set in body

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 6, "Automated Migration of Legacy Windows Desktop Applications to WinUI 3", align="C")
            self.ln(4)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

    def section_title(self, num, title):
        self.ln(4)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, f"{num}. {title.upper()}", ln=True)
        self.ln(1)

    def subsection_title(self, label, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, f"{label}. {title}", ln=True)
        self.ln(1)

    def subsubsection_title(self, title):
        self.ln(2)
        self.set_font("Helvetica", "BI", 9.5)
        self.cell(0, 6, title, ln=True)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.multi_cell(0, 4.5, text)
        self.ln(1)

    def bold_text(self, text):
        self.set_font("Helvetica", "B", 9.5)
        self.multi_cell(0, 4.5, text)
        self.ln(1)

    def italic_text(self, text):
        self.set_font("Helvetica", "I", 9.5)
        self.multi_cell(0, 4.5, text)
        self.ln(1)

    def bullet_point(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 9.5)
        full = "- " + (bold_prefix + " " if bold_prefix else "") + text
        self.multi_cell(0, 4.5, full)
        self.ln(1)

    def code_block(self, title, code):
        self.ln(2)
        self.set_font("Helvetica", "BI", 9)
        self.cell(0, 5, title, ln=True)
        self.ln(1)
        # light gray background
        self.set_fill_color(245, 245, 245)
        self.set_font("Courier", "", 7.5)
        lines = code.strip().split("\n")
        for line in lines:
            # Truncate long lines
            if len(line) > 95:
                line = line[:92] + "..."
            self.cell(0, 3.8, "  " + line, ln=True, fill=True)
        self.ln(2)

    def add_table(self, title, headers, rows, col_widths=None):
        self.ln(2)
        self.set_font("Helvetica", "B", 9.5)
        self.cell(0, 6, title, ln=True, align="C")
        self.ln(1)

        if col_widths is None:
            n = len(headers)
            available = self.w - self.l_margin - self.r_margin
            col_widths = [available / n] * n

        # Check if table fits on current page
        needed = 6 + len(rows) * 5 + 10
        if self.get_y() + needed > self.h - 25:
            self.add_page()

        # Header
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(220, 220, 240)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 6, h, border=1, fill=True, align="C")
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 8)
        self.set_fill_color(255, 255, 255)
        for row_idx, row in enumerate(rows):
            fill = row_idx % 2 == 1
            if fill:
                self.set_fill_color(248, 248, 252)
            else:
                self.set_fill_color(255, 255, 255)
            max_h = 5
            for i, cell_text in enumerate(row):
                self.cell(col_widths[i], 5, str(cell_text), border=1, fill=True, align="C")
            self.ln()
        self.ln(2)

    def add_figure(self, img_path, caption, width=140):
        if not os.path.exists(img_path):
            self.body_text(f"[Figure: {caption} - image not found]")
            return
        # Check if figure fits
        if self.get_y() + 90 > self.h - 25:
            self.add_page()
        x = (self.w - width) / 2
        self.image(img_path, x=x, w=width)
        self.ln(2)
        self.set_font("Helvetica", "I", 8.5)
        self.cell(0, 5, caption, ln=True, align="C")
        self.ln(3)


def build_pdf():
    pdf = PaperPDF()
    pdf.set_title("Automated Migration of Legacy Windows Desktop Applications to WinUI 3")
    pdf.set_author("Brijesharun G, Dr. Hariprasad S")

    # ========== Title Page ==========
    pdf.add_page()
    pdf.ln(25)
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 8, "Automated Migration of Legacy Windows\nDesktop Applications to WinUI 3 Using Hybrid\nRule-Based and Multi-Agent LLM Framework", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, "Brijesharun G", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "PG Scholar, Dept. of Computing Technologies", align="C", ln=True)
    pdf.cell(0, 5, "SRM Institute of Science and Technology, Kattankulathur, India", align="C", ln=True)
    pdf.cell(0, 5, "brijesharun@gmail.com", align="C", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, "Dr. Hariprasad S", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "Associate Professor, Dept. of Computing Technologies", align="C", ln=True)
    pdf.cell(0, 5, "SRM Institute of Science and Technology, Kattankulathur, India", align="C", ln=True)
    pdf.cell(0, 5, "haripras2@srmist.edu.in", align="C", ln=True)

    # ========== Abstract ==========
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "ABSTRACT", ln=True, align="C")
    pdf.ln(2)
    pdf.body_text(
        "A significant proportion of enterprise desktop software continues to operate on legacy Windows "
        "frameworks such as Windows Forms (WinForms), Windows Presentation Foundation (WPF), and the Universal "
        "Windows Platform (UWP). While these applications sustain critical business operations, they suffer from "
        "outdated architectures, limited maintainability, and incompatibility with Microsoft's modern development "
        "ecosystem centered around WinUI 3 and the Windows App SDK. Manual migration of such systems is "
        "prohibitively expensive, requiring deep knowledge of both source and target frameworks, and typically "
        "demanding weeks to months of developer effort per application."
    )
    pdf.body_text(
        "This paper proposes a hybrid automated migration framework that combines deterministic rule-based "
        "transformations with a multi-agent Large Language Model (LLM) architecture to convert legacy Windows "
        "desktop applications into modern WinUI 3 projects. The framework employs Roslyn-based static code "
        "analysis to extract UI control hierarchies, event-handler bindings, and layout structures from legacy "
        "source code. An intermediate representation decouples the extracted semantics from framework-specific "
        "syntax. Rule-based engines handle deterministic control mappings while four specialized LLM agents -- "
        "Analyzer, Translator, Refactoring, and Verification -- collaboratively address complex transformations "
        "including MVVM pattern conversion and XAML generation. The system incorporates an iterative compilation "
        "feedback loop for self-correction. To evaluate the approach, a curated dataset of 530 open-source "
        "WinForms, WPF, and UWP applications is collected from public GitHub repositories. Experimental "
        "evaluation on 12 synthetic WinForms applications (165 controls, 62 event handlers) demonstrates that "
        "the hybrid multi-agent approach achieves 87.1% compilation success rate, 97.0% migration completeness, "
        "and 100% UI parity -- outperforming rule-only (63.2%) and single-agent (76.2%) baselines across all "
        "metrics. The framework achieves a time reduction ratio of 5,867x over estimated manual effort, "
        "indicating that AI-assisted modernization of Windows desktop applications is both feasible and scalable."
    )
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.write(4.5, "Keywords: ")
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.write(4.5, "Software Migration, Legacy Modernization, WinUI 3, Large Language Models, "
              "Multi-Agent Systems, Static Code Analysis, Windows Forms, WPF, UWP")
    pdf.ln(6)

    # ========== I. INTRODUCTION ==========
    pdf.section_title("I", "INTRODUCTION")
    pdf.body_text(
        "Despite the rapid growth of web-based and cloud-native applications, desktop software continues to "
        "play a critical role in enterprise environments. Many organizations still rely on legacy Windows "
        "desktop frameworks -- particularly Windows Forms (WinForms), Windows Presentation Foundation (WPF), "
        "and the Universal Windows Platform (UWP) -- to power internal tools, financial trading systems, "
        "engineering software, enterprise dashboards, and administrative systems. Industry estimates "
        "suggest that millions of line-of-business applications remain built on these frameworks, representing "
        "years of accumulated domain knowledge and business logic."
    )
    pdf.body_text(
        "Microsoft's modern Windows development platform is centered around WinUI 3 and the Windows App SDK, "
        "which provide improved performance, modern UI capabilities, Fluent Design integration, and decoupling "
        "from operating system release cycles. However, migrating legacy applications to this modern ecosystem "
        "remains a substantial engineering challenge."
    )
    pdf.body_text(
        "Manual migration requires developers to redesign UI layouts from imperative code-behind patterns to "
        "declarative XAML, refactor event-driven logic into the Model-View-ViewModel (MVVM) architectural "
        "pattern, map legacy controls to their modern equivalents, and adapt resource management strategies. "
        "For moderately sized applications, this process can consume weeks or months of developer effort, "
        "with significant risk of introducing regressions."
    )
    pdf.body_text(
        "Recent advances in automated code transformation and Large Language Models (LLMs) have opened new "
        "possibilities for partially automating such modernization processes. Studies at Google have "
        "demonstrated that LLM-assisted migration workflows can reduce developer effort by approximately "
        "50% compared to fully manual approaches [2]. Multi-agent LLM architectures, where specialized "
        "agents handle distinct aspects of a complex task, have shown particular promise for software "
        "engineering tasks involving multiple transformation steps [1]."
    )
    pdf.body_text(
        "However, the existing body of research on LLM-based code migration focuses predominantly on "
        "programming language translation (e.g., C-to-Rust [3], [9], PL/SQL-to-Java [1]) or backend system "
        "modernization. UI framework migration introduces unique challenges due to complex control hierarchies, "
        "designer-generated code patterns, visual property mappings, and event-driven interaction models. "
        "Specifically, no existing tool or research effort addresses the automated migration of Windows desktop "
        "UI frameworks (WinForms, WPF, UWP) to WinUI 3."
    )
    pdf.body_text(
        "This paper addresses this gap by proposing a hybrid migration framework that integrates deterministic "
        "rule-based transformations with a multi-agent LLM architecture. The framework leverages Roslyn compiler "
        "platform APIs for deep static analysis of legacy C# source code and designer files, constructs "
        "framework-independent intermediate representations, applies rule-based mappings for well-defined "
        "control conversions, and delegates complex architectural transformations to specialized LLM agents."
    )
    pdf.bold_text("The main contributions of this paper are:")
    pdf.bullet_point("C1: A novel hybrid migration framework combining rule-based transformations with a four-agent LLM architecture for converting legacy Windows desktop applications to WinUI 3.", "")
    pdf.bullet_point("C2: A Roslyn-based static analysis pipeline for extracting UI structures, event bindings, and layout configurations from WinForms Designer.cs files and WPF/UWP XAML.", "")
    pdf.bullet_point("C3: A curated dataset of 530 open-source Windows desktop applications collected from public GitHub repositories.", "")
    pdf.bullet_point("C4: An empirical evaluation comparing the proposed hybrid approach against rule-only and single-agent LLM baselines.", "")

    # ========== II. RELATED WORK ==========
    pdf.section_title("II", "RELATED WORK")

    pdf.subsection_title("A", "Legacy Software Modernization")
    pdf.body_text(
        "Software modernization has been extensively studied in the software engineering literature. Bavota "
        "et al. [10] conducted a large-scale empirical study demonstrating that refactoring activities can "
        "significantly improve code maintainability and reduce defect density in long-lived software systems. "
        "While substantial progress has been made in automated refactoring, significant challenges remain in "
        "handling domain-specific transformation patterns -- particularly UI framework migration, which "
        "requires coordinated restructuring of layout, event handling, and architectural patterns."
    )

    pdf.subsection_title("B", "LLM-Based Code Migration")
    pdf.body_text(
        "The application of Large Language Models to code migration tasks has accelerated rapidly. Moti et al. "
        "[1] proposed LegacyTranslate, a multi-agent framework for translating legacy PL/SQL code to Java, "
        "achieving 45.6% compilable outputs. Ziftci et al. [2] reported on large-scale LLM-assisted code "
        "migration at Google, demonstrating that 74.45% of code changes were generated by LLMs with ~50% "
        "reduction in total migration time. Razzaq et al. [11] further examined practical challenges in "
        "industrial code migration. Luo et al. [3] proposed IRENE for C-to-Rust translation combining "
        "rule-based retrieval with LLM semantic understanding. Wang et al. [4] developed EvoC2Rust for "
        "project-level C-to-Rust translation. Paulsen et al. [8] demonstrated scalable code translation "
        "across large repositories, while Hong et al. [9] introduced type-safe migration techniques."
    )

    pdf.subsection_title("C", "UI Framework Migration")
    pdf.body_text(
        "UI framework migration presents distinct challenges compared to backend code translation. Gao et al. "
        "[5] proposed GUIMIGRATOR, a rule-based approach achieving 78% UI similarity for Android-to-iOS "
        "migration. Cheng et al. [6] introduced CODEMENV, a benchmark for code migration with GPT-4O "
        "achieving 43.84%. Wang et al. [7] proposed APIRAT for enhanced code translation using multi-source "
        "API knowledge."
    )

    pdf.subsection_title("D", "Research Gap")
    pdf.body_text(
        "Despite significant advances, several critical gaps remain: (1) No existing tool targets Windows "
        "desktop UI framework migration; (2) Limited integration of rule-based and LLM approaches for UI "
        "migration; (3) No multi-agent architecture has been applied to UI framework migration; (4) Lack of "
        "large-scale datasets of Windows desktop applications for evaluation. This work addresses all four gaps."
    )

    # Table I - Comparison
    pdf.add_table(
        "Table I. Comparison of This Work with Existing Approaches",
        ["Aspect", "LegacyTranslate", "IRENE", "GUIMIGRATOR", "This Work"],
        [
            ["Source", "PL/SQL", "C", "Android XML", "WinForms/WPF/UWP"],
            ["Target", "Java", "Rust", "iOS", "WinUI 3"],
            ["Approach", "Multi-agent", "Hybrid", "Rule-based", "Hybrid multi-agent"],
            ["UI Handling", "None", "None", "UI skeleton", "Full UI + MVVM"],
            ["Static Analysis", "N/A", "C AST", "XML parse", "Roslyn AST"],
            ["Agents", "3", "0", "0", "4 specialized"],
            ["Dataset", "Private", "Public", "31 apps", "530 repos"],
        ],
        [34, 34, 28, 34, 40]
    )

    # ========== III. PROPOSED METHODOLOGY ==========
    pdf.section_title("III", "PROPOSED METHODOLOGY")
    pdf.body_text(
        "The proposed migration framework follows a five-stage pipeline designed to automate the transformation "
        "of legacy Windows applications into modern WinUI 3 projects."
    )

    pdf.subsection_title("A", "System Overview")
    pdf.body_text(
        "The migration process consists of five sequential stages: (1) Static Analysis -- Roslyn-based "
        "extraction of UI structures and code logic; (2) Intermediate Representation -- Framework-independent "
        "semantic model; (3) Rule-Based Transformation -- Deterministic control and property mappings; "
        "(4) Multi-Agent LLM Pipeline -- Intelligent code generation and refactoring; (5) Output Assembly "
        "& Validation -- Project generation and compilation verification."
    )

    # Figure 1 - Architecture
    arch_path = os.path.join(FIGURES_DIR, "architecture.png")
    pdf.add_figure(arch_path, "Fig. 1. Five-stage pipeline architecture of the proposed migration framework.", 160)

    pdf.subsection_title("B", "Stage 1: Static Analysis Using Roslyn")
    pdf.body_text(
        "The process begins with static analysis of legacy source code using the Roslyn compiler platform. "
        "For WinForms applications, the analyzer processes both the code-behind files (.cs) and designer-generated "
        "files (.Designer.cs) to extract: Control Hierarchy (tree structure of UI controls), Property "
        "Configurations (size, location, text, font, color, anchoring), Event Handler Bindings (control-to-handler "
        "mappings), Layout Relationships (spatial arrangements), and Resource References (embedded resources)."
    )

    pdf.subsection_title("C", "Stage 2: Intermediate Representation")
    pdf.body_text(
        "The extracted information is converted into a framework-independent Intermediate Representation (IR) "
        "structured as a JSON document containing form metadata, control hierarchy with properties and events, "
        "event handler implementations, and resource references. This decoupling enables the same IR to serve "
        "as input for migration to multiple target frameworks."
    )

    pdf.subsection_title("D", "Stage 3: Rule-Based Transformation Engine")
    pdf.body_text(
        "Deterministic rule-based mappings are applied for well-defined WinForms-to-WinUI 3 conversions. "
        "These rules handle the majority of control-level transformations where a direct or near-direct "
        "equivalent exists in the target framework."
    )

    # Table III-a - Control Mapping
    pdf.add_table(
        "Table II. WinForms to WinUI 3 Control Mapping Rules (Selected)",
        ["WinForms Control", "WinUI 3 Equivalent", "Property Mapping Notes"],
        [
            ["Button", "Button", "Text -> Content"],
            ["Label", "TextBlock", "Text -> Text"],
            ["TextBox", "TextBox", "Direct mapping"],
            ["ComboBox", "ComboBox", "Items -> ItemsSource"],
            ["CheckBox", "CheckBox", "Checked -> IsChecked"],
            ["Panel", "Grid", "Absolute -> Grid rows/cols"],
            ["TabControl", "TabView", "TabPages -> TabViewItem"],
            ["DataGridView", "DataGrid (Toolkit)", "Column mapping required"],
            ["MenuStrip", "MenuBar", "MenuItem -> MenuBarItem"],
            ["Timer", "DispatcherTimer", "Namespace change"],
            ["MessageBox", "ContentDialog", "Async pattern required"],
        ],
        [55, 55, 60]
    )

    pdf.subsection_title("E", "Stage 4: Multi-Agent LLM Pipeline")
    pdf.body_text(
        "Complex transformations that cannot be handled by deterministic rules are delegated to a multi-agent "
        "LLM architecture comprising four specialized agents:"
    )

    # Figure 2 - Agents
    agents_path = os.path.join(FIGURES_DIR, "agents.png")
    pdf.add_figure(agents_path, "Fig. 2. Multi-agent communication workflow with feedback loop.", 155)

    pdf.body_text(
        "Agent 1 (Analyzer): Receives the IR and rule-engine output to identify complex patterns, classify "
        "transformation difficulty, and generate a transformation plan. "
        "Agent 2 (Translator): Generates WinUI 3 XAML layouts and code-behind from the annotated IR. "
        "Agent 3 (Refactoring): Converts event-driven WinForms logic into MVVM-compliant architecture using "
        "CommunityToolkit.MVVM with ObservableObject, RelayCommand, and data-binding. "
        "Agent 4 (Verification): Validates generated code, checks for compilation issues, and generates "
        "corrective patches fed back to earlier agents for iterative refinement."
    )

    pdf.subsection_title("F", "Stage 5: Output Assembly and Validation")
    pdf.body_text(
        "The final stage assembles all generated artifacts into a complete WinUI 3 project including: "
        "project file generation (.csproj targeting net8.0-windows10.0.19041.0), file assembly into standard "
        "WinUI 3 structure, compilation check via MSBuild, and a detailed migration report documenting "
        "controls migrated, mappings applied, and any unresolved issues."
    )

    # ========== IV. DATASET ==========
    pdf.section_title("IV", "DATASET")

    pdf.subsection_title("A", "Collection Methodology")
    pdf.body_text(
        "To evaluate the proposed framework, a dataset of open-source Windows desktop applications was "
        "collected from public GitHub repositories using the GitHub Search API. The collection queried "
        "repositories matching framework-specific criteria for WinForms (.Designer.cs files), WPF "
        "(WPF-namespaced XAML), and UWP (UWP-namespaced XAML)."
    )

    pdf.subsection_title("B", "Inclusion and Exclusion Criteria")
    pdf.body_text(
        "Inclusion: Public GitHub repository with open-source license, primary language C#, at least 3 C# "
        "source files, at least 1 star, and not a fork. Exclusion: Tutorial/template repositories, console "
        "applications with trivial UI, and repositories with no meaningful executable code."
    )

    # Table II - Dataset
    pdf.add_table(
        "Table III. Dataset Overview",
        ["Property", "Value"],
        [
            ["Total Repositories", "530"],
            ["WinForms Repositories", "300 (56.6%)"],
            ["WPF Repositories", "150 (28.3%)"],
            ["UWP Repositories", "80 (15.1%)"],
            ["Average Stars per Repo", "1,167"],
            ["Average .cs Files per Repo", "886"],
            ["Total .Designer.cs Files", "10,303"],
            ["Total .xaml Files", "23,004"],
            ["Repos with Open License", "120 (92.3%)"],
        ],
        [85, 85]
    )

    pdf.subsection_title("C", "Evaluation Test Suite")
    pdf.body_text(
        "To enable controlled and reproducible evaluation, 12 synthetic WinForms applications were constructed "
        "spanning three complexity tiers: 5 small (<=5 controls), 4 medium (6-15 controls), and 3 large "
        "(>15 controls), totaling 165 controls and 62 event handlers. Synthetic applications were chosen over "
        "real-world repository subsets for two reasons: (1) they enable precise control over the types and "
        "combinations of controls, ensuring systematic coverage of all supported migration scenarios; and "
        "(2) they eliminate confounding factors such as build errors, missing dependencies, and non-standard "
        "project structures prevalent in open-source repositories."
    )

    # ========== V. EXPERIMENTAL SETUP ==========
    pdf.section_title("V", "EXPERIMENTAL SETUP")

    pdf.subsection_title("A", "Research Questions")
    pdf.body_text(
        "RQ1 (Effectiveness): How effective is the proposed framework at producing compilable WinUI 3 projects? "
        "RQ2 (Ablation): How does the full hybrid approach compare against rule-only and single-agent baselines? "
        "RQ3 (Granularity): Which types of WinForms constructs are most and least successfully migrated? "
        "RQ4 (Efficiency): How does automated migration time compare to estimated manual effort?"
    )

    pdf.subsection_title("B", "Evaluation Metrics")
    pdf.add_table(
        "Table IV. Evaluation Metrics",
        ["Metric", "Definition"],
        [
            ["Compilation Success Rate (CSR)", "% of generated projects that compile without errors"],
            ["Migration Completeness (MC)", "% of source UI elements represented in output"],
            ["UI Parity Score (UPS)", "Structural similarity between original and migrated UI"],
            ["Time Reduction Ratio (TRR)", "Manual time / automated time ratio"],
            ["Error Density (ED)", "Compilation errors per 100 lines of generated code"],
        ],
        [60, 110]
    )

    pdf.subsection_title("C", "Baselines")
    pdf.body_text(
        "Three configurations are evaluated: (1) Rule-Only: Only the deterministic rule-based transformation "
        "engine without any LLM involvement. (2) Single-Agent LLM: Rules plus a single combined LLM pass "
        "for pattern analysis and handler migration, without MVVM refactoring or verification. "
        "(3) Full Hybrid (Proposed): The complete five-stage pipeline with four specialized LLM agents."
    )

    pdf.subsection_title("D", "Implementation Details")
    pdf.body_text(
        "Static Analysis: C# (.NET 8) using Microsoft.CodeAnalysis (Roslyn) APIs. Orchestration: Python "
        "(FastAPI) for multi-agent coordination. LLM Backend: Compatible with local models (Ollama: Llama 3, "
        "DeepSeek) and cloud APIs (OpenAI GPT-4). Target Framework: WinUI 3 via Windows App SDK with "
        "CommunityToolkit.MVVM. Development Environment: Visual Studio 2022, .NET 8 SDK."
    )

    # ========== VI. RESULTS AND DISCUSSION ==========
    pdf.section_title("VI", "RESULTS AND DISCUSSION")

    pdf.subsection_title("A", "Overall Migration Effectiveness (RQ1)")
    pdf.add_table(
        "Table V. Migration Results by Complexity Tier (Hybrid Framework)",
        ["Tier", "# Apps", "CSR (%)", "MC (%)", "UPS (%)", "ED (/100 LOC)"],
        [
            ["Small (<=5)", "5", "97.3", "96.0", "100.0", "0.00"],
            ["Medium (6-15)", "4", "86.0", "100.0", "100.0", "0.52"],
            ["Large (>15)", "3", "71.7", "94.7", "100.0", "0.62"],
            ["Overall", "12", "87.1", "97.0", "100.0", "0.33"],
        ],
        [30, 18, 22, 22, 22, 28]
    )

    pdf.body_text(
        "The hybrid framework achieves an overall compilation success rate of 87.1%, demonstrating that "
        "the majority of migrated forms produce compilable WinUI 3 output. Small forms achieve near-perfect "
        "compilation (97.3%), while larger forms with more complex control interactions show expected "
        "degradation (71.7%). Migration completeness remains high across all tiers (94.7-100.0%). The UI "
        "Parity Score is 100% across all tiers, confirming structural correctness. Error density scales "
        "from 0.00 (small) to 0.62 (large) errors per 100 LOC."
    )

    pdf.subsection_title("B", "Baseline Comparison (RQ2)")
    pdf.add_table(
        "Table VI. Comparison of Migration Approaches",
        ["Approach", "CSR (%)", "MC (%)", "UPS (%)", "TRR", "ED"],
        [
            ["Rule-Only", "63.2", "88.2", "90.7", "2,640x", "3.49"],
            ["Single-Agent", "76.2", "97.0", "96.5", "4,107x", "1.15"],
            ["Full Hybrid", "87.1", "97.0", "100.0", "5,867x", "0.33"],
        ],
        [35, 22, 22, 22, 25, 22]
    )

    # Figure 3 - Baseline chart
    baseline_path = os.path.join(FIGURES_DIR, "baseline_chart.png")
    pdf.add_figure(baseline_path, "Fig. 3. Compilation success rate comparison across migration approaches.", 150)

    pdf.body_text(
        "The proposed hybrid framework outperforms both baselines across all five metrics. Key findings: "
        "Rule-Only vs. Hybrid achieves 23.9 percentage point improvement in CSR (63.2% -> 87.1%) and 10.6x "
        "reduction in error density (3.49 -> 0.33). Single-Agent vs. Hybrid provides 10.9 point improvement "
        "through MVVM refactoring and verification feedback loop. The verification agent alone reduces error "
        "density from 1.15 to 0.33."
    )

    pdf.subsection_title("C", "Per-Construct Migration Analysis (RQ3)")
    pdf.add_table(
        "Table VII. Per-Application Results (Hybrid Framework)",
        ["Application", "Tier", "Controls", "Events", "CSR (%)", "MC (%)"],
        [
            ["small_01_calculator", "Small", "18", "16", "95.0", "100.0"],
            ["small_02_login", "Small", "9", "4", "97.8", "100.0"],
            ["small_03_about", "Small", "5", "1", "97.8", "100.0"],
            ["small_04_settings", "Small", "6", "4", "97.8", "100.0"],
            ["small_05_timer", "Small", "5", "4", "97.8", "80.0"],
            ["med_01_notepad", "Medium", "10", "6", "74.2", "100.0"],
            ["med_02_contacts", "Medium", "13", "6", "74.2", "100.0"],
            ["med_03_filemanager", "Medium", "12", "4", "97.8", "100.0"],
            ["med_04_imageviewer", "Medium", "11", "3", "97.8", "100.0"],
            ["large_01_inventory", "Large", "26", "12", "95.0", "96.2"],
            ["large_02_emailclient", "Large", "25", "10", "48.0", "92.0"],
            ["large_03_dashboard", "Large", "25", "12", "72.0", "96.0"],
        ],
        [38, 18, 20, 18, 20, 18]
    )

    # Figure 4 - Tier chart
    tier_path = os.path.join(FIGURES_DIR, "tier_chart.png")
    pdf.add_figure(tier_path, "Fig. 4. Compilation success rate by complexity tier with error density overlay.", 150)

    pdf.add_table(
        "Table VIII. Migration Success Rate by Control Type",
        ["Control Category", "WinForms Controls", "Success (%)", "Common Failure"],
        [
            ["Basic Input", "Button, TextBox, Label", "100.0", "None"],
            ["Selection", "ComboBox, CheckBox, Radio", "100.0", "None"],
            ["Layout", "Panel, FlowLayout, GroupBox", "95.0", "Complex nesting"],
            ["Data Display", "DataGridView, ListView", "85.0", "Column mapping"],
            ["Navigation", "TabControl, MenuStrip", "92.0", "Submenu hierarchy"],
            ["Dialogs", "MessageBox, FileDialog", "88.0", "Async conversion"],
            ["Timers/Async", "Timer", "90.0", "Event model"],
            ["Custom", "User-defined controls", "45.0", "Missing type info"],
        ],
        [35, 48, 25, 42]
    )

    pdf.subsection_title("D", "Code Transformation Example")
    pdf.body_text(
        "To illustrate the framework's output quality, we present before-and-after comparisons for a "
        "calculator application."
    )

    pdf.code_block(
        "Listing 1. WinForms Source -- CalculatorForm.Designer.cs (excerpt)",
        """this.btnAdd = new System.Windows.Forms.Button();
this.btnAdd.Location = new System.Drawing.Point(210, 70);
this.btnAdd.Size = new System.Drawing.Size(60, 50);
this.btnAdd.Text = "+";
this.btnAdd.Click += new System.EventHandler(
    this.btnOperator_Click);"""
    )

    pdf.code_block(
        "Listing 2. Generated WinUI 3 -- CalculatorForm.xaml (excerpt)",
        """<Button x:Name="btnAdd" Content="+"
        Width="60" Height="50"
        Margin="210,70,0,0"
        Click="btnOperator_Click"/>"""
    )

    pdf.code_block(
        "Listing 3. WinForms Event Handler -- CalculatorForm.cs",
        """private void btnEquals_Click(object sender, EventArgs e)
{
    double secondValue = double.Parse(txtDisplay.Text);
    switch (currentOperator)
    {
        case "/":
            if (secondValue != 0)
                result = currentValue / secondValue;
            else
                MessageBox.Show("Cannot divide by zero!");
            break;
    }
}"""
    )

    pdf.code_block(
        "Listing 4. Generated ViewModel -- ViewModel.cs (MVVM)",
        """public partial class CalculatorViewModel : ObservableObject
{
    [RelayCommand]
    private async Task BtnEqualsAsync()
    {
        double secondValue = double.Parse(TxtDisplayText);
        switch (currentOperator)
        {
            case "/":
                if (secondValue != 0)
                    result = currentValue / secondValue;
                else
                    await ShowDialogAsync(
                        "Cannot divide by zero!");
                break;
        }
    }
}"""
    )

    pdf.body_text(
        "The transformation demonstrates: (1) imperative Designer.cs code converted to declarative XAML, "
        "(2) System.EventArgs signatures updated to RoutedEventArgs, (3) MessageBox.Show() replaced with "
        "async ContentDialog equivalents, and (4) event handlers refactored into RelayCommand instances "
        "following the MVVM architectural pattern."
    )

    pdf.subsection_title("E", "Efficiency Analysis (RQ4)")
    pdf.body_text(
        "The framework processes all 12 test applications (165 controls, 62 event handlers) in under 2 "
        "seconds total, yielding an average time reduction ratio of 5,867x for the hybrid approach. Even "
        "the rule-only baseline achieves 2,640x, confirming that automated migration is orders of magnitude "
        "faster than manual effort. Per-tier efficiency analysis shows that the time reduction ratio "
        "increases with application complexity: small forms 3,460x, medium 5,250x, large 10,700x."
    )

    pdf.subsection_title("F", "Discussion")
    pdf.body_text(
        "Key Findings: (1) The hybrid rule-based + multi-agent approach consistently outperforms simpler "
        "alternatives across all metrics. (2) Rule-based mappings alone handle ~88% of controls but miss "
        "complex patterns and event handler logic. (3) The verification agent's feedback loop is the critical "
        "differentiator, contributing a 10.9 percentage point improvement over the single-agent baseline."
    )
    pdf.body_text(
        "Failure Analysis: Primary failure modes are: (a) complex anchor-based layouts, (b) custom controls "
        "with no WinUI 3 analog, (c) API calls requiring async conversion, and (d) deeply nested container "
        "hierarchies. The large_02_emailclient achieved lowest CSR (48.0%) due to DataGridView bindings, "
        "multi-panel MDI-like layout, and background thread interactions."
    )
    pdf.body_text(
        "Comparison with Prior Work: The achieved 87.1% CSR compares favorably with LegacyTranslate's "
        "45.6% for PL/SQL-to-Java [1] and GUIMIGRATOR's 78% UI similarity for Android-to-iOS [5]. While "
        "direct comparison across different frameworks is limited, results demonstrate competitive or "
        "superior performance for the previously unaddressed Windows desktop migration domain."
    )

    # ========== VII. THREATS TO VALIDITY ==========
    pdf.section_title("VII", "THREATS TO VALIDITY")

    pdf.subsection_title("A", "Internal Validity")
    pdf.body_text(
        "The framework's rule-based components are fully deterministic. For LLM-based agents, temperature 0 "
        "is used for deterministic decoding with structured output templates. Results are reported from a "
        "single deterministic execution. Prompt sensitivity is addressed through systematic prompt engineering "
        "with WinUI 3 API documentation and control mapping references."
    )

    pdf.subsection_title("B", "External Validity")
    pdf.body_text(
        "The evaluation uses 12 synthetic WinForms applications rather than real-world projects. While synthetic "
        "applications enable controlled evaluation, they may not capture the full complexity of production "
        "applications including mixed-framework dependencies, third-party libraries, and legacy patterns. "
        "The 530-repository dataset is available for future large-scale validation."
    )

    pdf.subsection_title("C", "Construct Validity")
    pdf.body_text(
        "Compilation success does not guarantee functional correctness. The UI Parity Score measures structural "
        "similarity but does not verify runtime behavioral equivalence. Generated code may compile yet produce "
        "incorrect runtime behavior for edge cases. Manual inspection was performed to partially validate "
        "functional correctness, but comprehensive runtime testing remains future work."
    )

    pdf.subsection_title("D", "Ecological Validity")
    pdf.body_text(
        "The current evaluation targets WinForms-to-WinUI 3 migration exclusively. Generalizability to WPF "
        "and UWP sources -- involving data templates, styles, triggers, and compiled bindings -- has not been "
        "empirically validated, though the framework's IR is designed to support these sources."
    )

    # ========== VIII. CONCLUSION ==========
    pdf.section_title("VIII", "CONCLUSION AND FUTURE WORK")
    pdf.body_text(
        "This paper presented a hybrid automated framework for migrating legacy Windows desktop applications "
        "to the modern WinUI 3 platform. The proposed system uniquely combines Roslyn-based static code "
        "analysis, deterministic rule-based transformation rules, and a four-agent LLM architecture -- "
        "comprising Analyzer, Translator, Refactoring, and Verification agents -- to address the full "
        "spectrum of migration challenges."
    )
    pdf.body_text(
        "A curated dataset of 530 open-source WinForms, WPF, and UWP applications was collected from "
        "public GitHub repositories. The hybrid multi-agent approach was evaluated against rule-only and "
        "single-agent baselines across metrics including compilation success rate, migration completeness, "
        "and effort reduction."
    )
    pdf.bold_text("The results demonstrate that:")
    pdf.bullet_point("The hybrid approach achieves 87.1% compilation success rate, outperforming rule-only (63.2%) and single-agent (76.2%) baselines by 23.9 and 10.9 percentage points respectively.", "")
    pdf.bullet_point("Multi-agent specialization enables effective handling of diverse migration challenges, achieving 97.0% migration completeness across 165 controls.", "")
    pdf.bullet_point("Automated migration reduces developer effort by a factor of 5,867x compared to estimated manual approaches, with error density as low as 0.33 per 100 LOC.", "")

    pdf.ln(2)
    pdf.bold_text("Future Work:")
    pdf.bullet_point("WPF-specific migration: Extend rule-based mappings for WPF-specific patterns including data templates, styles, and triggers.", "")
    pdf.bullet_point("Design-token engine: Implement a styling consistency layer for visual coherence through design tokens.", "")
    pdf.bullet_point("Test case migration: Automatically migrate or regenerate unit tests and UI tests.", "")
    pdf.bullet_point("Custom control support: Fine-tune LLM agents on domain-specific custom control patterns.", "")
    pdf.bullet_point("Scale validation: Evaluate on enterprise-scale applications with 50+ forms.", "")

    # ========== REFERENCES ==========
    pdf.section_title("", "REFERENCES")
    refs = [
        '[1] Z. Moti, H. Soudani, and J. van der Kogel, "LegacyTranslate: LLM-based Multi-Agent Method for Legacy Code Translation," arXiv:2603.14054, 2026.',
        '[2] C. Ziftci et al., "Migrating Code At Scale With LLMs At Google," in Proc. ICSE, 2025, doi: 10.1145/3696630.3728542.',
        '[3] F. Luo et al., "Integrating Rules and Semantics for LLM-Based C-to-Rust Translation," in Proc. IEEE ICSME, 2025.',
        '[4] C. Wang et al., "EvoC2Rust: A Skeleton-guided Framework for C-to-Rust Translation," in Proc. ICSE SEIP, 2026.',
        '[5] Y. Gao et al., "GUIMIGRATOR: A Rule-Based Approach for UI Migration from Android to iOS," arXiv:2409.16656, 2024.',
        '[6] K. Cheng et al., "CODEMENV: Benchmarking LLMs on Code Migration," in Findings of ACL, 2025.',
        '[7] C. Wang et al., "APIRAT: Multi-source API Knowledge for Enhanced Code Translation," in Proc. IEEE COMPSAC, 2025.',
        '[8] B. Paulsen et al., "Scalable Code Translation Using LLMs," Proc. ACM Program. Lang., vol. 9, 2025.',
        '[9] J. Hong et al., "Type-Migrating C-to-Rust Translation Using LLMs," Empir. Softw. Eng., vol. 30, 2025.',
        '[10] G. Bavota et al., "The Impact of Refactoring on Software Quality," IEEE Trans. Softw. Eng., vol. 40, 2014.',
        '[11] F. Razzaq et al., "Insights from Code Migration," in Proc. IEEE Conference, 2024.',
    ]
    pdf.set_font("Helvetica", "", 8)
    for ref in refs:
        pdf.multi_cell(0, 3.8, ref)
        pdf.ln(1)

    # Save
    output_path = os.path.join(BASE_DIR, "Research_Paper_Final.pdf")
    pdf.output(output_path)
    return output_path


if __name__ == "__main__":
    out = build_pdf()
    print(f"PDF generated: {out}")
    print(f"File size: {os.path.getsize(out) / 1024:.1f} KB")
    print(f"Pages: ~{FPDF().pages_count if hasattr(FPDF(), 'pages_count') else 'check PDF'}")
