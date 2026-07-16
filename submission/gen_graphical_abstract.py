import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

os.chdir(r"D:\麻醉科共病\ra-painkg\submission")

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_facecolor('#FAFAFA')
fig.patch.set_facecolor('#FAFAFA')

# Color scheme
c_blue = '#2E86AB'
c_orange = '#D64045'
c_green = '#2A7F3F'
c_gray = '#666666'
c_light = '#E8F4F8'
c_warn = '#FFF3CD'
c_dark = '#1a1a2e'

def add_box(ax, x, y, w, h, text, color, fontsize=10, bold=False, fontcolor='white', edgecolor=None):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor=edgecolor or color,
                         linewidth=1.5, alpha=0.95)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, color=fontcolor, weight=weight,
            fontfamily='sans-serif')

def add_arrow(ax, x1, y1, x2, y2, color='#888888', lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                               connectionstyle='arc3,rad=0'))

# === TITLE ===
ax.text(7, 7.6, 'Multi-Split Ablation Benchmark for Knowledge Graph Perturbation Prediction',
        ha='center', va='center', fontsize=16, weight='bold', color=c_dark,
        fontfamily='sans-serif')
ax.text(7, 7.25, 'Yongxin Yang | J. Biomed. Inform. | 2026',
        ha='center', va='center', fontsize=9, color=c_gray,
        fontfamily='sans-serif', style='italic')

# === ROW 1: WORKFLOW ===
y1 = 6.2
boxes_row1 = [
    (0.3, y1, 2.2, 0.75, 'Norman Perturb-seq\n91,205 K562 cells\n5,045 genes', c_blue),
    (2.8, y1, 2.2, 0.75, '11 KG Variants\nGO / RA-PainKG / Random\nAblation / Identity / STRING', c_blue),
    (5.3, y1, 2.2, 0.75, 'Spectral Embedding\nk=128 Laplacian\neigenvectors', c_blue),
    (7.8, y1, 2.2, 0.75, 'Ridge Regression\n10 splits (80/20%)\nPaired t-tests', c_blue),
    (10.3, y1, 2.2, 0.75, 'Sensitivity Analysis\nalpha 0.001–100\nk = 32–512', c_blue),
]
for x, y, w, h, txt, c in boxes_row1:
    add_box(ax, x, y, w, h, txt, c, fontsize=8, bold=False)

for i in range(len(boxes_row1)-1):
    add_arrow(ax, boxes_row1[i][0]+boxes_row1[i][2], boxes_row1[i][1]+0.35,
              boxes_row1[i+1][0], boxes_row1[i+1][1]+0.35, '#AAAAAA', 1.5)

# === ROW 2: KEY RESULTS ===
y2 = 4.5
ax.text(0.3, y2 + 0.5, 'KEY RESULTS', fontsize=11, weight='bold', color=c_dark, fontfamily='sans-serif')

# Bar chart for key comparison
bar_data = [
    ('Random_R1', 0.667, 0.620, c_orange),
    ('GO-BP', 0.589, 0.542, c_blue),
    ('GO-painCentric', 0.604, 0.523, '#5BA0C8'),
    ('RA-PainKG', 0.551, 0.503, c_green),
]

bar_x = np.arange(len(bar_data))
bar_w = 0.35
for i, (name, r_all, r_pain, color) in enumerate(bar_data):
    # Transform to figure coordinates
    bx = 0.8 + i * 1.5
    by = y2 - 0.8
    # All-genes bar
    bar_h_all = r_all * 1.2
    rect1 = FancyBboxPatch((bx, by), bar_w, bar_h_all, boxstyle="round,pad=0.05",
                           facecolor=color, edgecolor=color, alpha=0.9, linewidth=0.5)
    ax.add_patch(rect1)
    ax.text(bx + bar_w/2, by + bar_h_all + 0.05, f'{r_all:.3f}', ha='center', fontsize=7.5, color=color, weight='bold')
    
    # Pain-genes bar
    bar_h_pain = r_pain * 1.2
    bx2 = bx + bar_w + 0.08
    rect2 = FancyBboxPatch((bx2, by), bar_w, bar_h_pain, boxstyle="round,pad=0.05",
                           facecolor=color, edgecolor=color, alpha=0.45, linewidth=0.5, hatch='///')
    ax.add_patch(rect2)
    ax.text(bx2 + bar_w/2, by + bar_h_pain + 0.05, f'{r_pain:.3f}', ha='center', fontsize=7.5, color=color, alpha=0.7)
    
    # Label
    ax.text(bx + bar_w + 0.04, by - 0.2, name, ha='center', fontsize=8, color=c_dark, weight='bold',
            rotation=25)

# Legend
legend_y = y2 - 1.5
p1 = mpatches.Patch(facecolor=c_orange, alpha=0.9, label='All-genes Pearson r')
p2 = mpatches.Patch(facecolor=c_orange, alpha=0.45, hatch='///', label='Pain-genes Pearson r')
ax.legend(handles=[p1, p2], loc='upper left', bbox_to_anchor=(0.3, legend_y+1.3),
          fontsize=7.5, framealpha=0.8)

# === ROW 3: KEY FINDINGS ===
y3 = 2.3
findings = [
    ('1', 'Single-split ARTIFACT: RA-PainKG > GO (r=0.558 vs 0.481)\nreversed under multi-split (0.503 vs 0.542)', c_warn),
    ('2', 'CAUSAL evidence: degree-preserving randomization\n→ performance unchanged (p = 0.41–0.83)', c_light),
    ('3', 'DENSITY drives prediction: Random > GO > RA-PainKG\nKendall W = 0.64–0.65 across 10 splits', c_light),
]
for i, (num, txt, color) in enumerate(findings):
    fx = 0.3 + i * 4.5
    fy = y3
    add_box(ax, fx, fy, 4.2, 1.2, '', color, edgecolor='#CCCCCC', fontcolor=c_dark)
    ax.text(fx + 0.2, fy + 1.0, num, fontsize=18, weight='bold', color=c_orange if i==0 else c_blue,
            fontfamily='sans-serif', va='top')
    ax.text(fx + 0.7, fy + 0.6, txt, fontsize=7.5, color=c_dark, fontfamily='sans-serif', va='center')

# === ROW 4: BOTTOM LINE ===
y4 = 0.8
add_box(ax, 0.3, y4, 4.2, 0.9,
        'METHODOLOGICAL CONTRIBUTION\nOpen-source multi-split ablation\nbenchmark framework',
        c_dark, edgecolor=c_dark, fontsize=8)

add_box(ax, 4.8, y4, 4.2, 0.9,
        'LIMITATION\nK562: 59.1% pain genes below\nexpression threshold',
        '#8B0000', edgecolor='#8B0000', fontsize=8)

add_box(ax, 9.3, y4, 4.2, 0.9,
        'NEXT STEP\nSensory neuron / DRG models\nfor domain-KG validation',
        c_green, edgecolor=c_green, fontsize=8)

plt.tight_layout(pad=0.5)
plt.savefig('graphical_abstract.pdf', dpi=300, bbox_inches='tight', facecolor='#FAFAFA', edgecolor='none')
plt.savefig('graphical_abstract.png', dpi=300, bbox_inches='tight', facecolor='#FAFAFA', edgecolor='none')
print("Graphical abstract saved: graphical_abstract.pdf, graphical_abstract.png")

# Also create Mermaid version for reference
mermaid = '''
```mermaid
flowchart TD
    A["Norman Perturb-seq<br/>91,205 K562 cells<br/>5,045 genes"] --> B["11 KG Variants<br/>GO / RA-PainKG / Random ×5<br/>degPreserved / painCentric<br/>Identity / STRING"]
    B --> C["Spectral Embedding<br/>k=128 Laplacian"]
    C --> D["Ridge Regression<br/>10 splits (80/20%)"]
    D --> E["Statistical Evaluation<br/>Paired t-tests / Kendall W<br/>alpha & k sensitivity"]
    
    E --> F1["🔴 Single-Split ARTIFACT<br/>RA-PainKG > GO (r=0.558 vs 0.481)<br/>→ reversed: 0.503 vs 0.542"]
    E --> F2["🟢 CAUSAL Evidence<br/>degPreserved ~ RA-PainKG<br/>p = 0.41–0.83"]
    E --> F3["🔵 DENSITY Drives Prediction<br/>Random > GO > RA-PainKG<br/>W = 0.64–0.65"]
    
    F1 --> G["Methodology Contribution:<br/>Multi-split ablation benchmark"]
    F2 --> G
    F3 --> G
    
    G --> H["Next: Sensory Neuron Models"]
    
    style A fill:#2E86AB,color:#fff
    style B fill:#2E86AB,color:#fff
    style C fill:#2E86AB,color:#fff
    style D fill:#2E86AB,color:#fff
    style E fill:#2E86AB,color:#fff
    style F1 fill:#FFF3CD,color:#333
    style F2 fill:#E8F4F8,color:#333
    style F3 fill:#E8F4F8,color:#333
    style G fill:#1a1a2e,color:#fff
    style H fill:#2A7F3F,color:#fff
```
'''
with open('graphical_abstract_mermaid.md', 'w', encoding='utf-8') as f:
    f.write(mermaid)
print("Mermaid version saved: graphical_abstract_mermaid.md")