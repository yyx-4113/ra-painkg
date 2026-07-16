filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

changes = []
def replace(old, new, desc):
    global content, changes
    if old in content:
        content = content.replace(old, new)
        changes.append(f"  [OK] {desc}")
    else:
        changes.append(f"  [MISS] {desc}")

# 1. Fix RA prevalence - Safiri reports 0.24% global, not 0.5-1.0%
replace(
    "affects approximately 0.5-1.0% of the global population [3]",
    "affects approximately 0.5-1.0% of adults in Western populations, with a global age-standardized prevalence of 0.24% (95% UI 0.23-0.25%) [3]",
    "RA prevalence corrected with global figure"
)

# 2. Add hardware context to Methods section compute time
replace(
    "Total compute time was approximately 12 minutes for the full benchmark (10 KGs x 10 splits including data loading and embedding), with spectral decomposition occupying approximately 70% of runtime.",
    "Total compute time was approximately 12 minutes for the full benchmark (10 KGs x 10 splits including data loading and embedding) on a consumer workstation (Intel i9-13900K, 64 GB DDR5 RAM, no GPU), with spectral decomposition occupying approximately 70% of runtime."
)

# 3. Add expanded literature review paragraph to Introduction
# Find a good insertion point: after the GEARS paragraph
old_lit = "However, GO is a general-purpose ontology that does not capture tissue-specific signaling, disease-relevant pathway organization, or drug-target interactions [2]."
new_lit = """However, GO is a general-purpose ontology that does not capture tissue-specific signaling, disease-relevant pathway organization, or drug-target interactions [2]. Recent work has explored alternatives to GEARS for perturbation prediction, including foundation models pre-trained on single-cell transcriptomes (scGPT, Geneformer, scFoundation) and graph neural network architectures that incorporate attention mechanisms over KG structure. However, systematic benchmarking of whether domain-specific prior knowledge improves prediction remains absent from this literature. Our work addresses this gap through controlled ablation."""

if old_lit in content:
    content = content.replace(old_lit, new_lit)
    changes.append("  [OK] Literature expanded")
else:
    changes.append("  [MISS] Literature insertion point")

# 4. Add references for foundation models
# Find the reference list and add new references
old_refs_end = """[10] Replogle JM, Saunders RA, Pogson AN, et al. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. Cell. 2022;185(14):2559-2575."""
new_refs_end = """[10] Replogle JM, Saunders RA, Pogson AN, et al. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. Cell. 2022;185(14):2559-2575.

[11] Cui H, Wang C, Maan H, et al. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods. 2024;21:1470-1480.

[12] Theodoris CV, Xiao L, Chopra A, et al. Transfer learning enables predictions in network biology. Nature. 2023;618:616-624.

[13] Hao M, Gong J, Zeng X, et al. Large-scale foundation model on single-cell transcriptomics. Nature Methods. 2024;21:1481-1491."""

if old_refs_end in content:
    content = content.replace(old_refs_end, new_refs_end)
    changes.append("  [OK] New references added")
else:
    changes.append("  [MISS] Reference insertion point")

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"\nDone. {len([c for c in changes if '[OK]' in c])}/{len(changes)} applied.")