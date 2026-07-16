import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# FIX 1: Move Table 1 (structural characteristics) to Supplementary
# ============================================================

# Find Table 1 block and replace with a reference to supplementary
old_t1 = """**Table 1. KG variant structural characteristics**

| KG Variant | Edges | Density | Mean Degree | Coverage (%) |
|-----------|-------|---------|-------------|-------------|
| GO-BP | 673,899 | 0.02648 | 267.1 | 100 |
| Random (5 graphs; range) | 673,899 | 0.02648 | 267.1 | 100 |
| GO-painCentric | 121,543 | 0.00478 | 48.2 | 100 |
| RA-PainKG | 2,400 | 0.00009 | 1.0 | 31.7 |
| RA-PainKG-degPreserved | 2,400 | 0.00009 | 1.0 | 31.7 |
| Identity | 0 | 0 | 0 | 0 |
| STRING (gene-symbol filtered) | 15,403 | 0.00061 | 6.1 | 100 |

RA-PainKG is 280-fold sparser than GO, with 68.3% of genes having zero edges."""

new_t1 = """RA-PainKG is 280-fold sparser than GO (2,400 vs 673,899 edges), with 68.3% of genes having zero edges. Complete structural characteristics for all 11 KG variants are provided in Supplementary Table S6."""

content = content.replace(old_t1, new_t1)
print("[OK] Table 1 moved to supplementary")

# Renumber remaining tables (Table 2 -> Table 1, Table 3 -> Table 2)
content = content.replace("**Table 2. Multi-split benchmark results", "**Table 1. Multi-split benchmark results")
content = content.replace("**Table 3. Paired comparisons", "**Table 2. Paired comparisons")

# Update table references in text
content = content.replace("in Table 3", "in Table 2")
content = content.replace("Table 3", "Table 2")  # careful - Table 3 may appear in multiple places
# But Table 2 references should now be Table 1
content = content.replace("Table 2", "Table 1")  # This changes all remaining
# Restore the Table 2 -> Table 1 issue by making sure Table 2 is only for what was Table 3
# Actually, let me do this more carefully

# Reset and redo numbering
content = content.replace("Table 1", "Table TEMP")
content = content.replace("Table 2", "Table 1")  # Old Table 2 -> 1
content = content.replace("Table TEMP", "Table 2")  # Old Table 3 -> 2

print("[OK] Tables renumbered: Table 1 (benchmark), Table 2 (paired comparisons)")

# Verify counts
import re
table_mentions = re.findall(r'\*\*Table (\d+)', content)
print(f"Tables now: {sorted(set(int(x) for x in table_mentions))}")

# ============================================================
# FIX 2: Compress abstract from 448 to <=350 words
# ============================================================

old_abstract_start = "## Abstract"
old_abstract_end = "**Keywords:**"

# Extract abstract
abs_start = content.index(old_abstract_start)
abs_end = content.index(old_abstract_end, abs_start)
old_abs = content[abs_start:abs_end]

new_abstract = """## Abstract

**Objective:** To establish rigorous methodology for benchmarking knowledge graph (KG) contributions to gene perturbation prediction, and to determine whether domain-specific edge semantics improve prediction beyond graph connectivity alone.

**Materials and Methods:** We benchmarked 11 KG variants—GO Biological Process, RA-PainKG, five dense random graphs (673,899 edges each), two ablation variants (degree-preserving randomization and pain-gene-centric GO reduction), an Identity baseline, and STRING—on the Norman et al. (2019) Perturb-seq dataset (91,205 K562 cells, 5,045 genes). Gene embeddings were computed via spectral decomposition (k = 128). Perturbation effects were predicted via ridge regression across 10 independent splits (80%/20%), with paired t-tests, delta-r confidence intervals, and sensitivity analyses (alpha = 0.001–100.0, k = 32–512).

**Results:** Dense random graphs consistently achieved highest accuracy. A representative random graph (Random_R1) achieved Pearson r = 0.667 (all genes) and 0.620 (pain genes, n = 44 overlapping), significantly outperforming GO (r = 0.589, 0.542; delta = +0.078, p < 0.001) and RA-PainKG (pain r = 0.503; delta = +0.117, p < 0.001). RA-PainKG did not differ from GO (delta = −0.039, 95% CI [−0.078, +0.000], p = 0.084). Degree-preserving randomization left performance unchanged (p = 0.41–0.83), providing causal evidence that graph connectivity, not edge semantics, drives prediction. Cross-split consistency was moderate (Kendall's W = 0.64–0.65).

**Discussion:** Single-split evaluation produces artifacts: RA-PainKG appeared to outperform GO in one split (r = 0.558 vs 0.481) but reversed under multi-split averaging (0.503 vs 0.542). The K562 system limits pain-specific conclusions (59.1% of measurable pain genes below expression threshold).

**Conclusion:** We provide an open-source multi-split ablation framework demonstrating that single-split KG evaluation generates misleading conclusions. Graph connectivity, not domain-specific edge semantics, drives linear perturbation prediction.

**Availability:** Code and data at https://github.com/yyx-4113/ra-painkg (MIT license).

"""

content = content.replace(old_abs, new_abstract)

# Verify abstract word count
abs_text = new_abstract
abs_text = re.sub(r'\*\*', '', abs_text)
abs_text = re.sub(r'\[|\]|\(|\)|`|#+ ', '', abs_text)
abs_text = re.sub(r'\s+', ' ', abs_text).strip()
abs_words = len(abs_text.split())
print(f"\nNew abstract word count: {abs_words} (limit: 350)")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("[OK] All fixes applied")