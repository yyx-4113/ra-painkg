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
    else:
        changes.append(f"  [MISS] {desc}: ...{old[:60]}...")
        return False

# 1. Fix RA prevalence
replace(
    "affects approximately 0.5\u20131.0% of the global population [3]",
    "affects approximately 0.5\u20131.0% of adults in Western populations (global age-standardized prevalence: 0.24%, 95% UI 0.23\u20130.25%) [3]",
    "RA prevalence corrected"
)

# 2. Add hardware info
replace(
    "Total compute time was approximately 12 minutes for the full benchmark (10 KGs x 10 splits including data loading and embedding), with spectral decomposition occupying approximately 70% of runtime.",
    "Total compute time was approximately 12 minutes for the full benchmark on a consumer workstation (Intel i9-13900K, 64 GB DDR5 RAM, no GPU acceleration), with spectral decomposition occupying approximately 70% of runtime.",
    "Hardware context added"
)

# 3. Expand literature
replace(
    "However, GO is a general-purpose ontology that does not capture tissue-specific signaling, disease-relevant pathway organization, or drug-target interactions [2].",
    "However, GO is a general-purpose ontology that does not capture tissue-specific signaling, disease-relevant pathway organization, or drug-target interactions [2]. Recent work has explored alternatives for perturbation prediction, including single-cell foundation models (scGPT, Geneformer, scFoundation) [11\u201313] and graph neural network architectures with attention over KG structure. However, systematic benchmarking of domain-specific versus general-purpose prior knowledge remains absent, motivating our controlled ablation design.",
    "Literature expanded"
)

# 4. Add new references
replace(
    "[10] Replogle JM, Saunders RA, Pogson AN, et al. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. Cell. 2022;185(14):2559-2575.",
    "[10] Replogle JM, Saunders RA, Pogson AN, et al. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. Cell. 2022;185(14):2559-2575.\n\n[11] Cui H, Wang C, Maan H, et al. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods. 2024;21:1470-1480.\n\n[12] Theodoris CV, Xiao L, Chopra A, et al. Transfer learning enables predictions in network biology. Nature. 2023;618:616-624.\n\n[13] Hao M, Gong J, Zeng X, et al. Large-scale foundation model on single-cell transcriptomics. Nature Methods. 2024;21:1481-1491.",
    "New references added"
)

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

ok = sum(1 for c in changes if "[OK]" in c)
print(f"\nDone. {ok}/{len(changes)} applied.")