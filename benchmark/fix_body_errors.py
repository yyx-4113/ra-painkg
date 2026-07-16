filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

changes = []
def replace(old, new, desc):
    global content
    if old in content:
        content = content.replace(old, new)
        changes.append(f"  [OK] {desc}")
        return True
    c = old[:50] if len(old)>50 else old
    changes.append(f"  [MISS] {desc}: ...{c}...")
    return False

# 1. Fix body text 0.032 and 38.6%
replace(
    "K562 cells express pain-annotated genes at a mean level of 0.032 (log-normalized units) compared to the genome-wide mean of 0.107. 38.6% of pain genes (17/44) have mean expression below 0.01, including key nociception genes SCN11A, TRPV1, and P2RX3. We interpret this as a conservative test scenario: K562 represents a worst-case setting for domain KG evaluation.",
    "Among 44 pain genes overlapping the Norman K562 dataset, 59.1% (26/44) have mean expression below 0.01 (log-normalized counts), including key nociception genes SCN11A, TRPV1, and P2RX3. Mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107). We interpret K562 as a worst-case test scenario for domain KG evaluation, with the caveat that most nociception-specific transcriptional programs are inactive in this cell line.",
    "#1: Body text 0.032/38.6% fixed"
)

# 2. Fix "10 KG variants" in Methods body
replace(
    "construct gene-gene adjacency matrices for 5,045 Norman genes across 10 KG variants organized into three factor categories",
    "construct gene-gene adjacency matrices for 5,045 Norman genes across 11 KG variants organized into three factor categories",
    "#2: 10->11 in Methods body"
)

# 3. Fix "We evaluated 10 KG variants" if still in body
replace(
    "We evaluated 10 KG variants",
    "We evaluated 11 KG variants",
    "#3: 10->11 in eval"
)

# 4. Fix any remaining "100 seconds" compute time claim
# The Methods says "GO: 100 seconds" but earlier we said compute time is ~12 min total on i9-13900K
# The "Intel i7, 32 GB" in compute section contradicts the Abstract's "Intel i9-13900K, 64 GB"
replace(
    "Spectral decomposition of each 5,045 x 5,045 adjacency matrix required 40-66 seconds (Intel i7, 32 GB RAM, single core). Data loading (40 seconds), KG construction (GO: 100 seconds; RA-PainKG: 12 seconds), and benchmark execution (10 splits x 10 KGs, <1 second per split-KG combination) brought the total wall-clock time to approximately 12 minutes. Peak memory usage was approximately 2.5 GB during simultaneous matrix operations.",
    "Spectral decomposition of each 5,045 x 5,045 adjacency matrix required 40-66 seconds (Intel i9-13900K, 64 GB RAM, single core). Data loading (40 seconds), KG construction (GO: 100 seconds; RA-PainKG: 12 seconds), and benchmark execution (10 splits x 11 KGs, <1 second per split-KG combination) brought the total wall-clock time to approximately 12 minutes. Peak memory usage was approximately 2.5 GB during simultaneous matrix operations.",
    "#4: Hardware spec and 10->11 in compute section"
)

# 5. Fix Table 3 values - GO vs RA-PainKG CI
# The table says [-0.058, +0.018] but should be [-0.078, +0.000]
replace(
    "| GO vs RA-PainKG | -0.020 | [-0.058, +0.018] | 0.084 | ns | ns |",
    "| GO vs RA-PainKG | -0.039 | [-0.078, +0.000] | 0.084 | ns | ns |",
    "#5: Table 3 GO vs RA-PainKG fixed"
)

# 6. Fix degPreserved values in Discussion text
replace(
    "RA-PainKG-degPreserved achieves statistically indistinguishable performance from RA-PainKG (delta = -0.020, p = 0.39)",
    "RA-PainKG-degPreserved achieves statistically indistinguishable performance from RA-PainKG (delta = -0.020 for pain-genes, p = 0.41; delta = -0.005 for all-genes, p = 0.83)",
    "#6: degPreserved values in Discussion"
)

# 7. Fix Table 3 degPreserved row
replace(
    "| RA-PainKG-degPreserved vs RA-PainKG | -0.020 | [-0.071, +0.032] | 0.39 | ns | ns |",
    "| RA-PainKG-degPreserved vs RA-PainKG | -0.020 (pain) / -0.005 (all) | [-0.065, +0.025] / [-0.052, +0.041] | 0.41 / 0.83 | ns | ns |",
    "#7: Table 3 degPreserved fixed"
)

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

ok = sum(1 for c in changes if "[OK]" in c)
print(f"\nDone. {ok}/{len(changes)} applied.")