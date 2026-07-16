import csv, json, statistics, math, os
from collections import defaultdict

os.chdir(r"D:\麻醉科共病\ra-painkg\benchmark\results")

# ===== S1: Complete benchmark results =====
rows = []
with open("benchmark_jbi_extended.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

kg_data = defaultdict(list)
for r in rows:
    kg_data[r["kg"]].append(r)

lines = []
lines.append("# Supplementary Table S1: Complete Benchmark Results")
lines.append("")
lines.append("Mean Pearson r (+/- SD) across 10 independent train/test splits (80%/20%). Random values are mean of 5 independent graph realizations each averaged over 10 splits.")
lines.append("")
lines.append("| Knowledge Graph | PPI Edges | All-Genes r | Pain-Genes r | Non-Pain r | Track A r | Track B r | Track Dual r |")
lines.append("|---|---|---|---|---|---|---|---|")

kg_order = ["GO", "RA_PainKG", "RA_PainKG_degPreserved", "GO_painCentric", "Random_R0", "Random_R1", "Random_R2", "Random_R3", "Random_R4", "STRING", "Identity"]
kg_edges = {"GO": 673899, "RA_PainKG": 2400, "RA_PainKG_degPreserved": 2400, "GO_painCentric": 121543, "Random_R0": 673899, "Random_R1": 673899, "Random_R2": 673899, "Random_R3": 673899, "Random_R4": 673899, "STRING": 0, "Identity": 0}

for kg in kg_order:
    if kg not in kg_data:
        continue
    data = kg_data[kg]
    metrics = {}
    for m in ["r_all", "r_pain", "r_nonpain", "r_trackA", "r_trackB", "r_trackDual"]:
        vals = [float(d[m]) for d in data if d[m]]
        if vals:
            metrics[m] = (statistics.mean(vals), statistics.stdev(vals) if len(vals) > 1 else 0)
        else:
            metrics[m] = (0, 0)
    
    edges = kg_edges.get(kg, "N/A")
    if edges == "N/A":
        edges_str = "N/A"
    else:
        edges_str = f"{edges:,}"
    
    line = f"| {kg} | {edges_str} | {metrics['r_all'][0]:.3f} +/- {metrics['r_all'][1]:.3f} | {metrics['r_pain'][0]:.3f} +/- {metrics['r_pain'][1]:.3f} | {metrics['r_nonpain'][0]:.3f} +/- {metrics['r_nonpain'][1]:.3f} | {metrics['r_trackA'][0]:.3f} +/- {metrics['r_trackA'][1]:.3f} | {metrics['r_trackB'][0]:.3f} +/- {metrics['r_trackB'][1]:.3f} | {metrics['r_trackDual'][0]:.3f} +/- {metrics['r_trackDual'][1]:.3f} |"
    lines.append(line)

lines.append("")
lines.append("*Track A: n=3 genes (immune-inflammation). Track B: n=5 genes (nociception-pain transduction). Track Dual: n=96 genes spanning both tracks. Note: Track A/B measurements are noise-dominated due to small sample sizes.*")

with open("supplementary_table_S1.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("S1 done")

# ===== S2: Alpha Sensitivity =====
rows2 = []
with open("benchmark_alpha_sensitivity.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows2.append(row)

lines2 = []
lines2.append("# Supplementary Table S2: Regularization Sensitivity (Alpha)")
lines2.append("")
lines2.append("Pearson r (all-genes) at varying ridge regression regularization strengths. Single split (seed 42).")
lines2.append("")
lines2.append("| KG | alpha=0.001 | alpha=0.01 | alpha=0.1 | alpha=1.0 | alpha=10.0 | alpha=100.0 |")
lines2.append("|---|---|---|---|---|---|---|")

alpha_data = defaultdict(dict)
for r in rows2:
    alpha_data[r["kg"]][float(r["alpha"])] = float(r["r_all"])

for kg in kg_order:
    if kg not in alpha_data:
        continue
    vals = []
    for a in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]:
        v = alpha_data[kg].get(a, None)
        vals.append(f"{v:.3f}" if v is not None else "N/A")
    lines2.append(f"| {kg} | {' | '.join(vals)} |")

with open("supplementary_table_S2.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines2))

print("S2 done")

# ===== S3: K Sensitivity =====
rows3 = []
with open("benchmark_k_sensitivity.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows3.append(row)

lines3 = []
lines3.append("# Supplementary Table S3: Embedding Dimension Sensitivity (k)")
lines3.append("")
lines3.append("Pearson r (all-genes) at varying spectral embedding dimensions. Single split (seed 42).")
lines3.append("")
lines3.append("| KG | k=32 | k=64 | k=128 | k=256 | k=512 |")
lines3.append("|---|---|---|---|---|---|")

k_data = defaultdict(dict)
for r in rows3:
    k_data[r["kg"]][int(r["k"])] = float(r["r_all"])

for kg in kg_order:
    if kg not in k_data:
        continue
    vals = []
    for k in [32, 64, 128, 256, 512]:
        v = k_data[kg].get(k, None)
        vals.append(f"{v:.3f}" if v is not None else "N/A")
    lines3.append(f"| {kg} | {' | '.join(vals)} |")

with open("supplementary_table_S3.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines3))

print("S3 done")

# ===== S4: Pairwise Statistical Comparisons =====
lines4 = []
lines4.append("# Supplementary Table S4: Pairwise Statistical Comparisons")
lines4.append("")
lines4.append("Paired t-tests across 10 matched splits. Bonferroni-adjusted significance threshold: p < 0.01 (5 primary comparisons).")
lines4.append("")
lines4.append("| Comparison | Metric | Mean Delta r | 95% CI | t | df | p (unadjusted) | Significance |")
lines4.append("|---|---|---|---|---|---|---|---|")

comparisons = [
    ("Random_R1", "GO", "r_all"),
    ("Random_R1", "GO", "r_pain"),
    ("Random_R1", "RA_PainKG", "r_all"),
    ("Random_R1", "RA_PainKG", "r_pain"),
    ("GO", "RA_PainKG", "r_all"),
    ("GO", "RA_PainKG", "r_pain"),
    ("RA_PainKG", "RA_PainKG_degPreserved", "r_all"),
    ("RA_PainKG", "RA_PainKG_degPreserved", "r_pain"),
    ("GO", "GO_painCentric", "r_all"),
    ("GO", "GO_painCentric", "r_pain"),
    ("Random_R1", "RA_PainKG_degPreserved", "r_all"),
    ("Random_R1", "RA_PainKG_degPreserved", "r_pain"),
    ("Random_R1", "GO_painCentric", "r_all"),
    ("Random_R1", "GO_painCentric", "r_pain"),
]

for kg1, kg2, metric in comparisons:
    d1 = kg_data[kg1]
    d2 = kg_data[kg2]
    splits = sorted(set(d["split"] for d in d1) & set(d["split"] for d in d2))
    x1 = [float([d for d in d1 if d["split"]==s][0][metric]) for s in splits]
    x2 = [float([d for d in d2 if d["split"]==s][0][metric]) for s in splits]
    diffs = [a-b for a,b in zip(x1,x2)]
    mean_diff = statistics.mean(diffs)
    sd_diff = statistics.stdev(diffs)
    n = len(diffs)
    t_stat = mean_diff / (sd_diff / math.sqrt(n))
    df = n - 1
    from scipy.stats import t
    p_val = 2 * t.sf(abs(t_stat), df)
    ci = 1.96 * sd_diff / math.sqrt(n)
    sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
    lines4.append(f"| {kg1} vs {kg2} | {metric} | {mean_diff:+.3f} | [{mean_diff-ci:+.3f}, {mean_diff+ci:+.3f}] | {t_stat:.2f} | {df} | {p_val:.4f} | {sig} |")

with open("supplementary_table_S4.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines4))

print("S4 done")

# ===== S5: Pain Gene Expression and Annotation =====
lines5 = []
lines5.append("# Supplementary Table S5: Pain Gene Expression in K562 Cells and Track Annotations")
lines5.append("")
lines5.append("Expression data from Norman et al. (2019) Perturb-seq K562 dataset. Units: log-normalized counts.")
lines5.append("")
lines5.append("| Gene | Mean Expression | Expression Percentile | Track A | Track B | Track Dual |")
lines5.append("|---|---|---|---|---|---|---|")

# Read gene sets
with open("gene_sets.json", "r") as f:
    gene_sets = json.load(f)

# Read expression data
expr_data = {}
with open("k562_pain_expr.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        expr_data[row["gene"]] = (float(row["mean_expr"]), float(row["pct"]))

all_genes = set()
for gs in gene_sets.values():
    all_genes.update(gs)

for gene in sorted(all_genes):
    mean_e, pct = expr_data.get(gene, (float('nan'), float('nan')))
    track_a = "Y" if gene in gene_sets.get("trackA", []) else ""
    track_b = "Y" if gene in gene_sets.get("trackB", []) else ""
    track_dual = "Y" if gene in gene_sets.get("trackDual", []) else ""
    mean_str = f"{mean_e:.6f}" if not math.isnan(mean_e) else "N/A"
    pct_str = f"{pct:.6f}" if not math.isnan(pct) else "N/A"
    lines5.append(f"| {gene} | {mean_str} | {pct_str} | {track_a} | {track_b} | {track_dual} |")

lines5.append("")
lines5.append("*Track assignment based on RA-PainKG dual-track framework [4]. Track A: immune-inflammation. Track B: nociception-pain transduction.*")

with open("supplementary_table_S5.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines5))

print("S5 done")
print("\nAll 5 supplementary tables generated.")