# Extract all numerical claims from the paper for cross-referencing
filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Find all numbers in the paper with context
lines = content.split("\n")
print("="*70)
print("ALL NUMERICAL CLAIMS IN PAPER (for cross-verification)")
print("="*70)

numerical_patterns = [
    (r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:cells|genes|conditions|splits|edges|minutes|seconds|GB|RAM)', 'count/unit'),
    (r'Pearson r\s*=\s*(0\.\d+)', 'r value'),
    (r'delta\s*=\s*([+-]?\d+\.\d+)', 'delta'),
    (r'p\s*[=<]\s*(0\.\d+)', 'p value'),
    (r'CI[:\s]*\[([+-]?\d+\.\d+),\s*([+-]?\d+\.\d+)\]', 'CI'),
    (r'Kendall.*?W\s*=\s*(0\.\d+)', 'Kendall W'),
    (r'(mean|SD)\s*(?:=\s*)?(0\.\d+)', 'mean/SD'),
    (r'(\d+(?:\.\d+)?%)\s*(?:of|below|CI)', 'percentage'),
    (r'(alpha|k)\s*=\s*(\d+(?:\.\d+)?)', 'parameter'),
    (r'(\d+)\s*KG variants', 'KG count'),
    (r'(\d+)\s*PPI edges', 'edge count'),
    (r'(\d{1,3}(?:,\d{3})*)\s*(?:nodes|edges|genes)', 'entity count'),
]

for i, line in enumerate(lines):
    line_stripped = line.strip()
    if not line_stripped:
        continue
    # Find numbers
    nums = re.findall(r'\d+\.?\d*', line_stripped)
    if nums and len(nums) >= 2:
        # Check for key numerical claims
        for pattern, desc in numerical_patterns:
            matches = re.findall(pattern, line_stripped)
            if matches:
                print(f"  L{i+1}: {desc} -> {matches}")
                break

print("\n" + "="*70)
print("SPECIFIC CLAIMS TO VERIFY")
print("="*70)

# Manual verification list
claims = [
    ("91,205 K562 cells", "Norman 2019 paper"),
    ("5,045 genes", "from benchmark_metadata.json: n_genes=2000? Wait..." + " Actually metadata says 2000 used"),
    ("284 CRISPRi conditions", "Norman 2019"),
    ("10 KG variants", "Actual count: GO+RA-PainKG+5random+2ablation+Identity+STRING = 11"),
    ("673,899 edges", "Random graph edge count = GO edge count"),
    ("r = 0.667", "Random_R1 r_all mean"),
    ("r = 0.620", "Random_R1 r_pain mean"),
    ("r = 0.589", "GO r_all mean"),
    ("r = 0.542", "GO r_pain mean"),
    ("r = 0.503", "RA_PainKG r_pain mean"),
    ("delta = +0.077", "Random_R1 vs GO r_all diff"),
    ("delta = +0.117", "Random_R1 vs RA_PainKG r_pain diff"),
    ("delta = -0.039", "RA_PainKG vs GO"),
    ("CI [-0.085, +0.007]", "RA_PainKG vs GO CI"),
    ("CI [+0.059, +0.096]", "Random_R1 vs GO r_all CI"),
    ("CI [+0.083, +0.150]", "Random_R1 vs RA_PainKG r_pain CI"),
    ("p = 0.084", "RA_PainKG vs GO p value"),
    ("p = 0.41-0.83", "degPreserved p values"),
    ("p = 0.22", "GO vs GO_painCentric p"),
    ("SD = 0.010", "Random all-genes SD across realizations"),
    ("Kendall W = 0.64-0.65", "ranking consistency"),
    ("37.5%", "core pain genes absent from PPI"),
    ("50%", "nociception-specific genes isolated"),
    ("60,000 edges", "extrapolated target"),
    ("25-fold increase", "from 2,400 to 60,000"),
    ("~2,400 PPI edges", "RA-PainKG PPI edges"),
    ("~121,500 PPI edges", "GO-painCentric PPI edges"),
    ("68.3% of genes", "isolated in RA-PainKG"),
    ("38.6% below 0.01", "pain gene expression"),
    ("12 minutes", "compute time"),
    ("70%", "spectral decomposition time"),
    ("18,069 nodes", "RA-PainKG total nodes"),
    ("127,226 edges", "RA-PainKG total edges"),
    ("165 pain genes", "annotated genes"),
    ("Track A: 106 genes", ""),
    ("Track B: 122 genes", ""),
    ("96 spanning both", ""),
    ("10 entity types", ""),
    ("24 relation types", ""),
    ("192 core pain genes", "seed genes"),
    ("120 matched", "matched in PrimeKG"),
    ("45 additional", "from 2-hop expansion"),
    ("72 absent", "from PrimeKG"),
    ("d = -0.61", "effect size for power analysis"),
    ("55% power", ""),
    ("21 splits for 80%", ""),
]

for claim, note in claims:
    print(f"  [{claim}]  — {note}")
