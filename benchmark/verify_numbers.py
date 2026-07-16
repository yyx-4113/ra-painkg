import csv, json, statistics, math
from collections import defaultdict
import sys, os

os.chdir(r"D:\麻醉科共病\ra-painkg\benchmark\results")

rows = []
with open("benchmark_jbi_extended.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

kg_data = defaultdict(list)
for r in rows:
    kg_data[r["kg"]].append({
        "split": int(r["split"]), "seed": int(r["seed"]),
        "r_all": float(r["r_all"]), "r_pain": float(r["r_pain"]),
        "r_nonpain": float(r["r_nonpain"]),
        "r_trackA": float(r["r_trackA"]), "r_trackB": float(r["r_trackB"]),
        "r_trackDual": float(r["r_trackDual"]),
        "mse_all": float(r["mse_all"]), "mse_pain": float(r["mse_pain"])
    })

print("="*80)
print("1. PER-KG MEAN PERFORMANCE (10 splits)")
print("="*80)
for kg in sorted(kg_data.keys()):
    data = kg_data[kg]
    n = len(data)
    r_all_mean = statistics.mean([d["r_all"] for d in data])
    r_all_sd = statistics.stdev([d["r_all"] for d in data]) if n > 1 else 0
    r_pain_mean = statistics.mean([d["r_pain"] for d in data])
    r_pain_sd = statistics.stdev([d["r_pain"] for d in data]) if n > 1 else 0
    print(f"{kg:30s} | all r={r_all_mean:.3f}+-{r_all_sd:.3f} | pain r={r_pain_mean:.3f}+-{r_pain_sd:.3f} | n={n}")

from scipy import stats as scistats

def paired_compare(kg1, kg2, metric="r_all"):
    d1 = kg_data[kg1]
    d2 = kg_data[kg2]
    d1_by_split = {d["split"]: d[metric] for d in d1}
    d2_by_split = {d["split"]: d[metric] for d in d2}
    common_splits = sorted(set(d1_by_split.keys()) & set(d2_by_split.keys()))
    if len(common_splits) < 2:
        return None
    x1 = [d1_by_split[s] for s in common_splits]
    x2 = [d2_by_split[s] for s in common_splits]
    diffs = [a-b for a,b in zip(x1,x2)]
    mean_diff = statistics.mean(diffs)
    sd_diff = statistics.stdev(diffs) if len(diffs) > 1 else 0
    n = len(diffs)
    t_stat = mean_diff / (sd_diff / math.sqrt(n)) if sd_diff > 0 else float("inf")
    df = n - 1
    from scipy.stats import t
    p_val = 2 * t.sf(abs(t_stat), df) if sd_diff > 0 else 0.0
    ci_95 = 1.96 * sd_diff / math.sqrt(n)
    return mean_diff, ci_95, p_val, n

random_kgs = [k for k in kg_data if k.startswith("Random_R") and k not in ["Random_Original"] and len(kg_data[k]) == 10]
random_means = {}
for k in random_kgs:
    data = kg_data[k]
    random_means[k] = statistics.mean([d["r_all"] for d in data])
best_random = max(random_means, key=random_means.get)
print(f"\nBest random KG: {best_random} with all r={random_means[best_random]:.3f}")

print("\n" + "="*80)
print("2. KEY PAIRED COMPARISONS")
print("="*80)
comparisons = [
    (best_random, "GO", "r_all"),
    (best_random, "GO", "r_pain"),
    (best_random, "RA_PainKG", "r_all"),
    (best_random, "RA_PainKG", "r_pain"),
    ("GO", "RA_PainKG", "r_all"),
    ("GO", "RA_PainKG", "r_pain"),
    ("RA_PainKG", "RA_PainKG_degPreserved", "r_all"),
    ("RA_PainKG", "RA_PainKG_degPreserved", "r_pain"),
    ("GO", "GO_painCentric", "r_all"),
    ("GO", "GO_painCentric", "r_pain"),
]

for kg1, kg2, metric in comparisons:
    result = paired_compare(kg1, kg2, metric)
    if result:
        mean_diff, ci_95, p_val, n = result
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
        print(f"{kg1} vs {kg2} [{metric:7s}]: delta={mean_diff:+.3f} CI=[{mean_diff-ci_95:+.3f}, {mean_diff+ci_95:+.3f}] p={p_val:.4f} {sig}")

print("\n" + "="*80)
print("3. RANDOM GRAPH SUMMARY")
print("="*80)
random_all_means = []
random_pain_means = []
for k in random_kgs:
    data = kg_data[k]
    m_all = statistics.mean([d["r_all"] for d in data])
    m_pain = statistics.mean([d["r_pain"] for d in data])
    random_all_means.append(m_all)
    random_pain_means.append(m_pain)
    print(f"{k}: all={m_all:.4f}, pain={m_pain:.4f}")
print(f"\nRandom mean all: {statistics.mean(random_all_means):.4f} SD: {statistics.stdev(random_all_means):.4f}")
print(f"Random mean pain: {statistics.mean(random_pain_means):.4f} SD: {statistics.stdev(random_pain_means):.4f}")

print("\n" + "="*80)
print("4. RANKING CONSISTENCY")
print("="*80)
ranking_kgs = ["GO", "RA_PainKG", "GO_painCentric"] + random_kgs
for metric in ["r_all", "r_pain"]:
    rank_matrix = []
    for split in range(10):
        split_scores = {}
        for kg in ranking_kgs:
            data = [d for d in kg_data[kg] if d["split"] == split]
            if data:
                split_scores[kg] = data[0][metric]
        sorted_kgs = sorted(split_scores.items(), key=lambda x: x[1], reverse=True)
        ranks = {}
        for rank, (kg, _) in enumerate(sorted_kgs, 1):
            ranks[kg] = rank
        rank_matrix.append([ranks.get(kg, 99) for kg in ranking_kgs])
    
    n, m = len(rank_matrix), len(ranking_kgs)
    Ri = [sum(rank_matrix[i][j] for i in range(n)) for j in range(m)]
    Rbar = statistics.mean(Ri)
    S = sum((r - Rbar)**2 for r in Ri)
    W = 12 * S / (n**2 * (m**3 - m)) if m > 1 and n > 0 else 0
    print(f"{metric}: Kendall W = {W:.4f}")

print("\n" + "="*80)
print("5. GO-PAINCENTRIC vs GO (Ablation)")
print("="*80)
r = paired_compare("GO", "GO_painCentric", "r_all")
print(f"GO vs GO_painCentric [all]: delta={r[0]:+.3f} CI=[{r[0]-r[1]:+.3f}, {r[0]+r[1]:+.3f}] p={r[2]:.4f}")
r = paired_compare("GO", "GO_painCentric", "r_pain")
print(f"GO vs GO_painCentric [pain]: delta={r[0]:+.3f} CI=[{r[0]-r[1]:+.3f}, {r[0]+r[1]:+.3f}] p={r[2]:.4f}")

print("\nDone.")