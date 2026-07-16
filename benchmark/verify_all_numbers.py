import csv, json, statistics, math
from collections import defaultdict

os.chdir(r"D:\麻醉科共病\ra-painkg\benchmark\results")

# Full verification of ALL numbers
print("="*70)
print("COMPREHENSIVE DATA VERIFICATION FOR FINAL REVIEW")
print("="*70)

rows = []
with open("benchmark_jbi_extended.csv", "r") as f:
    for row in csv.DictReader(f):
        rows.append(row)

kg_data = defaultdict(list)
for r in rows:
    kg_data[r["kg"]].append(r)

# 1. Per-KG per-split detail
print("\n--- 1. ALL MEANS (10 splits each) ---")
kg_order = ["GO", "RA_PainKG", "RA_PainKG_degPreserved", "GO_painCentric",
            "Random_R0", "Random_R1", "Random_R2", "Random_R3", "Random_R4",
            "STRING", "Identity", "Random_Original"]
metrics = ["r_all", "r_pain", "r_nonpain", "r_trackA", "r_trackB", "r_trackDual"]

for kg in kg_order:
    if kg not in kg_data:
        continue
    data = kg_data[kg]
    n = len(data)
    for m in metrics:
        vals = [float(d[m]) for d in data]
        m_mean = statistics.mean(vals)
        m_sd = statistics.stdev(vals) if n > 1 else 0
        print(f"  {kg:30s} | {m:12s} | mean={m_mean:.4f} | sd={m_sd:.4f} | n={n}")

# 2. Random graph summary
print("\n--- 2. RANDOM GRAPH SUMMARY (5 realizations) ---")
random_kgs = ["Random_R0", "Random_R1", "Random_R2", "Random_R3", "Random_R4"]
for m in ["r_all", "r_pain"]:
    means = []
    for kg in random_kgs:
        means.append(statistics.mean([float(d[m]) for d in kg_data[kg]]))
    print(f"  {m}: mean of means={statistics.mean(means):.4f}, sd of means={statistics.stdev(means):.4f}")
    print(f"  {m}: range=[{min(means):.4f}, {max(means):.4f}]")

# 3. ALL paired comparisons with full stats
print("\n--- 3. ALL PAIRED COMPARISONS ---")
from scipy import stats as scistats

comparisons = [
    ("Random_R1", "GO", "r_all"), ("Random_R1", "GO", "r_pain"),
    ("Random_R1", "RA_PainKG", "r_all"), ("Random_R1", "RA_PainKG", "r_pain"),
    ("GO", "RA_PainKG", "r_all"), ("GO", "RA_PainKG", "r_pain"),
    ("RA_PainKG", "RA_PainKG_degPreserved", "r_all"),
    ("RA_PainKG", "RA_PainKG_degPreserved", "r_pain"),
    ("GO", "GO_painCentric", "r_all"), ("GO", "GO_painCentric", "r_pain"),
    ("Random_R1", "GO_painCentric", "r_all"), ("Random_R1", "GO_painCentric", "r_pain"),
    ("Random_R1", "RA_PainKG_degPreserved", "r_all"),
    ("Random_R1", "RA_PainKG_degPreserved", "r_pain"),
    ("GO", "RA_PainKG_degPreserved", "r_all"), ("GO", "RA_PainKG_degPreserved", "r_pain"),
]

for kg1, kg2, metric in comparisons:
    d1, d2 = kg_data[kg1], kg_data[kg2]
    splits = sorted(set(d["split"] for d in d1) & set(d["split"] for d in d2))
    x1 = [float([d for d in d1 if d["split"]==s][0][metric]) for s in splits]
    x2 = [float([d for d in d2 if d["split"]==s][0][metric]) for s in splits]
    diffs = [a-b for a,b in zip(x1,x2)]
    m = statistics.mean(diffs)
    s = statistics.stdev(diffs)
    n = len(diffs)
    t_stat = m/(s/math.sqrt(n))
    df = n-1
    p = 2*scistats.t.sf(abs(t_stat), df)
    ci = 1.96*s/math.sqrt(n)
    sig = "***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "ns"
    print(f"  {kg1} vs {kg2} [{metric}]: diff={m:+.4f} CI=[{m-ci:+.4f},{m+ci:+.4f}] t={t_stat:.2f} p={p:.4f} {sig}")

# 4. Kendall W
print("\n--- 4. KENDALL W ---")
ranking_kgs = ["GO", "RA_PainKG", "GO_painCentric", "Random_R0", "Random_R1", "Random_R2", "Random_R3", "Random_R4"]
for metric in ["r_all", "r_pain"]:
    rank_matrix = []
    for split in range(10):
        scores = {}
        for kg in ranking_kgs:
            d = [d for d in kg_data[kg] if d["split"]==str(split)]
            if d: scores[kg] = float(d[0][metric])
        sorted_kgs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ranks = {kg: rank+1 for rank, (kg, _) in enumerate(sorted_kgs)}
        rank_matrix.append([ranks.get(kg, 99) for kg in ranking_kgs])
    n, m = len(rank_matrix), len(ranking_kgs)
    Ri = [sum(rank_matrix[i][j] for i in range(n)) for j in range(m)]
    Rbar = statistics.mean(Ri)
    S = sum((r-Rbar)**2 for r in Ri)
    W = 12*S/(n**2*(m**3-m))
    print(f"  {metric}: Kendall W = {W:.4f}")
    # First place counts
    first = defaultdict(int)
    for row in rank_matrix:
        min_rank = min(row)
        for j, r in enumerate(row):
            if r == min_rank:
                first[ranking_kgs[j]] += 1
    print(f"    First-place counts: {dict(first)}")

# 5. DEG-PRESERVED detailed
print("\n--- 5. DEG-PRESERVED ABLATION ---")
for kg in ["RA_PainKG", "RA_PainKG_degPreserved"]:
    data = kg_data[kg]
    for m in ["r_all", "r_pain"]:
        vals = [float(d[m]) for d in data]
        print(f"  {kg} {m}: {statistics.mean(vals):.4f} +/- {statistics.stdev(vals):.4f}")

# 6. GO vs GO-painCentric detailed
print("\n--- 6. GO vs GO-PAINCENTRIC ---")
for kg in ["GO", "GO_painCentric"]:
    data = kg_data[kg]
    for m in ["r_all", "r_pain"]:
        vals = [float(d[m]) for d in data]
        print(f"  {kg} {m}: {statistics.mean(vals):.4f} +/- {statistics.stdev(vals):.4f}")

# 7. Check for the single-split seed=42 data points
print("\n--- 7. SINGLE SPLIT (seed=42, split=0) ---")
for kg in kg_order:
    if kg not in kg_data:
        continue
    d = [d for d in kg_data[kg] if d["split"]=="0" and d["seed"]=="42"]
    if d:
        d = d[0]
        print(f"  {kg:30s} | r_all={float(d['r_all']):.4f} | r_pain={float(d['r_pain']):.4f}")

# 8. STRING p-value check
print("\n--- 8. STRING & IDENTITY CONSISTENCY ---")
for kg in ["STRING", "Identity"]:
    data = kg_data[kg]
    for m in ["r_all", "r_pain"]:
        vals = [float(d[m]) for d in data]
        # All should be 0.0
        unique = set(vals)
        print(f"  {kg} {m}: values={unique} (n={len(vals)})")

print("\nDone.")