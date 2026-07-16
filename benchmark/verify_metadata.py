import json

# Check metadata for gene count discrepancy
with open(r"D:\麻醉科共病\ra-painkg\benchmark\results\benchmark_metadata.json", "r") as f:
    meta = json.load(f)

print("Benchmark metadata:")
for k, v in meta.items():
    if "gene" in k.lower() or "vocab" in k.lower() or "cell" in k.lower() or "perturb" in k.lower():
        print(f"  {k}: {v}")

# Check gene_vocab size
import csv
with open(r"D:\麻醉科共病\ra-painkg\benchmark\results\gene_vocab.csv", "r") as f:
    reader = csv.reader(f)
    rows = list(reader)
print(f"\ngene_vocab.csv: {len(rows)} genes")

# Check gene_sets  
with open(r"D:\麻醉科共病\ra-painkg\benchmark\results\gene_sets.json", "r") as f:
    gs = json.load(f)
print(f"\ngene_sets.json keys: {list(gs.keys())}")
for k, v in gs.items():
    if isinstance(v, list):
        print(f"  {k}: {len(v)} genes")

# Check k562 expression data
with open(r"D:\麻醉科共病\ra-painkg\benchmark\results\k562_pain_expr.csv", "r") as f:
    reader = csv.DictReader(f)
    expr_rows = list(reader)
print(f"\nk562_pain_expr.csv: {len(expr_rows)} genes")
pcts = [float(r["pct"]) for r in expr_rows]
means = [float(r["mean_expr"]) for r in expr_rows]
below_001 = sum(1 for m in means if m < 0.01)
print(f"  Range: mean_expr [{min(means):.6f}, {max(means):.6f}]")
print(f"  Below 0.01: {below_001}/{len(means)} = {below_001/len(means)*100:.1f}%")

# Check benchmark_jbi_extended for n_genes info
with open(r"D:\麻醉科共病\ra-painkg\benchmark\results\benchmark_jbi_extended.csv", "r") as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
print(f"\nbenchmark_jbi_extended.csv columns: {header}")