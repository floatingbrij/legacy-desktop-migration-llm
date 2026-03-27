"""
Generate all figures for the paper as PNG images.
Produces:
  - figures/architecture.png (5-stage pipeline)
  - figures/agents.png (4-agent workflow)
  - figures/baseline_chart.png (CSR/MC/UPS bar chart)
  - figures/tier_chart.png (CSR by complexity tier)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("figures", exist_ok=True)

# ============================================================
# Figure 1: Architecture Pipeline
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 4))
ax.set_xlim(0, 12)
ax.set_ylim(0, 4)
ax.axis('off')

stages = [
    ("Stage 1\nStatic Analysis\n(Roslyn Parser)", "#BBDEFB"),
    ("Stage 2\nIntermediate\nRepresentation", "#C8E6C9"),
    ("Stage 3\nRule Engine\n(28 Rules)", "#F8BBD0"),
    ("Stage 4\nMulti-Agent\nLLM Pipeline", "#D1C4E9"),
    ("Stage 5\nOutput Assembly\n& Validation", "#B2EBF2"),
]

box_w, box_h = 1.8, 2.5
gap = 0.3
start_x = 0.3
y = 0.7

for i, (label, color) in enumerate(stages):
    x = start_x + i * (box_w + gap)
    rect = mpatches.FancyBboxPatch((x, y), box_w, box_h, 
                                    boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#333333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + box_w/2, y + box_h/2, label, ha='center', va='center',
            fontsize=9, fontweight='bold', fontfamily='sans-serif')
    
    if i < len(stages) - 1:
        ax.annotate('', xy=(x + box_w + gap, y + box_h/2),
                    xytext=(x + box_w, y + box_h/2),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#333333'))

# Input/Output labels
ax.text(0.15, y + box_h/2, "WinForms\nSource", ha='right', va='center', fontsize=8,
        color='#666666', fontstyle='italic')
final_x = start_x + 4 * (box_w + gap) + box_w
ax.text(final_x + 0.15, y + box_h/2, "WinUI 3\nProject", ha='left', va='center', fontsize=8,
        color='#666666', fontstyle='italic')

fig.suptitle("Fig. 1: Five-Stage Pipeline Architecture", fontsize=12, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig("figures/architecture.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figures/architecture.png")

# ============================================================
# Figure 2: Multi-Agent Pipeline
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.5)
ax.axis('off')

agents = [
    ("Agent 1\nAnalyzer", "Pattern detection\n10 categories\nTransformation plan", "#E3F2FD"),
    ("Agent 2\nTranslator", "XAML generation\nCode-behind\nHandler migration", "#E8F5E9"),
    ("Agent 3\nRefactoring", "MVVM conversion\nObservableObject\nRelayCommand", "#FFF3E0"),
    ("Agent 4\nVerification", "XAML/C# validation\nAPI leak detection\nAuto-fix patches", "#FCE4EC"),
]

box_w, box_h = 2.0, 3.0
gap = 0.35
start_x = 0.3
y = 1.5

for i, (title, desc, color) in enumerate(agents):
    x = start_x + i * (box_w + gap)
    rect = mpatches.FancyBboxPatch((x, y), box_w, box_h,
                                    boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#333333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + box_w/2, y + box_h - 0.4, title, ha='center', va='center',
            fontsize=10, fontweight='bold')
    ax.text(x + box_w/2, y + box_h/2 - 0.3, desc, ha='center', va='center',
            fontsize=7, fontfamily='sans-serif')
    
    if i < len(agents) - 1:
        ax.annotate('', xy=(x + box_w + gap, y + box_h/2),
                    xytext=(x + box_w, y + box_h/2),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#333333'))

# Feedback loop arrow
x4 = start_x + 3 * (box_w + gap)
x2 = start_x + 1 * (box_w + gap)
ax.annotate('', xy=(x2 + box_w/2, y - 0.1),
            xytext=(x4 + box_w/2, y - 0.1),
            arrowprops=dict(arrowstyle='->', lw=2, color='red', 
                          connectionstyle='arc3,rad=0.3', linestyle='dashed'))
ax.text((x2 + x4) / 2 + box_w/2, y - 0.5, "Feedback Loop (fix patches)",
        ha='center', va='center', fontsize=8, color='red', fontstyle='italic')

# IR input
ax.text(0.15, y + box_h/2, "IR +\nRules", ha='right', va='center', fontsize=8,
        color='#666666', fontstyle='italic')
# Output
ax.text(start_x + 3 * (box_w + gap) + box_w + 0.15, y + box_h/2, 
        "Validated\nOutput", ha='left', va='center', fontsize=8,
        color='#666666', fontstyle='italic')

fig.suptitle("Fig. 2: Multi-Agent LLM Pipeline Architecture", fontsize=12, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig("figures/agents.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figures/agents.png")

# ============================================================
# Figure 3: Baseline Comparison Bar Chart
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

approaches = ['Rule-Only', 'Single-Agent', 'Full Hybrid\n(Proposed)']
csr = [63.2, 76.2, 87.1]
mc = [88.2, 97.0, 97.0]
ups = [90.7, 96.5, 100.0]

x = np.arange(len(approaches))
width = 0.25

bars1 = ax.bar(x - width, csr, width, label='Compilation Success Rate (%)', color='#0066CC', edgecolor='white')
bars2 = ax.bar(x, mc, width, label='Migration Completeness (%)', color='#009933', edgecolor='white')
bars3 = ax.bar(x + width, ups, width, label='UI Parity Score (%)', color='#CC6600', edgecolor='white')

ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(approaches, fontsize=11)
ax.set_ylim(0, 110)
ax.legend(loc='upper left', fontsize=9)
ax.grid(axis='y', alpha=0.3)

# Value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1,
                f'{h:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.set_title('Fig. 3: Baseline Comparison Across All Metrics', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig("figures/baseline_chart.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figures/baseline_chart.png")

# ============================================================
# Figure 4: Tier-wise Results Bar Chart
# ============================================================
fig, ax = plt.subplots(figsize=(7, 5))

tiers = ['Small\n(≤5 controls)', 'Medium\n(6–15 controls)', 'Large\n(>15 controls)']
tier_csr = [97.3, 86.0, 71.7]
tier_ed = [0.00, 0.52, 0.62]

x = np.arange(len(tiers))
colors = ['#4CAF50', '#FFC107', '#F44336']

bars = ax.bar(x, tier_csr, 0.5, color=colors, edgecolor='white', linewidth=1.5)

for bar, val in zip(bars, tier_csr):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Compilation Success Rate (%)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(tiers, fontsize=11)
ax.set_ylim(0, 110)
ax.grid(axis='y', alpha=0.3)

# Secondary axis for error density
ax2 = ax.twinx()
ax2.plot(x, tier_ed, 'ko-', linewidth=2, markersize=8, label='Error Density')
for i, val in enumerate(tier_ed):
    ax2.text(i + 0.15, val + 0.03, f'{val:.2f}', fontsize=9, fontweight='bold')
ax2.set_ylabel('Error Density (per 100 LOC)', fontsize=11)
ax2.set_ylim(-0.1, 1.0)
ax2.legend(loc='upper right', fontsize=9)

ax.set_title('Fig. 4: Compilation Success Rate by Complexity Tier', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig("figures/tier_chart.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figures/tier_chart.png")

print("\nAll 4 figures generated in figures/")
