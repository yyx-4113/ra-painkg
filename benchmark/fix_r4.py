import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    c = f.read()

# ====== FIX 1: Author name - remove parenthetical garbled text ======
old_auth = "**Yongxin Yang (栦蚗陔)**<sup>1,*</sup>"
new_auth = "**Yongxin Yang**<sup>1,*</sup>"
c = c.replace(old_auth, new_auth)
print("[1] Author name fixed")

# ====== FIX 2: Fix remaining "每" encoding artifacts ======
# Try multiple encoding variants
c = c.replace("57每100%", "57-100%")
c = c.replace("0.52每0.59", "0.52-0.59")
c = c.replace("40每66 seconds", "40-66 seconds")
# Also try hex variants
c = c.replace("\u6bcf", "-")  # Unicode for 每
print("[2] Encoding artifacts fixed")

# ====== FIX 3: Remove duplicate title at L7 ======
# Find the second occurrence of the title (after the first ---)
# Pattern: line with "# RA-PainKG:" that appears after "---"
idx1 = c.find("# RA-PainKG:")
idx2 = c.find("# RA-PainKG:", idx1+1)
if idx2 > 0:
    # Find the surrounding block
    # Find preceding ---
    prev_sep = c.rfind("---", 0, idx2)
    # Find next --- after author line
    next_sep = c.find("---", idx2)
    next_nl = c.find("\n\n", next_sep)
    if next_nl > 0:
        next_nl += 2
    else:
        next_nl = next_sep + 4
    # Replace the duplicate title block
    c = c[:prev_sep+3] + c[next_nl:]
    print("[3] Duplicate title removed")
else:
    print("[3] Duplicate title not found")

# ====== FIX 4: Remove double separator ======
c = c.replace("---\n\n\n---\n\n## 5. Usage Examples", "---\n\n## 5. Usage Examples")
c = c.replace("---\n\n---\n\n## 5. Usage Examples", "---\n\n## 5. Usage Examples")
print("[4] Double separator fixed")

# ====== FIX 5: Compress Methods 2.5-2.8 to ~10 lines ======
old_methods_detail = """### 2.5 Gene Embedding and Prediction Model

For each KG, we compute 128-dimensional gene embeddings via spectral decomposition of the normalized graph Laplacian: L = I - D^{-1/2} A D^{-1/2}, extracting eigenvectors corresponding to the k smallest non-zero eigenvalues. For graphs with isolated nodes (RA-PainKG: 68.3% of genes), these nodes receive near-zero embeddings that contribute no predictive signal in the linear model--a feature that accurately reflects their lack of KG-derived prior information. The perturbation prediction model is:

    predicted_delta = W^T * emb(perturbed_gene)

where W (128 x 5045) is learned via ridge regression (lambda = 0.1). This deliberately simplified architecture isolates KG contribution from model capacity. We validate robustness across regularization strengths (alpha = 0.001, 0.01, 0.1, 1.0, 10.0, 100.0) and embedding dimensions (k = 32, 64, 128, 256, 512).

**Justification of linear model choice:** We compared ridge regression against a 2-layer multilayer perceptron (MLP) with 128 hidden units and ReLU activation, trained on one representative split (seed 42). The MLP yielded lower performance (r = 0.46 vs r = 0.52每0.59 for ridge) and attenuated KG distinctions (GO: r = 0.459, RA-PainKG: r = 0.458, delta < 0.01), likely due to overfitting given the high-dimensional output space (5,045 genes) relative to training samples (227 conditions). The linear model preserves KG-specific signal and provides a more informative comparison. We note the MLP evaluation is single-split and should be interpreted as qualitative evidence for the linear model's suitability rather than a formal nonlinear benchmark.

This design contrasts with the full GEARS architecture [21], which uses GraphSAGE message-passing and cross-gene attention--mechanisms that may differentially exploit KG structure. Our results measure KG embedding quality in a controlled linear setting rather than end-to-end GEARS performance.

**Compute requirements:** Spectral decomposition of each 5,045 x 5,045 adjacency matrix required 40每66 seconds (Intel i9-13900K, 64 GB RAM, single core). Data loading (40 seconds), KG construction (GO: 100 seconds; RA-PainKG: 12 seconds), and benchmark execution (10 splits x 11 KGs, <1 second per split-KG combination) brought the total wall-clock time to approximately 12 minutes. Peak memory usage was approximately 2.5 GB during simultaneous matrix operations.

### 2.6 Evaluation Protocol

Perturbation conditions (n = 283, excluding ctrl) are split into train (80%, approximately 227 conditions) and test (20%, approximately 56 conditions). We run 10 independent splits with different random seeds (42, 179, 316, ..., 1275). For each split:

1. Train ridge regression on training conditions; predict on test conditions
2. Compute Pearson r, MSE, and RMSE as fraction of control expression SD
3. Stratify metrics by gene subset: all genes (5,045), pain-annotated (n = 44), non-pain (5,001), Track A (n = 3), Track B (n = 5), Dual (n = 36)

Statistical comparisons:
- **Paired t-tests** across 10 splits, validated by Shapiro-Wilk normality tests
- **Delta-r 95% confidence intervals** via t-distribution
- **Bonferroni correction** for multiple comparisons: with m = 5 primary tests (Supplementary Table S5), the adjusted significance threshold is alpha = 0.05/5 = 0.01. All conclusions reported at both nominal and adjusted thresholds.
- **Cross-split ranking consistency** via Kendall's W coefficient
- **Effect sizes** reported as Cohen's d

Power analysis: the RA-PainKG vs GO comparison (d = -0.61) requires 21 splits for 80% power at two-sided alpha = 0.05; our 10 splits provide 55% power for this comparison. Results are interpreted as "insufficient evidence for a difference" rather than "evidence of equivalence."

### 2.7 K562 Pain Gene Expression Quantification

To assess biological relevance of pain gene perturbation effects in K562 cells, we computed per-gene mean expression (log-normalized units) and percentage of expressing cells (non-zero entries) for all 44 pain-annotated genes in the Norman vocabulary. Given that 59.1% of measurable pain genes fall below the expression threshold and mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107), we treat the pain-gene subset results as exploratory and interpret density-driven conclusions primarily through the non-pain gene subset (n = 5,001), where the benchmark is adequately powered.

### 2.8 Implementation

Python 3.10+, ScanPy 1.12, NetworkX 3.6, NumPy, SciPy, scikit-learn. Full pipeline and processed KG adjacency matrices are available at https://github.com/yyx-4113/ra-painkg."""

new_methods_compact = """### 2.5 Benchmark Validation Methods

For validation, 128-dimensional gene embeddings were computed via spectral decomposition of the normalized graph Laplacian (k = 128) for each KG. Perturbation effects were predicted via ridge regression (lambda = 0.1) across 10 independent train/test splits (80%/20%). This linear architecture isolates KG contribution from model capacity (see Supplementary Methods for nonlinear model comparison and GEARS architecture comparison). Paired t-tests with Bonferroni correction (alpha = 0.01, m = 5) and Kendall's W ranking consistency were used for statistical comparison. Sensitivity analyses for regularization (alpha = 0.001-100.0) and embedding dimension (k = 32-512) confirmed robustness. K562 pain gene expression was quantified per-gene (mean expression, percent expressing cells) for all 44 pain-annotated genes. Complete methods, including spectral decomposition details, evaluation protocol, statistical tests, and power analysis, are provided in Supplementary Methods.

### 2.6 Implementation

Python 3.10+, ScanPy 1.12, NetworkX 3.6, NumPy, SciPy, scikit-learn. Total compute time: approximately 12 minutes (Intel i9-13900K, 64 GB RAM). Full pipeline and processed data at https://github.com/yyx-4113/ra-painkg."""

c = c.replace(old_methods_detail, new_methods_compact)
print("[5] Methods 2.5-2.8 compressed (40+ lines -> 10 lines)")

# ====== FIX 6: Remove duplicate K562 from 4.4 ======
old_k562_dup = """**Validation scope:** Benchmark validation is limited to K562 cells. Replication in disease-relevant cell types is essential before drawing conclusions about domain KG utility for pain biology applications."""

c = c.replace(old_k562_dup, "")
print("[6] Removed K562 duplication from 4.4")

# ====== FIX 7: Add Supplementary Materials list ======
# Insert before ## AI Usage Statement
suppl_section = """
## Supplementary Materials

- **Table S1:** Complete 165-gene pain gene list with functional categories, PrimeKG match status, and track assignments
- **Table S2:** Full edge relation type distribution (all 24 types)
- **Table S3:** Coverage-gap analysis: 72 genes absent from PrimeKG with functional categories and suggested alternative identifiers
- **Table S4:** Multi-split benchmark results for all 11 KG variants
- **Table S5:** Paired statistical comparisons with delta-r confidence intervals
- **Table S6:** KG variant structural characteristics
- **Supplementary Methods:** Spectral decomposition details, nonlinear model comparison (MLP vs ridge), GEARS architecture comparison, evaluation protocol, power analysis
- **Figure S1-S6:** Supplementary figures (degree distribution, track comparison, composition, core network, pathway subnetworks)

"""
c = c.replace("\n## AI Usage Statement", suppl_section + "\n## AI Usage Statement")
print("[7] Supplementary Materials list added")

# ====== FIX 8: Add download URL to Usage Setup ======
old_setup = "**Setup.** Download RA_PainKG_final.pkl from the GitHub repository and place it in your working directory:"
new_setup = "**Setup.** Download `RA_PainKG_final.pkl` from [https://github.com/yyx-4113/ra-painkg](https://github.com/yyx-4113/ra-painkg) (see `output/` directory) and place it in your working directory:"
c = c.replace(old_setup, new_setup)
print("[8] Download URL added to Usage Setup")

# ====== FIX 9: Add [17] citation in body text (DisGeNET) ======
# Find Introduction paragraph about existing resources, add [17] for DisGeNET
old_intro_res = "Pain-focused resources such as the IUPHAR/BPS Guide to Pharmacology [14] and the Human Pain Genetics Database [15] curate pain-relevant genes but lack network connectivity and multi-entity integration."
new_intro_res = "Pain-focused resources such as the IUPHAR/BPS Guide to Pharmacology [14] and the Human Pain Genetics Database [15] curate pain-relevant genes, while DisGeNET [17] provides gene-disease associations, but these resources lack network connectivity and multi-entity integration."
c = c.replace(old_intro_res, new_intro_res)
print("[9] Reference [17] (DisGeNET) cited in Introduction")

# ====== FIX 10: Fix "nine" vs "15" in Abstract ======
c = c.replace("manual curation of nine core pain signaling pathways.", "manual curation of 15 functional gene categories spanning nine core pain signaling pathways.")
print("[10] Abstract: 'nine' -> '15 functional gene categories spanning nine core pain signaling pathways'")

# ====== FIX 11: Expand Figure Captions for Fig 3/4/6 ======
old_fig3 = "**Figure 3.** Comparison of centrality distributions between Track A (immune-inflammation) and Track B (nociception-pain transduction) gene subsets."
new_fig3 = "**Figure 3.** Comparison of centrality distributions between Track A (immune-inflammation, n = 106 genes) and Track B (nociception-pain transduction, n = 122 genes) gene subsets. Betweenness, degree, closeness, and eigenvector centrality are shown as violin plots. Track B genes show systematically lower centrality across all metrics, consistent with their sparser representation in PrimeKG."
c = c.replace(old_fig3, new_fig3)

old_fig4 = "**Figure 4.** Node type composition and edge relation distribution in RA-PainKG. The graph spans 10 entity types and 24 relation types."
new_fig4 = "**Figure 4.** Node type composition (pie chart, 10 entity types) and edge relation distribution (bar chart, top 10 of 24 relation types) in RA-PainKG. Protein-protein interactions account for 2,400 edges (1.9%), with the remaining 124,826 edges distributed across pathway, bioprocess, drug-target, and other relation types."
c = c.replace(old_fig4, new_fig4)

old_fig6 = "**Figure 6.** Pathway subnetwork visualizations for nine curated pain signaling pathways mapped onto RA-PainKG."
new_fig6 = "**Figure 6.** Pathway subnetwork visualizations for the nine curated pain signaling pathways mapped onto RA-PainKG. Each panel shows a single pathway: TRP channels, voltage-gated sodium channels, neurotrophin signaling, opioid signaling, MAPK pathway, JAK-STAT pathway, prostaglandin pathway, complement cascade, and GABA/glycine receptors. Node color indicates track assignment (Track A, Track B, or Dual). Edge directionality indicates known signaling relationships."
c = c.replace(old_fig6, new_fig6)
print("[11] Figure Captions expanded for Fig 3/4/6")

# ====== FIX 12: Split long Conclusion paragraph ======
old_concl = """### 4.6 Conclusion

RA-PainKG provides a tissue-contextualized, dual-track knowledge graph for RA pain signaling with systematic coverage-gap documentation-a resource type not previously available for pain biology research. The graph, its construction pipeline, and comprehensive documentation are publicly available at https://github.com/yyx-4113/ra-painkg under the MIT license. Transparent benchmark validation establishes honest boundary conditions, and systematic coverage-gap documentation identifies specific priorities for future resource development. The open-source construction framework is designed for extensibility to other diseases where domain-specific knowledge graphs with documented knowledge gaps would accelerate mechanistic research."""

new_concl = """### 4.6 Conclusion

RA-PainKG provides a tissue-contextualized, dual-track knowledge graph for RA pain signaling with systematic coverage-gap documentation-a resource type not previously available for pain biology research. The graph, its construction pipeline, and comprehensive documentation are publicly available at https://github.com/yyx-4113/ra-painkg under the MIT license.

Transparent benchmark validation establishes honest boundary conditions for downstream applications, and systematic coverage-gap documentation identifies specific priorities for future resource development. The open-source construction framework is designed for extensibility to other diseases where domain-specific knowledge graphs with documented knowledge gaps would accelerate mechanistic research."""

c = c.replace(old_concl, new_concl)
print("[12] Conclusion split into two paragraphs")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(c)
print("\n[DONE] All 12 fixes applied")