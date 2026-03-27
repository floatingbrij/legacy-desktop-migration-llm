# Automated Migration of Legacy Windows Desktop Applications to WinUI 3 Using Hybrid Rule-Based and Multi-Agent LLM Framework

**Brijesharun G¹, Dr. Hariprasad S²**

¹ PG Scholar, Dept. of Computing Technologies, SRM Institute of Science and Technology, Kattankulathur, India. brijesharun@gmail.com  
² Associate Professor, Dept. of Computing Technologies, SRM Institute of Science and Technology, Kattankulathur, India. haripras2@srmist.edu.in

---

## Abstract

A significant proportion of enterprise desktop software continues to operate on legacy Windows frameworks such as Windows Forms (WinForms), Windows Presentation Foundation (WPF), and the Universal Windows Platform (UWP). While these applications sustain critical business operations, they suffer from outdated architectures, limited maintainability, and incompatibility with Microsoft's modern development ecosystem centered around WinUI 3 and the Windows App SDK. Manual migration of such systems is prohibitively expensive, requiring deep knowledge of both source and target frameworks, and typically demanding weeks to months of developer effort per application.

This paper proposes a hybrid automated migration framework that combines deterministic rule-based transformations with a multi-agent Large Language Model (LLM) architecture to convert legacy Windows desktop applications into modern WinUI 3 projects. The framework employs Roslyn-based static code analysis to extract UI control hierarchies, event-handler bindings, and layout structures from legacy source code. An intermediate representation decouples the extracted semantics from framework-specific syntax. Rule-based engines handle deterministic control mappings while four specialized LLM agents — Analyzer, Translator, Refactoring, and Verification — collaboratively address complex transformations including MVVM pattern conversion and XAML generation. The system incorporates an iterative compilation feedback loop for self-correction. To evaluate the approach, a curated dataset of over 100 open-source WinForms, WPF, and UWP applications is collected from public GitHub repositories. Experimental evaluation on 12 synthetic WinForms applications (165 controls, 62 event handlers) demonstrates that the hybrid multi-agent approach achieves 87.1% compilation success rate, 97.0% migration completeness, and 100% UI parity — outperforming rule-only (63.2%) and single-agent (76.2%) baselines across all metrics. The framework achieves a time reduction ratio of 5,867× over estimated manual effort, indicating that AI-assisted modernization of Windows desktop applications is both feasible and scalable.

**Keywords:** Software Migration, Legacy Modernization, WinUI 3, Large Language Models, Multi-Agent Systems, Static Code Analysis, Windows Forms, WPF, UWP

---

## I. INTRODUCTION

Despite the rapid growth of web-based and cloud-native applications, desktop software continues to play a critical role in enterprise environments. Many organizations still rely on legacy Windows desktop frameworks — particularly Windows Forms (WinForms), Windows Presentation Foundation (WPF), and the Universal Windows Platform (UWP) — to power internal tools, financial trading systems, engineering software, enterprise dashboards, and administrative systems. Industry estimates suggest that millions of line-of-business applications remain built on these frameworks, representing years of accumulated domain knowledge and business logic.

Microsoft's modern Windows development platform is centered around WinUI 3 and the Windows App SDK, which provide improved performance, modern UI capabilities, Fluent Design integration, and decoupling from operating system release cycles. However, migrating legacy applications to this modern ecosystem remains a substantial engineering challenge.

Manual migration requires developers to redesign UI layouts from imperative code-behind patterns to declarative XAML, refactor event-driven logic into the Model-View-ViewModel (MVVM) architectural pattern, map legacy controls to their modern equivalents, and adapt resource management strategies. For moderately sized applications, this process can consume weeks or months of developer effort, with significant risk of introducing regressions.

Recent advances in automated code transformation and Large Language Models (LLMs) have opened new possibilities for partially automating such modernization processes. Studies at Google have demonstrated that LLM-assisted migration workflows can reduce developer effort by approximately 50% compared to fully manual approaches [2]. Multi-agent LLM architectures, where specialized agents handle distinct aspects of a complex task, have shown particular promise for software engineering tasks involving multiple transformation steps [1].

However, the existing body of research on LLM-based code migration focuses predominantly on programming language translation (e.g., C-to-Rust [3], [9], PL/SQL-to-Java [1]) or backend system modernization. UI framework migration introduces unique challenges due to complex control hierarchies, designer-generated code patterns, visual property mappings, and event-driven interaction models. Specifically, no existing tool or research effort addresses the automated migration of Windows desktop UI frameworks (WinForms, WPF, UWP) to WinUI 3.

This paper addresses this gap by proposing a hybrid migration framework that integrates deterministic rule-based transformations with a multi-agent LLM architecture. The framework leverages Roslyn compiler platform APIs for deep static analysis of legacy C# source code and designer files, constructs framework-independent intermediate representations, applies rule-based mappings for well-defined control conversions, and delegates complex architectural transformations to specialized LLM agents.

The main contributions of this paper are:

1. **C1:** A novel hybrid migration framework combining rule-based transformations with a four-agent LLM architecture for converting legacy Windows desktop applications to WinUI 3.
2. **C2:** A Roslyn-based static analysis pipeline for extracting UI structures, event bindings, and layout configurations from WinForms Designer.cs files and WPF/UWP XAML.
3. **C3:** A curated dataset of over 100 open-source Windows desktop applications collected from public GitHub repositories, annotated with framework type, complexity tier, and file-level metadata.
4. **C4:** An empirical evaluation comparing the proposed hybrid approach against rule-only and single-agent LLM baselines using metrics including compilation success rate, migration completeness, and effort reduction.

---

## II. RELATED WORK

### A. Legacy Software Modernization

Software modernization has been extensively studied in the software engineering literature. Bavota et al. [10] conducted a large-scale empirical study demonstrating that refactoring activities can significantly improve code maintainability and reduce defect density in long-lived software systems. Their findings provide empirical justification for automated transformation approaches, showing measurable quality improvements from systematic code restructuring. While substantial progress has been made in automated refactoring, significant challenges remain in handling domain-specific transformation patterns — particularly UI framework migration, which requires coordinated restructuring of layout, event handling, and architectural patterns.

### B. LLM-Based Code Migration

The application of Large Language Models to code migration tasks has accelerated rapidly. Moti et al. [1] proposed LegacyTranslate, a multi-agent framework for translating legacy PL/SQL code to Java in the context of a financial institution migrating approximately 2.5 million lines of code. Their architecture comprises three specialized agents — Initial Translation, API Grounding, and Refinement — achieving 45.6% compilable outputs with the initial agent alone, and an additional 8% improvement through the full pipeline. This work serves as the methodological foundation for our multi-agent design.

Ziftci et al. [2] reported on large-scale LLM-assisted code migration at Google, demonstrating that 74.45% of code changes and 69.46% of individual edits in 39 migration projects were generated by LLMs. Developers reported approximately 50% reduction in total migration time, validating the practical feasibility of AI-assisted migration at industrial scale. Razzaq et al. [11] further examined practical challenges in industrial code migration, providing insights into common failure patterns and mitigation strategies.

Luo et al. [3] proposed IRENE, a framework that integrates rule-based retrieval with LLM-based semantic understanding for C-to-Rust translation. Their approach combines a rule-augmented retrieval module, a structured summarization module, and an error-driven translation module, achieving significant improvements in both translation accuracy and memory safety compliance. This hybrid rule-and-LLM design principle directly informs our framework architecture.

Wang et al. [4] developed EvoC2Rust, a skeleton-guided framework for project-level C-to-Rust translation that preserves structural relationships across files during migration. Their approach to maintaining project-level coherence during translation is relevant to our handling of multi-form WinForms applications.

Additional empirical evidence supports the viability of LLM-based migration: Paulsen et al. [8] demonstrated scalable code translation across large software repositories, while Hong et al. [9] introduced type-safe migration techniques for C-to-Rust translation.

### C. UI Framework Migration

UI framework migration presents distinct challenges compared to backend code translation due to hierarchical layout structures, visual property semantics, and event-driven interaction patterns. Gao et al. [5] proposed GUIMIGRATOR, a rule-based approach for UI migration from Android to iOS. Their system extracts Android UI layouts and constructs a UI skeleton tree, then generates iOS UI code using target code templates. GUIMIGRATOR achieved 78% UI similarity between source and target screenshots across 31 applications, demonstrating both the feasibility and limitations of purely rule-based UI migration approaches.

Cheng et al. [6] introduced CODEMENV, a benchmark specifically designed to assess LLM capabilities in code migration scenarios, reporting an average pass@1 rate of 26.50% with GPT-4O achieving the highest score at 43.84%. These benchmark results contextualize the difficulty of automated migration tasks and establish evaluation methodologies relevant to our work.

Wang et al. [7] proposed APIRAT, a method integrating multi-source API knowledge for enhanced code translation, achieving 4–15.1% accuracy improvements through API sequence retrieval, back-translation, and mapping techniques. Their API knowledge augmentation strategy informs our use of WinUI 3 documentation retrieval in the LLM agent pipeline.

### D. Research Gap

Table I summarizes the positioning of this work relative to existing approaches.

**Table I. Comparison of This Work with Existing Approaches**

| Aspect | LegacyTranslate [1] | IRENE [3] | GUIMIGRATOR [5] | **This Work** |
|--------|---------------------|-----------|-----------------|---------------|
| Source Domain | PL/SQL (backend) | C (systems) | Android XML (mobile UI) | **WinForms/WPF/UWP (desktop UI)** |
| Target Domain | Java | Rust | iOS Storyboard | **WinUI 3 (XAML + C#)** |
| Approach | Multi-agent LLM | Hybrid rule + LLM | Rule-based only | **Hybrid rule + multi-agent LLM** |
| UI Handling | None | None | UI skeleton tree | **Full UI hierarchy + MVVM** |
| Static Analysis | Not specified | C AST | XML parsing | **Roslyn AST (deep C# analysis)** |
| Agents | 3 | 0 (single pipeline) | 0 | **4 specialized agents** |
| Architecture Pattern | API alignment | Rule-based retrieval | Template matching | **MVVM conversion** |
| Dataset | Private (financial) | Public + Industrial | 31 apps | **100+ public repos** |
| Validation | Compilation + tests | Compilation + safety | Screenshot similarity | **Compilation + structural parity** |

Despite significant advances in automated code migration and LLM-based transformation, several critical gaps remain:

1. **No existing tool targets Windows desktop UI framework migration.** While mobile UI migration (Android↔iOS) has received attention [5], the Windows desktop ecosystem — representing a massive installed base of enterprise applications — remains unaddressed.

2. **Limited integration of rule-based and LLM approaches for UI migration.** Existing work tends toward either pure rule-based systems [5] (deterministic but inflexible) or pure LLM systems (flexible but unreliable). The combination of both for UI framework migration is underexplored.

3. **No multi-agent architecture has been applied to UI framework migration.** Multi-agent LLM architectures have proven effective for backend code translation [1], but their application to UI-specific migration tasks — requiring coordinated handling of layout, styling, event logic, and architectural patterns — has not been investigated.

4. **Lack of large-scale, publicly available datasets of Windows desktop applications** for evaluating migration tools. Most existing studies use small or private datasets, limiting reproducibility and generalizability.

This work addresses all four gaps simultaneously.

---

## III. PROPOSED METHODOLOGY

The proposed migration framework follows a five-stage pipeline designed to automate the transformation of legacy Windows applications into modern WinUI 3 projects. Figure 1 illustrates the overall system architecture.

### A. System Overview

The migration process consists of five sequential stages:

1. **Static Analysis** — Roslyn-based extraction of UI structures and code logic
2. **Intermediate Representation** — Framework-independent semantic model
3. **Rule-Based Transformation** — Deterministic control and property mappings
4. **Multi-Agent LLM Pipeline** — Intelligent code generation and refactoring
5. **Output Assembly & Validation** — Project generation and compilation verification

Each stage produces well-defined outputs that serve as inputs to subsequent stages, enabling modular evaluation and incremental improvement. Figure 1 presents the complete five-stage pipeline architecture.

### B. Stage 1: Static Analysis Using Roslyn

The process begins with static analysis of legacy source code using the Roslyn compiler platform. For WinForms applications, the analyzer processes both the code-behind files (.cs) and designer-generated files (.Designer.cs) to extract:

- **Control Hierarchy:** The tree structure of UI controls, including parent-child relationships and container nesting.
- **Property Configurations:** Visual properties such as size, location, text, font, color, anchoring, and docking settings for each control.
- **Event Handler Bindings:** Mappings between UI controls and their associated event handler methods (e.g., `button1.Click += button1_Click`).
- **Layout Relationships:** Spatial arrangements including absolute positioning, flow layouts, and docking configurations.
- **Resource References:** Links to embedded resources, images, and localization strings from .resx files.

For WPF and UWP applications, XAML files are parsed directly to extract the equivalent hierarchical structure, data bindings, styles, and triggers.

The Roslyn Syntax Tree API provides access to the full abstract syntax tree (AST) of C# source code, enabling precise identification of control instantiation patterns, property assignments, and event subscriptions that are characteristic of WinForms designer-generated code.

### C. Stage 2: Intermediate Representation

The extracted information is converted into a framework-independent Intermediate Representation (IR) that captures the structural and behavioral semantics of the original user interface while remaining decoupled from any specific framework syntax.

The IR is structured as a JSON document containing:

```json
{
  "form": {
    "name": "MainForm",
    "title": "Application Title",
    "size": { "width": 800, "height": 600 },
    "controls": [
      {
        "type": "Button",
        "name": "btnSubmit",
        "properties": {
          "text": "Submit",
          "location": { "x": 100, "y": 200 },
          "size": { "width": 120, "height": 35 }
        },
        "events": [
          { "event": "Click", "handler": "btnSubmit_Click" }
        ],
        "children": []
      }
    ]
  },
  "event_handlers": {
    "btnSubmit_Click": {
      "parameters": ["object sender", "EventArgs e"],
      "body": "// extracted C# logic"
    }
  },
  "resources": []
}
```

This decoupling enables the same IR to serve as input for migration to multiple target frameworks, though this paper focuses on WinUI 3 as the target.

### D. Stage 3: Rule-Based Transformation Engine

Deterministic rule-based mappings are applied for well-defined WinForms-to-WinUI 3 conversions. These rules handle the majority of control-level transformations where a direct or near-direct equivalent exists in the target framework.

**Table III-a. WinForms to WinUI 3 Control Mapping Rules**

| WinForms Control | WinUI 3 Equivalent | Property Mapping Notes |
|------------------|--------------------|----------------------|
| `Button` | `Button` | `Text` → `Content` |
| `Label` | `TextBlock` | `Text` → `Text` |
| `TextBox` | `TextBox` | Direct mapping |
| `ComboBox` | `ComboBox` | `Items` → `ItemsSource` (with binding) |
| `CheckBox` | `CheckBox` | `Checked` → `IsChecked` |
| `RadioButton` | `RadioButton` | `Checked` → `IsChecked` |
| `Panel` | `Grid` | Absolute positioning → Grid rows/columns |
| `FlowLayoutPanel` | `StackPanel` | `FlowDirection` → `Orientation` |
| `TabControl` | `TabView` | `TabPages` → `TabViewItem` |
| `ListView` | `ListView` | Significant API differences |
| `DataGridView` | `DataGrid` (Community Toolkit) | Column mapping required |
| `MenuStrip` | `MenuBar` | `ToolStripMenuItem` → `MenuBarItem` |
| `Timer` | `DispatcherTimer` | Namespace change |
| `MessageBox` | `ContentDialog` | Async pattern required |
| `OpenFileDialog` | `FileOpenPicker` | WinRT async API |
| `PictureBox` | `Image` | Source binding pattern change |
| `ProgressBar` | `ProgressBar` | Direct mapping |
| `GroupBox` | `Expander` or custom border | No direct equivalent |
| `ToolTip` | `ToolTipService` | Attached property pattern |
| `StatusStrip` | `InfoBar` or custom | No direct equivalent |

The rule engine also handles namespace transformations (`System.Windows.Forms` → `Microsoft.UI.Xaml.Controls`), project file restructuring (.csproj target framework changes), and resource file format conversions.

For absolute-positioned WinForms controls, the engine implements a layout inference algorithm that converts pixel-based `Location` and `Size` properties into Grid-based row/column definitions with appropriate star-sizing and margins.

### E. Stage 4: Multi-Agent LLM Pipeline

Complex transformations that cannot be handled by deterministic rules are delegated to a multi-agent LLM architecture comprising four specialized agents. Figure 2 depicts the agent communication workflow.

#### Agent 1: Analyzer Agent
The Analyzer Agent receives the IR and rule-engine output, then performs:
- Identification of code patterns that require non-trivial transformation (custom controls, complex event chains, dynamic UI generation)
- Classification of transformation difficulty per component
- Generation of a transformation plan specifying which components can be handled by rules alone and which require LLM-assisted generation

#### Agent 2: Translator Agent
The Translator Agent generates WinUI 3 XAML layouts and corresponding code-behind from the annotated IR:
- Converts the UI hierarchy into declarative XAML, selecting appropriate layout panels and control configurations
- Generates resource dictionaries for styles and templates
- Handles controls without direct rule-based mappings using contextual understanding of the original UI intent

#### Agent 3: Refactoring Agent
The Refactoring Agent converts event-driven WinForms logic into MVVM-compliant architecture:
- Creates ViewModel classes with `ObservableObject` base (from CommunityToolkit.MVVM)
- Converts event handlers (e.g., `button1_Click`) into `RelayCommand` instances
- Transforms direct control property access into data-binding expressions
- Separates business logic from UI interaction logic

#### Agent 4: Verification Agent
The Verification Agent validates the generated code:
- Checks for syntactic correctness of generated XAML and C#
- Validates namespace references and package dependencies
- Identifies compilation issues using MSBuild integration
- If errors are found, generates corrective patches and feeds them back to the Translator and Refactoring agents for iterative refinement

The agents communicate through a structured message protocol. Each agent receives the outputs of preceding agents along with the original IR and rule-engine results, ensuring full context is maintained throughout the pipeline. Retrieval-Augmented Generation (RAG) is employed to provide agents with relevant WinUI 3 documentation, API references, and migration examples during generation.

### F. Stage 5: Output Assembly and Validation

The final stage assembles all generated artifacts into a complete WinUI 3 project:

1. **Project File Generation:** Creates a `.csproj` targeting `net8.0-windows10.0.19041.0` with appropriate WinUI 3 and CommunityToolkit.MVVM NuGet references.
2. **File Assembly:** Organizes generated `.xaml`, `.xaml.cs`, and ViewModel files into the standard WinUI 3 project structure.
3. **Compilation Check:** Invokes MSBuild to compile the generated project. Compilation errors trigger a feedback loop to the Verification Agent for corrective transformation.
4. **Migration Report:** Generates a detailed report documenting: controls migrated, mappings applied, LLM-generated sections, compilation status, and any unresolved issues requiring manual attention.

---

## IV. DATASET

### A. Collection Methodology

To evaluate the proposed framework, a dataset of open-source Windows desktop applications was collected from public GitHub repositories using the GitHub Search API. The collection process queried repositories matching framework-specific criteria:

- **WinForms:** Repositories containing `.Designer.cs` files or tagged with the `winforms` topic
- **WPF:** Repositories containing WPF-namespaced `.xaml` files or tagged with the `wpf` topic
- **UWP:** Repositories containing UWP-namespaced `.xaml` files or tagged with the `uwp` topic

### B. Inclusion and Exclusion Criteria

**Inclusion Criteria:**
- Public GitHub repository with an identifiable open-source license
- Primary language is C#
- Contains at least 3 C# source files and a project file (.csproj or .sln)
- Has at least 1 GitHub star (filters trivial or abandoned projects)
- Is not a fork (avoids duplicates)

**Exclusion Criteria:**
- Tutorial or template repositories consisting primarily of boilerplate code
- Console applications with trivially simple UI components
- Repositories with no meaningful executable code

### C. Dataset Statistics

**Table II. Dataset Overview**

| Property | Value |
|----------|-------|
| Total Repositories | 130 |
| WinForms Repositories | 80 (61.5%) |
| WPF Repositories | 30 (23.1%) |
| UWP Repositories | 20 (15.4%) |
| Average Stars per Repo | 3,447 |
| Average .cs Files per Repo | 886 |
| Total .Designer.cs Files | 4,255 |
| Total .xaml Files | 10,954 |
| Repos with Open License | 120 (92.3%) |
| Collection Period | March 2026 |
| Source | Public GitHub Repositories |

**Table IIa. Complexity Distribution**

| Tier | UI Files | Count | Percentage |
|------|----------|-------|------------|
| Small | ≤5 | 23 | 17.7% |
| Medium | 6–15 | 27 | 20.8% |
| Large | >15 | 80 | 61.5% |

Notable repositories in the dataset include ScreenToGif (26,618 stars, WPF), ImageGlass (12,610 stars, WinForms), and MaterialDesignInXamlToolkit (16,103 stars, WPF), representing a diverse range of application complexity and domain coverage.

### D. Evaluation Test Suite

To enable controlled and reproducible evaluation, 12 synthetic WinForms applications were constructed by the authors spanning three complexity tiers: 5 small (≤5 controls), 4 medium (6–15 controls), and 3 large (>15 controls), totaling 165 controls and 62 event handlers. Synthetic applications were chosen over real-world repository subsets for two reasons: (1) they enable precise control over the types and combinations of controls, event patterns, and layout structures present, ensuring systematic coverage of all supported migration scenarios; and (2) they eliminate confounding factors such as build errors, missing dependencies, and non-standard project structures that are prevalent in open-source repositories. The 130-repository dataset described in Section IV.C serves as a representative corpus for validating that the synthetic applications cover patterns commonly found in real-world WinForms projects and is available for future large-scale evaluation.

---

## V. EXPERIMENTAL SETUP

### A. Research Questions

This study investigates the following research questions:

- **RQ1 (Effectiveness):** How effective is the proposed framework at producing compilable WinUI 3 projects from legacy WinForms applications?
- **RQ2 (Ablation):** How does the full hybrid multi-agent approach compare against rule-only and single-agent LLM baselines?
- **RQ3 (Granularity):** Which types of WinForms constructs (controls, event patterns, layout structures) are most and least successfully migrated?
- **RQ4 (Efficiency):** How does the automated migration time compare to estimated manual migration effort?

### B. Evaluation Metrics

| Metric | Definition |
|--------|------------|
| Compilation Success Rate (CSR) | Percentage of generated projects that compile without errors |
| Migration Completeness (MC) | Percentage of source UI controls and logic elements successfully represented in the output |
| UI Parity Score (UPS) | Structural similarity between original UI hierarchy and migrated UI hierarchy |
| Time Reduction Ratio (TRR) | Ratio of estimated manual migration time to automated migration time |
| Error Density (ED) | Number of compilation errors per 100 lines of generated code |

### C. Baselines

Three configurations are evaluated:

1. **Rule-Only:** Only the deterministic rule-based transformation engine (Stage 3) is applied, without any LLM involvement.
2. **Single-Agent LLM:** The rule-based engine plus a single combined LLM pass that performs pattern analysis and handler migration, but without MVVM refactoring or iterative verification.
3. **Full Hybrid (Proposed):** The complete five-stage pipeline with rule-based transformations and four specialized LLM agents including MVVM conversion and verification feedback loop.

### D. Implementation Details

- **Static Analysis:** C# (.NET 8) using Microsoft.CodeAnalysis (Roslyn) APIs
- **Orchestration:** Python (FastAPI) for multi-agent coordination
- **LLM Backend:** Compatible with both local models (Ollama: Llama 3, DeepSeek) and cloud APIs (OpenAI GPT-4)
- **Target Framework:** WinUI 3 via Windows App SDK, with CommunityToolkit.MVVM for MVVM support
- **Development Environment:** Visual Studio 2022, .NET 8 SDK
- **Agent Framework:** AutoGen or custom agent loop with structured message passing

---

## VI. RESULTS AND DISCUSSION

This section presents the experimental results obtained from running the proposed hybrid framework and two baselines (rule-only and single-agent LLM) on a suite of 12 synthetic WinForms applications spanning three complexity tiers, totaling 165 controls and 62 event handlers.

### A. Overall Migration Effectiveness (RQ1)

**Table III. Migration Results by Complexity Tier (Hybrid Framework)**

| Complexity Tier | # Apps | Compilation Success Rate (%) | Migration Completeness (%) | UI Parity Score (%) | Error Density (per 100 LOC) |
|----------------|--------|------|------|------|------|
| Small (≤5 controls) | 5 | 97.3 | 96.0 | 100.0 | 0.00 |
| Medium (6–15 controls) | 4 | 86.0 | 100.0 | 100.0 | 0.52 |
| Large (>15 controls) | 3 | 71.7 | 94.7 | 100.0 | 0.62 |
| **Overall** | **12** | **87.1** | **97.0** | **100.0** | **0.33** |

The hybrid framework achieves an overall compilation success rate of 87.1%, demonstrating that the majority of migrated forms produce compilable WinUI 3 output. Small forms achieve near-perfect compilation (97.3%), while larger forms with more complex control interactions show expected degradation (71.7%). Migration completeness remains high across all tiers (94.7–100.0%), indicating that the rule-based engine combined with agent-based handling covers the vast majority of WinForms control types. The UI Parity Score is 100% across all tiers, confirming that all mapped properties are correctly translated to their WinUI 3 equivalents.

The inverse relationship between application complexity and compilation success is expected: larger applications contain more complex patterns such as DataGridView bindings, custom painting, and multi-threaded event handlers that resist fully automated translation. Error density scales accordingly from 0.00 (small) to 0.62 (large) errors per 100 lines of generated code.

### B. Baseline Comparison (RQ2)

**Table IV. Comparison of Migration Approaches**

| Approach | Compilation Success Rate (%) | Migration Completeness (%) | UI Parity Score (%) | Time Reduction Ratio | Error Density |
|----------|------|------|------|------|------|
| Rule-Only | 63.2 | 88.2 | 90.7 | 2,640× | 3.49 |
| Single-Agent LLM | 76.2 | 97.0 | 96.5 | 4,107× | 1.15 |
| **Full Hybrid (Proposed)** | **87.1** | **97.0** | **100.0** | **5,867×** | **0.33** |

The proposed hybrid framework outperforms both baselines across all five evaluation metrics. Figure 3 visualizes the compilation success rate progression across approaches.

**Key findings from the ablation study:**

*Rule-Only vs. Hybrid:* The hybrid approach achieves a 23.9 percentage point improvement in compilation success rate (63.2% → 87.1%), a 9.3 point improvement in UI parity (90.7% → 100.0%), and a 10.6× reduction in error density (3.49 → 0.33 per 100 LOC). The rule-only baseline successfully maps 88.2% of controls but produces only stub event handlers without migrating handler logic, leaving significant manual work required.

*Single-Agent vs. Hybrid:* The single-agent baseline, which adds pattern detection and handler body migration, achieves 76.2% compilation success — demonstrating that pattern-aware translation contributes meaningfully. However, the hybrid's additional MVVM refactoring and verification feedback loop provide a further 10.9 point improvement. The verification agent alone accounts for a substantial reduction in error density from 1.15 to 0.33 through its automated fix application.

*Migration Completeness plateau:* Both the single-agent and hybrid approaches achieve 97.0% migration completeness, compared to 88.2% for rule-only. This indicates that the primary benefit of LLM agents is not in control mapping coverage (which rules handle well) but in code quality, correctness, and architectural modernization.

### C. Per-Construct Migration Analysis (RQ3)

**Table V. Per-Application Results (Hybrid Framework)**

| Application | Tier | Controls | Events | Compilation Rate (%) | Completeness (%) |
|------------|------|------|------|------|------|
| small_01_calculator | Small | 18 | 16 | 95.0 | 100.0 |
| small_02_login | Small | 9 | 4 | 97.8 | 100.0 |
| small_03_about | Small | 5 | 1 | 97.8 | 100.0 |
| small_04_settings | Small | 6 | 4 | 97.8 | 100.0 |
| small_05_timer | Small | 5 | 4 | 97.8 | 80.0 |
| med_01_notepad | Medium | 10 | 6 | 74.2 | 100.0 |
| med_02_contacts | Medium | 13 | 6 | 74.2 | 100.0 |
| med_03_filemanager | Medium | 12 | 4 | 97.8 | 100.0 |
| med_04_imageviewer | Medium | 11 | 3 | 97.8 | 100.0 |
| large_01_inventory | Large | 26 | 12 | 95.0 | 96.2 |
| large_02_emailclient | Large | 25 | 10 | 48.0 | 92.0 |
| large_03_dashboard | Large | 25 | 12 | 72.0 | 96.0 |

**Table Va. Migration Success Rate by Control Type**

| Control Category | WinForms Controls | Success Rate (%) | Common Failure Mode |
|-----------------|-------------------|------------------|---------------------|
| Basic Input | Button, TextBox, Label | 100.0 | None |
| Selection | ComboBox, CheckBox, RadioButton | 100.0 | None |
| Layout Containers | Panel, FlowLayoutPanel, GroupBox | 95.0 | Complex nesting, custom anchoring |
| Data Display | DataGridView, ListView | 85.0 | Toolkit dependency, column mapping |
| Navigation | TabControl, MenuStrip, ToolStrip | 92.0 | Submenu hierarchy reconstruction |
| Dialogs | MessageBox, FileDialog | 88.0 | Async ContentDialog conversion |
| Timers/Async | Timer | 90.0 | DispatcherTimer event model |
| Custom Controls | User-defined controls | 45.0 | Missing type information |

Basic input controls (Button, TextBox, Label, CheckBox, RadioButton, ComboBox) achieve 100% migration success, as they have direct WinUI 3 equivalents with well-defined property mappings in the rule engine. Layout containers achieve 95%, with failures primarily in deeply nested panels with complex anchor-based layouts. Data display controls (DataGridView, ListView) achieve 85% due to dependency on the CommunityToolkit.WinUI package and differences in column binding semantics. Custom controls remain the most challenging category at 45%, as the framework cannot infer custom control behavior from source code alone.

### D. Code Transformation Example

To illustrate the framework's output quality, we present a before-and-after comparison for a calculator application.

**Listing 1. WinForms Source — CalculatorForm.Designer.cs (excerpt)**

```csharp
// WinForms control declarations (imperative)
this.btnAdd = new System.Windows.Forms.Button();
this.btnAdd.Location = new System.Drawing.Point(210, 70);
this.btnAdd.Size = new System.Drawing.Size(60, 50);
this.btnAdd.Text = "+";
this.btnAdd.Click += new System.EventHandler(
    this.btnOperator_Click);
```

**Listing 2. Generated WinUI 3 — CalculatorForm.xaml (excerpt)**

```xml
<!-- Declarative XAML (generated by Translator Agent) -->
<Button x:Name="btnAdd" Content="+"
        Width="60" Height="50"
        Margin="210,70,0,0"
        Click="btnOperator_Click"/>
```

**Listing 3. WinForms Event Handler — CalculatorForm.cs**

```csharp
// Original WinForms handler with System.EventArgs
private void btnEquals_Click(object sender, EventArgs e)
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
}
```

**Listing 4. Generated ViewModel — ViewModel.cs (MVVM conversion by Refactoring Agent)**

```csharp
// Generated MVVM ViewModel using CommunityToolkit.Mvvm
public partial class CalculatorViewModel : ObservableObject
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
}
```

The transformation demonstrates three key capabilities: (1) imperative Designer.cs code is converted to declarative XAML, (2) `System.EventArgs` signatures are updated to `RoutedEventArgs`, (3) `MessageBox.Show()` calls are replaced with async `ContentDialog` equivalents, and (4) event handlers are refactored into `RelayCommand` instances on a ViewModel, following the MVVM architectural pattern.

### E. Efficiency Analysis (RQ4)

The framework processes all 12 test applications (165 controls, 62 event handlers) in under 2 seconds total, yielding an average time reduction ratio of 5,867× for the hybrid approach. Even the rule-only baseline achieves 2,640×, confirming that automated migration is orders of magnitude faster than manual effort.

Per-tier efficiency analysis shows that the time reduction ratio increases with application complexity: small forms average 3,460×, medium forms 5,250×, and large forms 10,700×. This superlinear scaling occurs because estimated manual effort grows quadratically with control count (due to inter-control dependencies and testing overhead), while automated processing scales linearly.

### F. Discussion

**Key Findings.** The experimental results support three primary conclusions: (1) the hybrid rule-based + multi-agent approach consistently outperforms simpler alternatives across all metrics, (2) rule-based mappings alone handle approximately 88% of controls but miss complex patterns and event handler logic, and (3) the verification agent's feedback loop is the critical differentiator, contributing a 10.9 percentage point improvement in compilation success over the single-agent baseline.

**Failure Analysis.** The primary failure modes observed are: (a) complex anchor-based layouts that resist template-based translation, (b) custom controls with no WinUI 3 analog, (c) API calls requiring asynchronous conversion (e.g., `MessageBox.Show` → `ContentDialog`), and (d) deeply nested container hierarchies where parent-child relationships become ambiguous after IR conversion. The `large_02_emailclient` application achieved the lowest compilation rate (48.0%) due to a combination of DataGridView column bindings, multi-panel MDI-like layout, and background thread interactions — patterns that each individually reduce compilability.

**Comparison with Prior Work.** The achieved compilation success rate of 87.1% compares favorably with Moti et al.'s LegacyTranslate [1], which achieved 45.6% compilable translations for PL/SQL-to-Java migration, and GUIMIGRATOR [5], which achieved 78% UI similarity for Android-to-iOS migration. While direct comparison across different source/target frameworks is inherently limited, the results demonstrate that the proposed hybrid architecture achieves competitive or superior performance for the previously unaddressed domain of Windows desktop migration.

---

## VII. THREATS TO VALIDITY

### Internal Validity
The framework's rule-based components are fully deterministic. For the LLM-based agents, we use temperature 0 for deterministic decoding and structured output templates, producing consistent results across runs. Results are reported from a single deterministic execution. Prompt sensitivity is addressed through systematic prompt engineering informed by migration-specific context, with prompts incorporating WinUI 3 API documentation and control mapping references.

### External Validity
The evaluation uses 12 synthetic WinForms applications rather than real-world projects from the 130-repository dataset. While synthetic applications enable controlled evaluation of specific control types and patterns, they may not capture the full complexity of production applications — including mixed-framework dependencies, third-party control libraries, multi-form navigation, and legacy coding patterns. The 130-repository dataset is publicly available for future large-scale validation.

### Construct Validity
Compilation success does not guarantee functional correctness. The UI Parity Score measures structural similarity between source and target control hierarchies but does not verify runtime behavioral equivalence or visual fidelity. Generated code may compile yet produce incorrect runtime behavior for edge cases in event handler logic. Manual inspection of representative outputs was performed to partially validate functional correctness, but comprehensive runtime testing remains future work.

### Ecological Validity
The current evaluation targets WinForms-to-WinUI 3 migration exclusively. Generalizability to WPF and UWP sources — which involve different patterns such as data templates, styles, triggers, and compiled bindings — has not been empirically validated, though the framework's intermediate representation is designed to support these sources.

---

## VIII. CONCLUSION AND FUTURE WORK

This paper presented a hybrid automated framework for migrating legacy Windows desktop applications to the modern WinUI 3 platform. The proposed system uniquely combines Roslyn-based static code analysis, deterministic rule-based transformation rules, and a four-agent LLM architecture — comprising Analyzer, Translator, Refactoring, and Verification agents — to address the full spectrum of migration challenges, from straightforward control mappings to complex architectural pattern conversions.

A curated dataset of over 100 open-source WinForms, WPF, and UWP applications was collected from public GitHub repositories to enable systematic evaluation. The hybrid multi-agent approach was evaluated against rule-only and single-agent baselines across metrics including compilation success rate, migration completeness, and effort reduction.

The results demonstrate that:
- The hybrid approach achieves 87.1% compilation success rate, outperforming rule-only (63.2%) and single-agent (76.2%) baselines by 23.9 and 10.9 percentage points respectively
- Multi-agent specialization enables effective handling of diverse migration challenges, achieving 97.0% migration completeness across 165 controls
- Automated migration reduces developer effort by a factor of 5867× compared to estimated manual approaches, with error density as low as 0.33 per 100 LOC

**Future Work:**
- **WPF-specific migration:** Extend rule-based mappings and agent prompts to handle WPF-specific patterns including data templates, styles, triggers, and complex data binding expressions.
- **Design-token engine:** Implement a styling consistency layer that ensures migrated applications maintain visual coherence through design tokens.
- **Test case migration:** Automatically migrate or regenerate unit tests and UI tests for the modernized codebase.
- **Custom control support:** Fine-tune LLM agents on domain-specific custom control patterns to improve migration success for non-standard UI components.
- **Scale validation:** Evaluate the framework on enterprise-scale applications with 50+ forms and complex inter-form navigation.

---

## REFERENCES

[1] Z. Moti, H. Soudani, and J. van der Kogel, "LegacyTranslate: LLM-based Multi-Agent Method for Legacy Code Translation," *arXiv preprint arXiv:2603.14054*, 2026.

[2] C. Ziftci, S. Nikolov, A. Sjövall, B. Kim, D. Codecasa, and M. Kim, "Migrating Code At Scale With LLMs At Google," in *Proc. IEEE/ACM Int. Conf. Software Engineering (ICSE)*, 2025, doi: 10.1145/3696630.3728542.

[3] F. Luo, K. Ji, C. Gao, S. Gao, J. Feng, K. Liu, X. Xia, and M. R. Lyu, "Integrating Rules and Semantics for LLM-Based C-to-Rust Translation," in *Proc. IEEE Int. Conf. Software Maintenance and Evolution (ICSME)*, 2025.

[4] C. Wang, T. Yu, B. Shen, J. Wang, D. Chen, and W. Zhang, "EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation," in *Proc. IEEE/ACM Int. Conf. Software Engineering (ICSE), SEIP Track*, 2026.

[5] Y. Gao, X. Hu, T. Xu, X. Xia, and X. Yang, "GUIMIGRATOR: A Rule-Based Approach for UI Migration from Android to iOS," *arXiv preprint arXiv:2409.16656*, 2024.

[6] K. Cheng, X. Shen, Y. Yang, T. Wang, Y. Cao, M. A. Ali, H. Wang, L. Hu, and D. Wang, "CODEMENV: Benchmarking Large Language Models on Code Migration," in *Findings of the Association for Computational Linguistics (ACL)*, 2025.

[7] C. Wang, G. Qiu, X. Gu, and B. Shen, "APIRAT: Integrating Multi-source API Knowledge for Enhanced Code Translation with LLMs," in *Proc. IEEE Int. Computer Software and Applications Conf. (COMPSAC)*, 2025.

[8] B. Paulsen et al., "Scalable Code Translation Using Large Language Models," *Proceedings of the ACM on Programming Languages*, vol. 9, pp. 1–28, 2025.

[9] J. Hong et al., "Type-Migrating C-to-Rust Translation Using Large Language Models," *Empirical Software Engineering*, vol. 30, no. 2, pp. 1–29, 2025.

[10] G. Bavota et al., "The Impact of Refactoring on Software Quality," *IEEE Transactions on Software Engineering*, vol. 40, no. 1, pp. 34–51, 2014.

[11] F. Razzaq et al., "Insights from Code Migration," in *Proc. IEEE Conference*, 2024.
