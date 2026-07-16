import csv, statistics, json

os.chdir(r"D:\麻醉科共病\ra-painkg\benchmark\results")

# CRITICAL CHECK 1: Pain gene expression - exact numbers
with open("k562_pain_expr.csv", "r") as f:
    reader = csv.DictReader(f)
    expr_rows = list(reader)

means = [float(r["mean_expr"]) for r in expr_rows]
pcts = [float(r["pct"]) for r in expr_rows]

below_001 = sum(1 for m in means if m < 0.01)
mean_pain = statistics.mean(means)
print(f"CRITICAL 1: Pain gene expression stats:")
print(f"  Number of pain genes: {len(expr_rows)}")
print(f"  Mean expression: {mean_pain:.4f}")
print(f"  Below 0.01: {below_001}/{len(means)} = {below_001/len(means)*100:.1f}%")
print(f"  Paper claims: 38.6% below 0.01  —  ACTUAL: {below_001/len(means)*100:.1f}%")
print(f"  DISCREPANCY: {abs(below_001/len(means)*100 - 38.6):.1f} percentage points!")

# CRITICAL CHECK 2: What's the genome-wide mean?
# The paper says "vs genome-wide mean 0.107"
# We need to verify this from the data if available
print(f"\nCRITICAL 2: Mean expression values:")
for i, r in enumerate(expr_rows[:5]):
    print(f"  {r['gene']}: mean_expr={float(r['mean_expr']):.6f}, pct={float(r['pct']):.6f}")
print(f"  ...")

# CRITICAL CHECK 3: Check gene_sets sizes
with open("gene_sets.json", "r") as f:
    gs = json.load(f)
print(f"\nCRITICAL 3: Gene set sizes:")
print(f"  norman_all: {len(gs['norman_all'])} genes (total in benchmark)")
print(f"  pain_all: {len(gs['pain_all'])} genes (pain genes in benchmark)")
print(f"  non_pain: {len(gs['non_pain'])} genes")
print(f"  track_a_only: {len(gs.get('track_a_only', []))} genes")
print(f"  track_b_only: {len(gs.get('track_b_only', []))} genes")
print(f"  track_dual: {len(gs.get('track_dual', []))} genes")
print(f"  Paper says 5,045 total genes, but gene_sets says {len(gs['norman_all'])}")
print(f"  Paper says 165 pain genes, but only {len(gs['pain_all'])} in benchmark")

# CRITICAL CHECK 4: Verify benchmark was on 5045 or 2000 genes
with open("benchmark_metadata.json", "r") as f:
    meta = json.load(f)
print(f"\nCRITICAL 4: Benchmark metadata:")
print(f"  n_genes: {meta['n_genes']}")
print(f"  n_cells: {meta['n_cells']}")
print(f"  n_perturbations: {meta['n_perturbations']}")
print(f"  n_pain_genes: {meta['n_pain_genes']}")
print(f"  Paper says: 5,045 genes, 91,205 cells, 284 conditions")
print(f"  Metadata says: {meta['n_genes']} genes, {meta['n_cells']} cells, {meta['n_perturbations']} conditions")

# CRITICAL CHECK 5: Track A and B gene counts
# metadata gene_vocabulary = 165 pain genes
print(f"\nCRITICAL 5: Track gene counts:")
print(f"  gene_vocabulary (metadata): {len(meta['gene_vocabulary'])} genes")
print(f"  Paper says: 165 pain genes annotated, Track A: 106, Track B: 122, Dual: 96")

# The genes in track sets
print(f"\n  track_a_only: {gs.get('track_a_only', [])} ({len(gs.get('track_a_only', []))})")
print(f"  track_b_only: {gs.get('track_b_only', [])} ({len(gs.get('track_b_only', []))})")
print(f"  track_dual: first 10: {gs.get('track_dual', [])[:10]} ({len(gs.get('track_dual', []))})")
