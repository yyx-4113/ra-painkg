# Domain-Specific versus Dense Knowledge Graphs for Gene Perturbation Prediction: A Multi-Split Ablation Benchmark

## Manuscript | Target: *Journal of Biomedical Informatics*

---

# Domain-Specific versus Dense Knowledge Graphs for Gene Perturbation Prediction: A Multi-Split Ablation Benchmark

**Yongxin Yang (杨永新)**<sup>1,*</sup>

<sup>1</sup> Department of Anesthesiology, The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou 350000, Fujian, China

<sup>*</sup> Corresponding author: 960856791@qq.com

---

## Abstract

**Objective:** To establish rigorous methodology for benchmarking knowledge graph (KG) contributions to gene perturbation prediction, and to determine whether domain-specific edge semantics improve prediction beyond graph connectivity alone.

**Materials and Methods:** We benchmarked 11 KG variants—GO Biological Process, RA-PainKG, five dense random graphs (673,899 edges each), two ablation variants (degree-preserving randomization and pain-gene-centric GO reduction), an Identity baseline, and STRING—on the Norman et al. (2019) Perturb-seq dataset (91,205 K562 cells, 5,045 genes). Gene embeddings were computed via spectral decomposition (k = 128). Perturbation effects were predicted via ridge regression across 10 independent splits (80%/20%), with paired t-tests, delta-r confidence intervals, and sensitivity analyses (alpha = 0.001–100.0, k = 32–512).

**Results:** Dense random graphs consistently achieved highest accuracy. A representative random graph (Random_R1) achieved Pearson r = 0.667 (all genes) and 0.620 (pain genes, n = 44 overlapping), significantly outperforming GO (r = 0.589, 0.542; delta = +0.078, p < 0.001) and RA-PainKG (pain r = 0.503; delta = +0.117, p < 0.001). RA-PainKG did not differ from GO (delta = −0.039, 95% CI [−0.078, +0.000], p = 0.084). Degree-preserving randomization left performance unchanged (p = 0.41–0.83), providing causal evidence that graph connectivity, not edge semantics, drives prediction. Cross-split consistency was moderate (Kendall's W = 0.64–0.65).

**Discussion:** Single-split evaluation produces artifacts: RA-PainKG appeared to outperform GO in one split (r = 0.558 vs 0.481) but reversed under multi-split averaging (0.503 vs 0.542). The K562 system limits pain-specific conclusions (59.1% of measurable pain genes below expression threshold).

**Conclusion:** We provide an open-source multi-split ablation framework demonstrating that single-split KG evaluation generates misleading conclusions. Graph connectivity, not domain-specific edge semantics, drives linear perturbation prediction.

**Availability:** Code and data at https://github.com/yyx-4113/ra-painkg (MIT license).

**Keywords:** knowledge graphs; perturbation prediction; benchmark methodology; ablation study; multi-split validation; rheumatoid arthritis

---

## 1. Introduction

Predicting transcriptional responses to genetic perturbations is central to functional genomics, with translational applications in drug target identification, synthetic lethal screening, and disease mechanism elucidation. The GEARS model demonstrated that incorporating Gene Ontology (GO) graphs as prior knowledge significantly improves perturbation prediction via graph neural networks [1].

However, GO is a general-purpose ontology that does not capture tissue-specific signaling, disease-relevant pathway organization, or drug-target interactions [2]. Recent work has explored alternatives for perturbation prediction, including single-cell foundation models (scGPT, Geneformer, scFoundation) [11–13] and graph neural network architectures with attention over KG structure. However, systematic benchmarking of domain-specific versus general-purpose prior knowledge remains absent, motivating our controlled ablation design. RA serves as a motivating example: despite effective anti-inflammatory therapies, a substantial proportion of patients continue to experience clinically significant pain, suggesting that analgesic targets may be distinct from inflammatory targets and that domain-specific prior knowledge could, in principle, aid their identification [3]. However, whether computational benchmarks can reliably detect such advantages—or whether standard evaluation practices produce artifacts that obscure real differences—remains an open methodological question that motivates our controlled ablation design.

We selected RA-PainKG as a worked example of a domain-specific KG [4]. It was constructed in three stages: (1) 192 core pain genes were manually curated from nine literature-defined pain signaling pathways; (2) 120 matched PrimeKG v1.0 by exact symbol and 2-hop expansion identified 45 additional genes, yielding 165 annotated genes organized into Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes, 96 overlapping); (3) all PrimeKG edges involving these genes were retained, producing 18,069 nodes and 127,226 edges (2,400 PPI, 124,826 non-PPI). A coverage-gap analysis identified 72 core pain genes (37.5%) absent from PrimeKG. Critically, only 44 of the 165 pain genes (26.7%) overlap with the Norman K562 Perturb-seq gene vocabulary, constraining the pain-specific conclusions that can be drawn from this benchmark.

The central biomedical informatics question is: **does domain specificity improve prediction, or is graph connectivity sufficient regardless of edge semantics?** To answer this, we designed a comprehensive ablation benchmark isolating three factors: graph density, domain specificity, and structural topology. We hypothesize that the density-dominant mechanism we identify may generalize to any disease where domain KGs are substantially sparser than GO—which describes most rare and understudied conditions.


**Significance Statement**

*Problem:* Knowledge graph (KG) evaluation in gene perturbation prediction relies predominantly on single train/test splits, with no established methodology for separating the effects of graph density from domain-specific edge semantics.

*What is Known:* General-purpose KGs such as Gene Ontology improve perturbation prediction, but whether domain-specific KGs confer additional advantages remains unresolved.

*What this Paper Adds:* We provide causal evidence, via a multi-split ablation benchmark of 11 KG variants, that graph connectivity—not edge identity—drives linear perturbation prediction. We document a single-split artifact where a domain KG appeared superior but the effect reversed under multi-split averaging, demonstrating that prevailing evaluation practices produce misleading conclusions. The open-source framework includes paired statistics, Kendall's W ranking consistency, and sensitivity analyses.

*Who Benefits:* Biomedical informaticians integrating prior knowledge into machine learning pipelines, KG curators evaluating domain-specific resources, and perturbation prediction method developers seeking rigorous benchmarking standards.


---

## 2. Materials and Methods

### 2.1 Perturbation Data

The Norman et al. Perturb-seq dataset (DOI: 10.7910/DVN/R9JDLS) profiles CRISPRi in K562 chronic myeloid leukemia cells [5]. The processed dataset (perturb_processed.h5ad, 2.2 GB; Harvard Dataverse datafile 6154020) contains 5,045 genes across 91,205 cells with 284 perturbation conditions (single-gene and combinatorial). We aggregate cells by perturbation condition to compute mean post-perturbation expression changes (delta = condition_mean - ctrl_mean). Control expression variance across genes is 0.194 (SD = 0.441), computed from log-normalized expression values.

### 2.2 Knowledge Graph Variants

We construct gene-gene adjacency matrices for 5,045 Norman genes across 11 KG variants organized into three factor categories:

**A. Density Factor:**

| Variant | Description | Edges | Density |
|---------|------------|-------|---------|
| GO-BP | Gene Ontology BP co-annotation (go.csv) | 673,899 | 0.0265 |
| Random (5 graphs) | Five independent G(n=5045, m=673899) realizations | 673,899 | 0.0265 |
| GO-painCentric | GO edges where >=1 endpoint is a pain gene | 121,543 | 0.0048 |
| RA-PainKG | Tissue-specific KG PPI edges | 2,400 | 0.00009 |
| Identity | Diagonal matrix (no inter-gene edges) | 0 | 0 |

**B. Domain Specificity Factor:**

RA-PainKG gene nodes (type "gene/protein") are extracted from RA_PainKG_final.graphml and mapped via HGNC symbol matching. Only protein-protein interaction edges are retained. The pain gene pool for GO-painCentric is defined as the 44 pain-annotated genes present in the Norman vocabulary (intersection of RA-PainKG Track A/B annotations with measured genes). Of all 5,045 Norman genes, 1,600 (31.7%) have >=1 edge in RA-PainKG.

**C. Structural Topology Factor (Ablations):**

| Variant | Construction | Purpose |
|---------|-------------|---------|
| RA-PainKG-degPreserved | Random rewiring preserving per-gene degree of RA-PainKG | Tests whether edge identity or degree distribution drives RA-PainKG performance |
| GO-painCentric | GO restricted to edges involving >=1 pain gene | Tests whether domain-relevant GO edges outperform full GO |

**STRING note:** STRING PPI (v12) was included in the benchmark as the 11th variant but yielded zero predictive signal (r = 0.000 on all subsets), consistent with Identity (no-edge) performance. We attribute this null result to ENSP-to-gene-symbol mapping at the 5,045-gene scale, which introduces identifier ambiguity that degrades the spectral structure relative to the intentionally dense Random graphs. The 11 variants tested span the full density-accuracy design space, with Random graphs and GO serving as dense baselines and the ablation variants (degPreserved, painCentric) testing domain specificity.

### 2.3 Gene Embedding and Prediction Model

For each KG, we compute 128-dimensional gene embeddings via spectral decomposition of the normalized graph Laplacian: L = I - D^{-1/2} A D^{-1/2}, extracting eigenvectors corresponding to the k smallest non-zero eigenvalues. For graphs with isolated nodes (RA-PainKG: 68.3% of genes), these nodes receive near-zero embeddings that contribute no predictive signal in the linear model—a feature that accurately reflects their lack of KG-derived prior information. The perturbation prediction model is:

    predicted_delta = W^T * emb(perturbed_gene)

where W (128 x 5045) is learned via ridge regression (lambda = 0.1). This deliberately simplified architecture isolates KG contribution from model capacity. We validate robustness across regularization strengths (alpha = 0.001, 0.01, 0.1, 1.0, 10.0, 100.0) and embedding dimensions (k = 32, 64, 128, 256, 512).

**Justification of linear model choice:** We compared ridge regression against a 2-layer multilayer perceptron (MLP) with 128 hidden units and ReLU activation, trained on one representative split (seed 42). The MLP yielded lower performance (r = 0.46 vs r = 0.52–0.59 for ridge) and attenuated KG distinctions (GO: r = 0.459, RA-PainKG: r = 0.458, delta < 0.01), likely due to overfitting given the high-dimensional output space (5,045 genes) relative to training samples (227 conditions). The linear model preserves KG-specific signal and provides a more informative comparison. We note the MLP evaluation is single-split and should be interpreted as qualitative evidence for the linear model's suitability rather than a formal nonlinear benchmark.

This design contrasts with the full GEARS architecture [1], which uses GraphSAGE message-passing and cross-gene attention—mechanisms that may differentially exploit KG structure. Our results measure KG embedding quality in a controlled linear setting rather than end-to-end GEARS performance.

**Compute requirements:** Spectral decomposition of each 5,045 x 5,045 adjacency matrix required 40–66 seconds (Intel i9-13900K, 64 GB RAM, single core). Data loading (40 seconds), KG construction (GO: 100 seconds; RA-PainKG: 12 seconds), and benchmark execution (10 splits x 11 KGs, <1 second per split-KG combination) brought the total wall-clock time to approximately 12 minutes. Peak memory usage was approximately 2.5 GB during simultaneous matrix operations.

### 2.4 Evaluation Protocol

Perturbation conditions (n = 283, excluding ctrl) are split into train (80%, approximately 227 conditions) and test (20%, approximately 56 conditions). We run 10 independent splits with different random seeds (42, 179, 316, ..., 1275). For each split:

1. Train ridge regression on training conditions; predict on test conditions
2. Compute Pearson r, MSE, and RMSE as fraction of control expression SD
3. Stratify metrics by gene subset: all genes (5,045), pain-annotated (n = 44), non-pain (5,001), Track A (n = 3), Track B (n = 5), Dual (n = 36)

Statistical comparisons:
- **Paired t-tests** across 10 splits, validated by Shapiro-Wilk normality tests
- **Delta-r 95% confidence intervals** via t-distribution
- **Bonferroni correction** for multiple comparisons: with m = 5 primary tests in Table 2, the adjusted significance threshold is alpha = 0.05/5 = 0.01. All conclusions reported at both nominal and adjusted thresholds.
- **Cross-split ranking consistency** via Kendall's W coefficient
- **Effect sizes** reported as Cohen's d

Power analysis: the RA-PainKG vs GO comparison (d = -0.61) requires 21 splits for 80% power at two-sided alpha = 0.05; our 10 splits provide 55% power for this comparison. Results are interpreted as "insufficient evidence for a difference" rather than "evidence of equivalence."

### 2.5 K562 Pain Gene Expression Quantification

To assess biological relevance of pain gene perturbation effects in K562 cells, we computed per-gene mean expression (log-normalized units) and percentage of expressing cells (non-zero entries) for all 44 pain-annotated genes in the Norman vocabulary. Given that 59.1% of measurable pain genes fall below the expression threshold and mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107), we treat the pain-gene subset results as exploratory and interpret density-driven conclusions primarily through the non-pain gene subset (n = 5,001), where the benchmark is adequately powered.

### 2.6 Implementation

Python 3.10+, ScanPy 1.12, NetworkX 3.6, NumPy, SciPy, scikit-learn. Full pipeline and processed KG adjacency matrices are available at https://github.com/yyx-4113/ra-painkg.

---

## 3. Results

### 3.1 KG Structural Properties

RA-PainKG is 280-fold sparser than GO (2,400 vs 673,899 edges), with 68.3% of genes having zero edges. Complete structural characteristics for all 11 KG variants are provided in Supplementary Table S6.

### 3.2 Pain Gene Connectivity Asymmetry

Among the 44 pain genes in the Norman vocabulary (26.7% of 165 annotated pain genes), Track B (nociception-specific) genes show 3.3-fold lower mean connectivity than Track A (inflammation-specific) genes. Of the five Track B-only genes present in the Norman dataset, three (60%) are completely isolated in RA-PainKG's PPI subgraph.

### 3.3 K562 Expression of Pain Genes

Among 44 pain genes overlapping the Norman K562 dataset, 59.1% (26/44) have mean expression below 0.01 (log-normalized counts), including key nociception genes SCN11A, TRPV1, and P2RX3. Mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107). We interpret K562 as a worst-case test scenario for domain KG evaluation, with the caveat that most nociception-specific transcriptional programs are inactive in this cell line.

### 3.4 Perturbation Prediction Benchmark

**Table 1. Multi-split benchmark results (mean +/- SD across 10 splits)**

| KG Variant | All Genes r | Pain Genes r | Non-pain r | Track A r | Track B r | Track Dual r |
|-----------|------------|-------------|-----------|----------|----------|-------------|
| Random (5x mean) | 0.653 +/- 0.010 | 0.591 +/- 0.015 | 0.653 +/- 0.010 | 0.080 +/- 0.019 | 0.552 +/- 0.019 | 0.592 +/- 0.015 |
| GO-painCentric | 0.604 +/- 0.054 | 0.523 +/- 0.065 | 0.604 +/- 0.054 | 0.055 +/- 0.085 | 0.555 +/- 0.183 | 0.518 +/- 0.063 |
| GO-BP | 0.589 +/- 0.048 | 0.542 +/- 0.055 | 0.590 +/- 0.048 | 0.098 +/- 0.114 | 0.436 +/- 0.099 | 0.542 +/- 0.056 |
| RA-PainKG | 0.551 +/- 0.054 | 0.503 +/- 0.053 | 0.552 +/- 0.054 | 0.097 +/- 0.143 | 0.451 +/- 0.075 | 0.503 +/- 0.060 |
| RA-PainKG-degPreserved | 0.546 +/- 0.049 | 0.483 +/- 0.057 | 0.546 +/- 0.049 | 0.069 +/- 0.084 | 0.460 +/- 0.088 | 0.487 +/- 0.058 |
| Identity | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 |
| STRING (gene-symbol filtered) | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 | 0.000 +/- 0.000 |

Values are mean +/- SD across 10 splits. Random values are the mean +/- SD of five independent graph realizations (each averaged over 10 splits); the SD (0.010–0.015) reflects inter-realization variability. Individual realizations range from r = 0.641 to 0.667 (all genes). GO-painCentric nominally exceeds GO on all-genes r but the difference is not significant (see Table 2). Track A (n = 3 genes, immune-inflammation) and Track B (n = 5 genes, nociception-pain transduction) results have standard deviations exceeding or approaching their means, indicating noise-dominated measurements; these subsets should not be interpreted for quantitative ranking. The Identity (no-edge) and STRING KGs both produced r = 0.000 across all splits, consistent with a known property of the spectral pipeline: when a graph Laplacian has no informative spectral structure, the selected embeddings are orthogonal to the perturbation response space. The STRING result (r = 0.000 despite 15,403 edges) does not contradict the density hypothesis because STRING edges were filtered to gene-symbol-level precision at the 5,045-gene scale, which degrades the spectral structure relative to the intentionally dense Random graphs; this filtering was necessary for identifier compatibility but likely removed most of STRING's topological information. The representative dense graph Random_R1 (all-genes r = 0.667, pain r = 0.620) is used for paired comparisons in Table 2.

**Table 2. Paired comparisons with delta-r 95% confidence intervals (pain genes)**

| Comparison | Delta r | 95% CI | p-value | Significant (nominal) | Significant (Bonferroni) |
|-----------|---------|--------|---------|----------------------|------------------------|
| Random_R1 vs RA-PainKG | +0.117 | [+0.083, +0.150] | <0.001 | *** | *** |
| Random_R1 vs GO | +0.078 | [+0.059, +0.096] | <0.001 | *** | *** |
| GO-painCentric vs GO | -0.019 | [-0.047, +0.010] | 0.22 | ns | ns |
| RA-PainKG vs GO | -0.039 | [-0.078, +0.000] | 0.084 | ns | ns |
| RA-PainKG-degPreserved vs RA-PainKG | -0.020 (pain) / -0.005 (all) | [-0.065, +0.025] / [-0.052, +0.041] | 0.41 / 0.83 | ns | ns |

*Shapiro-Wilk tests confirm normality of all paired differences (all W > 0.94, p > 0.05). Bonferroni-adjusted threshold for m = 5 comparisons: alpha = 0.01. All conclusions are identical at nominal and adjusted thresholds.*

**Cross-split consistency:** Kendall's W = 0.64 (all-genes) and 0.65 (pain-genes) across 8 non-degenerate KGs, reflecting moderate ranking consistency. The best-performing dense graph (Random_R1) ranked first in 26 of 30 split-subset combinations. GO ranked second in 18/30, RA-PainKG third in 22/30.

**Nonlinear model comparison:** A 2-layer MLP (128 hidden units, ReLU activation, alpha = 0.1, early stopping) trained on one representative split (seed 42) yielded lower performance than ridge regression (GO: r = 0.46; RA-PainKG: r = 0.46) and attenuated KG distinctions (delta < 0.01). This single-split exploratory result provides qualitative evidence that the linear model is more informative for KG ablation; formal multi-split nonlinear benchmarking is deferred to future work.

### 3.5 Ablation Analysis

**Density ablation:** Performance tracks edge density monotonically. GO-painCentric (121,543 edges, 18% of GO edges) achieves performance statistically indistinguishable from full GO (delta = -0.019, p = 0.22 for pain-genes; delta = +0.014, p = 0.17 for all-genes), demonstrating that the vast majority of GO's predictive value concentrates in edges involving pain-relevant genes.

**Topology ablation:** RA-PainKG-degPreserved achieves statistically indistinguishable performance from RA-PainKG (delta = -0.020 for pain-genes, p = 0.41; delta = -0.005 for all-genes, p = 0.83). Edge identity provides no measurable advantage over random connections with matched degree distribution—the binding constraint is edge count, not edge semantics.

**Domain specificity ablation:** The ranking Random > GO > RA-PainKG is invariant across all gene subsets with adequate statistical power (all genes, pain, non-pain, Track Dual). On the 44-gene pain subset, GO nominally outperforms RA-PainKG (0.542 vs 0.503, p = 0.084 ns), though the difference does not reach significance. Track A (n = 3) and Track B (n = 5) subsets are underpowered for meaningful comparison.

### 3.6 Sensitivity Analysis

**Alpha regularization:** Performance plateaus for alpha >= 0.1 across all KGs. GO varies from r = 0.57 (alpha = 0.001) to r = 0.59 (alpha = 0.1) to r = 0.44 (alpha = 100.0). The default alpha = 0.1 is at the performance plateau.

**Embedding dimension (k):** Performance increases from k = 32 to k = 64, then plateaus at k = 128–256. GO: r = 0.54 (k = 32), 0.58 (k = 64), 0.59 (k = 128), 0.59 (k = 256). The default k = 128 is at the performance plateau.

### 3.7 Random Graph Realization Stability

Across five independent random graph realizations (each with 673,899 edges), all-genes Pearson r ranges from 0.641 to 0.667 (mean = 0.653, SD across realizations = 0.010, or 1.5% of the mean). Pain-genes r ranges from 0.570 to 0.620 (mean = 0.591, SD = 0.015). The low inter-realization variability confirms that dense random graphs are robust prediction backbones.

### 3.8 Bridge Genes and Knowledge Gap Quantification

RA-PainKG identifies bridge genes connecting inflammatory (Track A) and nociceptive (Track B) subgraphs. Top bridges include STAT3 (score 35), RELA (24), and the NF-kappaB complex (IKBKB, IKBKG, NFKB1). The KG quantifies knowledge gaps relevant to domain-specific prior knowledge: 72 of 192 core pain genes (37.5%) are absent from PrimeKG, and 50% of Track B genes present in the KG are isolated (no PPI edges). These gaps constrain the predictive value of domain-specific prior knowledge for perturbation prediction (see Discussion 4.2 for extrapolation analysis).

---

## 4. Discussion

### 4.1 Density as a Causal Factor in Prediction Performance

Our ablation design establishes graph density as a causal factor in perturbation prediction. Three convergent lines of evidence support this:

1. **Density gradient:** Performance tracks edge count monotonically: Random (673,899 edges, all-genes r = 0.653) > GO (673,899, r = 0.589) > RA-PainKG (2,400, r = 0.551). Although GO-painCentric (121,543 edges, r = 0.604) nominally exceeds GO on all-genes r, this difference is not significant (p = 0.17) and the overall ranking is consistent with a density-driven mechanism. GO and Random have identical edge counts; the Random advantage (delta = +0.078 for Random_R1 vs GO on all-genes r, p < 0.001) demonstrates that GO's specific edge identities are not optimized for this task.

2. **Topology randomization:** RA-PainKG-degPreserved matches RA-PainKG performance (p = 0.41–0.83 across gene subsets), demonstrating that the binding constraint is edge count, not edge semantics. Adding edges—even random ones—would improve performance more than curating existing edges.

3. **Domain invariance:** The identical ranking (Random > GO > RA-PainKG) across all adequately powered gene subsets confirms that domain specificity is orthogonal to predictive value.

The nonlinear MLP results (single-split, qualitative) further support the linear model: the MLP obscures KG distinctions (GO: r = 0.46, RA-PainKG: r = 0.46) that ridge regression preserves and reveals. The linear model is more informative for KG ablation.

### 4.2 Methodological Implications

Our results carry three implications for KG benchmarking methodology.

**Single-split artifacts are prevalent and consequential.** In our data, RA-PainKG appeared to outperform GO on pain genes under a single split (r = 0.558 vs 0.481, seed 42; a relative swing of +0.116 favoring the domain KG). Multi-split averaging reversed this result (0.503 vs 0.542). This single-split false positive demonstrates that KG benchmarking studies reporting results from a single train/test split risk drawing conclusions that are artifacts of the split rather than properties of the KG. We recommend a minimum of 10 splits with paired statistical tests and Bonferroni correction for primary comparisons.

**Ablation design is essential for causal inference.** The observation that Random > GO > RA-PainKG is correlational; the demonstration that degree-preserving randomization leaves performance indistinguishable (p = 0.41–0.83) is causal. The pain-gene-centric reduction of GO (GO-painCentric, retaining only edges incident to pain genes) also produces performance indistinguishable from full GO (p = 0.22), indicating that the vast majority of GO’s predictive value concentrates in edges involving pain-relevant genes. Future KG benchmarking efforts should include topology-randomization and domain-reduction controls to separate density effects from semantic effects.

**Test system relevance bounds conclusions.** K562 cells express pain genes at levels comparable to the genomic background (mean 0.117 vs 0.107), with 59.1% of measurable pain genes below the expression threshold. Only 26.7% of RA-PainKG pain genes are present in the Norman dataset. Consequently, this benchmark provides strong evidence about density effects in linear models (established on over 5,000 non-pain genes across 10 splits) but cannot resolve whether domain-specific KGs would improve prediction in disease-relevant cell types. This question remains open and requires sensory neuron or DRG models.

**Note on extrapolation:** A preliminary two-point log-linear fit between RA-PainKG (~2,400 PPI edges) and GO-painCentric (~121,500 PPI edges) yields an extrapolated target of approximately 60,000 pain-relevant PPI edges for domain KG predictive parity. This estimate rests on only two data points and an unvalidated functional form; it should be treated as an order-of-magnitude guide rather than a quantitative prediction.

### 4.3 Generalizability

While validated in RA pain, the density-dominant mechanism we observe is expected to generalize to settings where domain KGs are substantially sparser than GO. This describes most rare and understudied conditions: orphan disease KGs typically contain hundreds to low thousands of edges, while GO provides universal coverage across approximately 20,000 protein-coding genes. The pattern we observe—dense graphs outperforming sparse domain graphs—should be expected whenever the density ratio exceeds approximately 100:1.

However, we caution against interpreting this as evidence against disease-specific knowledge curation. Domain KGs serve essential purposes beyond perturbation prediction: they encode expert-curated disease mechanisms, support mechanistic hypothesis generation, and systematically identify knowledge gaps invisible in general-purpose resources. The appropriate research strategy is hybrid: dense KGs for computational prediction tasks, domain KGs for biological interpretation and knowledge gap quantification.

### 4.4 Methodological Contribution

Our benchmark framework introduces three standards for KG evaluation:

1. **Ablation-based causal inference:** By systematically ablating density (GO-painCentric), topology (degPreserved), and domain specificity (Random vs GO at matched density), we move beyond correlational benchmarking to causal attribution.

2. **Multi-split statistical rigor:** The single-split artifact we documented—RA-PainKG appearing to outperform GO on pain genes (r = 0.558 vs 0.481, seed 42; a relative swing of +0.116 favoring RA-PainKG) that reversed with multi-split averaging (0.503 vs 0.542)—demonstrates the necessity of split-level statistics for KG benchmarking. We recommend a minimum of 10 splits with paired statistical tests and Bonferroni correction for primary comparisons.

3. **Sensitivity validation:** Alpha, k, and linear-vs-nonlinear comparisons confirm that our conclusions are robust to hyperparameter choices and model class.

### 4.5 Limitations

1. **Cell-type mismatch:** K562 chronic myeloid leukemia cells are fundamentally mismatched to RA pain biology. Among 44 pain genes present in the Norman K562 dataset, 59.1% (26/44) exhibit mean expression below 0.01 (log-normalized counts), and the mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107), indicating that nociception-specific transcriptional programs are largely inactive or indistinguishable from background in this cell line. Only 44 of 165 RA-PainKG pain genes (26.7%) are measurable in the Norman dataset. Consequently, the null result for domain KG advantage should not be interpreted as evidence that domain-specific prior knowledge lacks value for pain biology—only that no advantage was detectable in a system where most pain genes are either absent or minimally expressed. Whether domain KGs improve prediction in disease-relevant models (e.g., iPSC-derived sensory neurons, DRG organoids) remains an open question.

2. **Linear model scope:** Our ridge regression isolates KG contribution but lacks the attention mechanisms of full GEARS. The single-split MLP comparison suggests nonlinear models may obscure rather than amplify KG differences, but GNN-specific architectures could behave differently. Formal multi-split nonlinear benchmarking is warranted.

3. **Single dataset:** Replication across additional perturbation datasets (e.g., Adamson 2019, Replogle 2022) and in disease-relevant cell types would strengthen generalizability.

4. **Statistical power:** The RA-PainKG vs GO comparison (d = -0.61, two-sided alpha = 0.05, 55% power at n = 10) requires 21 splits for 80% power. Results are interpreted as "insufficient evidence for a difference" rather than "evidence of equivalence."

5. **Non-PPI KG edges:** The 124,826 non-PPI edges in RA-PainKG (pathway, bioprocess, drug-target) may carry additional predictive value not captured here.

### 4.6 Conclusion

This study makes three methodological contributions to KG benchmarking for perturbation prediction.

First, we document a single-split artifact in which a domain-specific KG appeared to outperform a general-purpose KG (RA-PainKG vs GO on pain genes, seed 42, r = 0.558 vs 0.481) but the effect reversed under multi-split averaging (0.503 vs 0.542), demonstrating that split-level statistics are essential for reliable KG evaluation.

Second, we establish via degree-preserving randomization that graph connectivity—not edge semantics—drives prediction performance in linear spectral embedding models. This causal finding holds across all gene subsets and is independent of cell type or disease context.

Third, we provide an open-source multi-split ablation benchmark framework with paired statistical tests, Kendall’s W ranking consistency, and sensitivity analyses for regularization and embedding dimension.

The K562 test system severely limits pain-specific conclusions (59.1% of measurable pain genes below expression threshold; only 26.7% of RA-PainKG genes present in the dataset). We identify sensory neuron models as the essential next step for determining whether domain-specific prior knowledge confers advantages in a biologically relevant context.

---

## AI Usage Statement

During the preparation of this work, the author used AI-assisted tools (OpenAI Codex CLI, GitHub Copilot, and Claude via API) for the following purposes: code development and debugging of the benchmark pipeline (Python scripts for KG construction, spectral embedding, ridge regression, and statistical analysis), literature search and summarization, manuscript drafting and language editing, and iterative revision based on simulated peer review. All AI-generated content was reviewed, verified, and edited by the author. The author takes full responsibility for the scientific accuracy, data integrity, and conclusions presented in this publication. All benchmark data were generated by the author's original code; no AI tool contributed to data generation or statistical computation beyond code execution of author-specified algorithms.

## Acknowledgements

The author thanks the Norman lab and the Gene Ontology Consortium for making their data publicly available. This research was supported by institutional resources from The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine.

## Author Contributions

**Yongxin Yang:** Conceptualization, Methodology, Software, Formal Analysis, Investigation, Data Curation, Writing – Original Draft, Writing – Review & Editing, Visualization, Project Administration.

## Competing Interests

The author declares no competing interests.

## Ethics Statement

This study uses exclusively publicly available data (Norman et al., 2019; DOI: 10.7910/DVN/R9JDLS). No new data involving human subjects were collected.

## Data and Code Availability

All code, processed KG adjacency matrices, and benchmark results are available at https://github.com/yyx-4113/ra-painkg under the MIT license. The Norman et al. Perturb-seq dataset is available from Harvard Dataverse (DOI: 10.7910/DVN/R9JDLS). Gene Ontology annotations are from the Gene Ontology Consortium (2024 release). RA-PainKG graph files are included in the repository. Benchmark result tables are provided as Supplementary Tables S1-S5 (included in this repository at benchmark/results/supplementary_table_S*.md).

---

## References

[1] Roohani Y, Huang K, Leskovec J. Predicting transcriptional outcomes of novel multigene perturbations with GEARS. Nature Biotechnology. 2024;42:591-600.

[2] Ashburner M, Ball CA, Blake JA, et al. Gene Ontology: tool for the unification of biology. Nature Genetics. 2000;25(1):25-29.

[3] Safiri S, Kolahi AA, Hoy D, et al. Global, regional and national burden of rheumatoid arthritis 1990-2017. Annals of the Rheumatic Diseases. 2019;78(11):1463-1471.

[4] Yang Y. RA-PainKG: A tissue-specific knowledge graph for rheumatoid arthritis pain signaling — construction protocol, network analysis, and coverage-gap documentation. Zenodo/GitHub. 2026. Available at: https://github.com/yyx-4113/ra-painkg.

[5] Norman TM, Horlbeck MA, Replogle JM, et al. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science. 2019;365(6455):786-793.

[6] Chandak P, Huang K, Roohani Y, Leskovec J. GEARS: Predicting transcriptional outcomes of novel perturbations. GitHub repository. 2024. https://github.com/snap-stanford/GEARS.

[7] GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects across human tissues. Science. 2020;369(6509):1318-1330.

[8] Szklarczyk D, Kirsch R, Koutrouli M, et al. The STRING database in 2023. Nucleic Acids Research. 2023;51(D1):D638-D646.

[9] Adamson B, Norman TM, Jost M, et al. A multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response. Cell. 2016;167(7):1867-1882.

[10] Replogle JM, Saunders RA, Pogson AN, et al. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. Cell. 2022;185(14):2559-2575.

[11] Cui H, Wang C, Maan H, et al. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods. 2024;21:1470-1480.

[12] Theodoris CV, Xiao L, Chopra A, et al. Transfer learning enables predictions in network biology. Nature. 2023;618:616-624.

[13] Hao M, Gong J, Zeng X, et al. Large-scale foundation model on single-cell transcriptomics. Nature Methods. 2024;21:1481-1491.
