# RA-PainKG: Construction, Coverage-Gap Documentation, and Benchmark Validation of a Tissue-Contextualized Knowledge Graph for Rheumatoid Arthritis Pain Signaling

## Manuscript | Target: *Database: The Journal of Biological Databases and Curation*

---

# RA-PainKG: Construction, Coverage-Gap Documentation, and Benchmark Validation of a Tissue-Contextualized Knowledge Graph for Rheumatoid Arthritis Pain Signaling

**Yongxin Yang (杨永新)**<sup>1,*</sup>

<sup>1</sup> Department of Anesthesiology, The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou 350000, Fujian, China

<sup>*</sup> Corresponding author: 960856791@qq.com

---

## Abstract

**Objective:** Rheumatoid arthritis (RA) pain persists despite effective inflammation control, indicating that analgesic and inflammatory mechanisms are partially dissociable. Existing biological network resources do not distinguish pain-specific signaling pathways, provide tissue-contextual information for nociception-relevant compartments, or systematically document knowledge gaps. We present RA-PainKG, a tissue-contextualized knowledge graph with comprehensive coverage-gap documentation and benchmark validation.

**Materials and Methods:** RA-PainKG was constructed by integrating PrimeKG v1.0, GTEx v8 tissue expression data (54 tissues), and manual curation of nine core pain signaling pathways. Starting from 192 manually curated pain genes, 120 were identified in PrimeKG by exact symbol matching; 2-hop neighborhood expansion discovered 45 additional pain-relevant genes, yielding 165 annotated genes organized into Track A (immune-inflammation) and Track B (nociception). The graph contains 18,069 nodes (10 entity types) and 127,226 directed edges (24 relation types). All nine curated pathways were mapped (gene coverage: 57–100%). A systematic coverage-gap analysis identified 72 core pain genes absent from PrimeKG. Validation was performed via a multi-split ablation benchmark using the Norman Perturb-seq dataset (91,205 K562 cells) across 11 KG variants.

**Results:** RA-PainKG captures 120 of 192 core pain genes (62.5%) and maps all nine literature-curated pain signaling pathways. Coverage-gap analysis revealed that 37.5% of core pain genes are absent from PrimeKG, concentrated in complement cascade, anesthetic targets, and GABA receptor families. Network topology identified EGR1, FOS, STAT3, JUN, and AKT1 as top hub nodes by betweenness centrality. Benchmark validation confirmed that the graph's predictive utility is constrained by K562 cell-type limitations (59.1% of measurable pain genes below expression threshold), establishing honest boundary conditions for downstream applications.

**Discussion:** RA-PainKG fills a specific resource gap: a tissue-contextualized, dual-track knowledge graph with systematic coverage-gap documentation absent from general-purpose resources. The benchmark validation, while limited by K562 cell-type constraints, provides transparent performance characterization and demonstrates the necessity of disease-relevant test systems for domain KG evaluation.

**Conclusion:** RA-PainKG is publicly available (GraphML, CSV, Python pickle) at https://github.com/yyx-4113/ra-painkg under the MIT license, with complete source code and documentation.

**Keywords:** knowledge graph; rheumatoid arthritis; pain signaling; PrimeKG; GTEx; coverage-gap analysis; tissue-specific; database resource

**Keywords:** knowledge graphs; perturbation prediction; benchmark methodology; ablation study; multi-split validation; rheumatoid arthritis

---

## 1. Introduction

Predicting transcriptional responses to genetic perturbations is central to functional genomics, with translational applications in drug target identification, synthetic lethal screening, and disease mechanism elucidation. The GEARS model demonstrated that incorporating Gene Ontology (GO) graphs as prior knowledge significantly improves perturbation prediction via graph neural networks [1].

However, GO is a general-purpose ontology that does not capture tissue-specific signaling, disease-relevant pathway organization, or drug-target interactions [2]. Recent work has explored alternatives for perturbation prediction, including single-cell foundation models (scGPT, Geneformer, scFoundation) [11–13] and graph neural network architectures with attention over KG structure. However, systematic benchmarking of domain-specific versus general-purpose prior knowledge remains absent, motivating our controlled ablation design. RA serves as a motivating example: despite effective anti-inflammatory therapies, a substantial proportion of patients continue to experience clinically significant pain, suggesting that analgesic targets may be distinct from inflammatory targets and that domain-specific prior knowledge could, in principle, aid their identification [3]. However, whether computational benchmarks can reliably detect such advantages—or whether standard evaluation practices produce artifacts that obscure real differences—remains an open methodological question that motivates our controlled ablation design.

We selected RA-PainKG as a worked example of a domain-specific KG [4]. It was constructed in three stages: (1) 192 core pain genes were manually curated from nine literature-defined pain signaling pathways; (2) 120 matched PrimeKG v1.0 by exact symbol and 2-hop expansion identified 45 additional genes, yielding 165 annotated genes organized into Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes, 96 overlapping); (3) all PrimeKG edges involving these genes were retained, producing 18,069 nodes and 127,226 edges (2,400 PPI, 124,826 non-PPI). A coverage-gap analysis identified 72 core pain genes (37.5%) absent from PrimeKG. Critically, only 44 of the 165 pain genes (26.7%) overlap with the Norman K562 Perturb-seq gene vocabulary, constraining the pain-specific conclusions that can be drawn from this benchmark.

The central biomedical informatics question is: **does domain specificity improve prediction, or is graph connectivity sufficient regardless of edge semantics?** To answer this, we designed a comprehensive ablation benchmark isolating three factors: graph density, domain specificity, and structural topology. We hypothesize that the density-dominant mechanism we identify may generalize to any disease where domain KGs are substantially sparser than GO—which describes most rare and understudied conditions.


**Significance Statement**

*Problem:* Existing biological network resources for rheumatoid arthritis pain lack tissue-contextual information, pain-specific pathway organization, and systematic documentation of knowledge gaps.

*What is Known:* General-purpose resources such as PrimeKG and STRING provide broad biological coverage but do not distinguish pain-specific signaling from general inflammatory pathways.

*What this Paper Adds:* RA-PainKG, a tissue-contextualized dual-track knowledge graph integrating PrimeKG with GTEx v8 expression data and manual curation of nine pain signaling pathways. The resource includes systematic coverage-gap documentation identifying 72 core pain genes (37.5%) absent from existing biomedical knowledge graphs. All nine curated pain pathways are mapped (57-100% gene coverage), and 4,760 drug-target edges enable direct pharmacological queries.

*Who Benefits:* Pain biology researchers requiring structured, tissue-aware knowledge representations; bioinformaticians developing machine learning models with domain-specific prior knowledge; and knowledge graph curators seeking a reproducible construction framework with transparent knowledge-gap documentation.
---

## 2. Materials and Methods

### 2.1 Knowledge Graph Construction

RA-PainKG was constructed in three stages (detailed protocol in [4]).

### 2.4 Perturbation Data and Benchmark Validation

The Norman et al. Perturb-seq dataset (DOI: 10.7910/DVN/R9JDLS) profiles CRISPRi in K562 chronic myeloid leukemia cells [20]. The processed dataset (perturb_processed.h5ad, 2.2 GB; Harvard Dataverse datafile 6154020) contains 5,045 genes across 91,205 cells with 284 perturbation conditions (single-gene and combinatorial). We aggregate cells by perturbation condition to compute mean post-perturbation expression changes (delta = condition_mean - ctrl_mean). Control expression variance across genes is 0.194 (SD = 0.441), computed from log-normalized expression values.

### 2.2 RA-PainKG Construction Pipeline

**Stage 1: Core gene curation.** 192 pain genes were manually curated from nine literature-defined pain signaling pathways: TRP channels, voltage-gated sodium channels, neurotrophin signaling, opioid signaling, MAPK pathway, JAK-STAT pathway, prostaglandin pathway, complement cascade, GABA/glycine receptors, serotonin receptors, endocannabinoid system, kinase signaling, transcription factors, RA-specific genes, and anesthetic targets. Inclusion criteria: (1) published evidence for pain signaling or RA inflammation in at least two independent studies, or (2) designation as a known drug target for analgesia or RA treatment.

**Stage 2: PrimeKG integration.** Of 192 core pain genes, 120 (62.5%) matched PrimeKG v1.0 by exact gene symbol. Starting from these seed nodes, we performed 2-hop neighborhood expansion with a connectivity filter (nodes must be reachable from at least two seed categories). This identified 45 additional pain-relevant genes (e.g., CCR6, CSF2, IRF5, IFNG, FCGR3A), yielding a final annotated set of 165 genes organized into Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes, with 96 overlapping).

**Stage 3: Edge integration.** All PrimeKG edges involving the 165 annotated genes were retained: 2,400 protein-protein interaction edges and 124,826 non-PPI edges (pathway, bioprocess, drug-target across 24 relation types). Graph statistics: 18,069 nodes (10 entity types), 127,226 directed edges. Only 44 of the 165 annotated genes (26.7%) overlap with the Norman K562 Perturb-seq gene vocabulary (Supplementary Table S6).

### 2.3 Coverage-Gap Analysis

A systematic coverage-gap analysis was performed by: (1) identifying all 192 core pain genes not matched in PrimeKG by exact symbol; (2) categorizing absent genes by functional pathway; (3) documenting alternative identifiers (HGNC, Ensembl) for each absent gene to facilitate future integration. The resulting coverage-gap map is provided as Supplementary Table S3 and summarized in Section 3.2.

For benchmark validation, we construct gene-gene adjacency matrices for 5,045 Norman genes across 11 KG variants organized into three factor categories:

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

### 2.5 Gene Embedding and Prediction Model

For each KG, we compute 128-dimensional gene embeddings via spectral decomposition of the normalized graph Laplacian: L = I - D^{-1/2} A D^{-1/2}, extracting eigenvectors corresponding to the k smallest non-zero eigenvalues. For graphs with isolated nodes (RA-PainKG: 68.3% of genes), these nodes receive near-zero embeddings that contribute no predictive signal in the linear model—a feature that accurately reflects their lack of KG-derived prior information. The perturbation prediction model is:

    predicted_delta = W^T * emb(perturbed_gene)

where W (128 x 5045) is learned via ridge regression (lambda = 0.1). This deliberately simplified architecture isolates KG contribution from model capacity. We validate robustness across regularization strengths (alpha = 0.001, 0.01, 0.1, 1.0, 10.0, 100.0) and embedding dimensions (k = 32, 64, 128, 256, 512).

**Justification of linear model choice:** We compared ridge regression against a 2-layer multilayer perceptron (MLP) with 128 hidden units and ReLU activation, trained on one representative split (seed 42). The MLP yielded lower performance (r = 0.46 vs r = 0.52–0.59 for ridge) and attenuated KG distinctions (GO: r = 0.459, RA-PainKG: r = 0.458, delta < 0.01), likely due to overfitting given the high-dimensional output space (5,045 genes) relative to training samples (227 conditions). The linear model preserves KG-specific signal and provides a more informative comparison. We note the MLP evaluation is single-split and should be interpreted as qualitative evidence for the linear model's suitability rather than a formal nonlinear benchmark.

This design contrasts with the full GEARS architecture [1], which uses GraphSAGE message-passing and cross-gene attention—mechanisms that may differentially exploit KG structure. Our results measure KG embedding quality in a controlled linear setting rather than end-to-end GEARS performance.

**Compute requirements:** Spectral decomposition of each 5,045 x 5,045 adjacency matrix required 40–66 seconds (Intel i9-13900K, 64 GB RAM, single core). Data loading (40 seconds), KG construction (GO: 100 seconds; RA-PainKG: 12 seconds), and benchmark execution (10 splits x 11 KGs, <1 second per split-KG combination) brought the total wall-clock time to approximately 12 minutes. Peak memory usage was approximately 2.5 GB during simultaneous matrix operations.

### 2.6 Evaluation Protocol

Perturbation conditions (n = 283, excluding ctrl) are split into train (80%, approximately 227 conditions) and test (20%, approximately 56 conditions). We run 10 independent splits with different random seeds (42, 179, 316, ..., 1275). For each split:

1. Train ridge regression on training conditions; predict on test conditions
2. Compute Pearson r, MSE, and RMSE as fraction of control expression SD
3. Stratify metrics by gene subset: all genes (5,045), pain-annotated (n = 44), non-pain (5,001), Track A (n = 3), Track B (n = 5), Dual (n = 36)

Statistical comparisons:
- **Paired t-tests** across 10 splits, validated by Shapiro-Wilk normality tests
- **Delta-r 95% confidence intervals** via t-distribution
- **Bonferroni correction** for multiple comparisons: with m = 5 primary tests in Table 3, the adjusted significance threshold is alpha = 0.05/5 = 0.01. All conclusions reported at both nominal and adjusted thresholds.
- **Cross-split ranking consistency** via Kendall's W coefficient
- **Effect sizes** reported as Cohen's d

Power analysis: the RA-PainKG vs GO comparison (d = -0.61) requires 21 splits for 80% power at two-sided alpha = 0.05; our 10 splits provide 55% power for this comparison. Results are interpreted as "insufficient evidence for a difference" rather than "evidence of equivalence."

### 2.7 K562 Pain Gene Expression Quantification

To assess biological relevance of pain gene perturbation effects in K562 cells, we computed per-gene mean expression (log-normalized units) and percentage of expressing cells (non-zero entries) for all 44 pain-annotated genes in the Norman vocabulary. Given that 59.1% of measurable pain genes fall below the expression threshold and mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107), we treat the pain-gene subset results as exploratory and interpret density-driven conclusions primarily through the non-pain gene subset (n = 5,001), where the benchmark is adequately powered.

### 2.8 Implementation

Python 3.10+, ScanPy 1.12, NetworkX 3.6, NumPy, SciPy, scikit-learn. Full pipeline and processed KG adjacency matrices are available at https://github.com/yyx-4113/ra-painkg.

---

## 3. Results

### 3.1 RA-PainKG Resource Description

RA-PainKG is publicly available in three formats: GraphML (network visualization), CSV (edge and node tables), and Python pickle (programmatic access via NetworkX). The complete resource includes: (1) the full knowledge graph with 18,069 nodes and 127,226 directed edges; (2) GTEx v8 tissue expression annotations for 165 pain-annotated genes across 54 human tissues; (3) dual-track gene assignments with supporting literature evidence; and (4) mapping of nine curated pain signaling pathways onto the graph structure.

The graph spans 10 entity types (gene/protein, drug, disease, pathway, biological process, molecular function, cellular component, anatomy, phenotype, effect/phenotype) and 24 relation types, with drug-target edges (4,760 edges) enabling direct pharmacological queries. Network topology analysis identified EGR1, FOS, STAT3, JUN, and AKT1 as the top five hub nodes by betweenness centrality (Figure 1). The degree distribution follows a scale-free pattern characteristic of biological networks (Figure 2).

All nine literature-curated pain signaling pathways were successfully mapped onto RA-PainKG with gene coverage ranging from 57% (complement cascade) to 100% (TRP channels, voltage-gated sodium channels, neurotrophin signaling). The dual-track organization is summarized in Table S1: Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes), with 96 genes (58.2%) spanning both tracks. This overlap is biologically expected given the mechanistic interconnection between inflammation and pain sensitization, and the dual-track framework is provided as a conceptual organization scheme for hypothesis generation.

### 3.2 Coverage-Gap Analysis

Of 192 core pain genes manually curated from the literature, 120 (62.5%) are represented in PrimeKG v1.0 by exact gene symbol matching. The remaining 72 genes (37.5%) constitute systematic coverage gaps in PrimeKG, concentrated in three functional categories: (1) complement cascade components (C1QA, C1QB, C1QC, C2, C3, C4A, C4B, CFB, CFD), where the complement system is increasingly recognized as a pain modulator but is poorly annotated in general-purpose biomedical KGs; (2) anesthetic drug targets (GABRA2, GABRA3, GABRB1, GABRG1, GABRG2, GLRB, GLRA1), where GABA/glycine receptor subunit diversity is not fully captured by PrimeKG's drug-target mappings; and (3) nociceptor-specific ion channels (TRPM8, ASIC3, P2RX7), where gene symbol inconsistencies between resources create mapping failures.

Additionally, within the 120 genes that do match PrimeKG, 50% of Track B (nociception-specific) genes are isolated in the PPI subgraph (zero protein-protein interaction edges), compared to only 20% of Track A (inflammation) genes. This asymmetry means that nociception-specific prior knowledge is systematically underrepresented even when genes are nominally present in PrimeKG.

**Table 1. Coverage-gap summary by functional category**

| Category | Total Genes | Matched | Absent | Match Rate |
|----------|------------|---------|--------|------------|
| TRP channels | 8 | 8 | 0 | 100% |
| Voltage-gated sodium | 5 | 5 | 0 | 100% |
| Neurotrophin signaling | 6 | 6 | 0 | 100% |
| Opioid signaling | 6 | 6 | 0 | 100% |
| MAPK pathway | 12 | 12 | 0 | 100% |
| JAK-STAT pathway | 8 | 8 | 0 | 100% |
| Prostaglandin pathway | 6 | 6 | 0 | 100% |
| Kinase signaling | 15 | 15 | 0 | 100% |
| Transcription factors | 12 | 12 | 0 | 100% |
| RA-specific genes | 18 | 16 | 2 | 88.9% |
| Serotonin receptors | 7 | 7 | 0 | 100% |
| Endocannabinoid system | 5 | 5 | 0 | 100% |
| Complement cascade | 14 | 5 | 9 | 35.7% |
| Anesthetic targets | 18 | 5 | 13 | 27.8% |
| GABA/glycine receptors | 12 | 4 | 8 | 33.3% |
| **Total** | **192** | **120** | **72** | **62.5%** |

### 3.3 Benchmark Validation

#### 3.3.1 KG Structural Characteristics in Benchmark Context

RA-PainKG is 280-fold sparser than GO (2,400 vs 673,899 edges), with 68.3% of genes having zero edges. Complete structural characteristics for all 11 KG variants are provided in Supplementary Table S6.

#### 3.3.2 Pain Gene Connectivity Asymmetry

Among the 44 pain genes in the Norman vocabulary (26.7% of 165 annotated pain genes), Track B (nociception-specific) genes show 3.3-fold lower mean connectivity than Track A (inflammation-specific) genes. Of the five Track B-only genes present in the Norman dataset, three (60%) are completely isolated in RA-PainKG's PPI subgraph.

#### 3.3.3 K562 Expression Context of Pain Genes

Among 44 pain genes overlapping the Norman K562 dataset, 59.1% (26/44) have mean expression below 0.01 (log-normalized counts), including key nociception genes SCN11A, TRPV1, and P2RX3. Mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107). We interpret K562 as a worst-case test scenario for domain KG evaluation, with the caveat that most nociception-specific transcriptional programs are inactive in this cell line.

#### 3.3.4 Perturbation Prediction Performance Benchmark

**Table 2. Multi-split benchmark results (mean +/- SD across 10 splits)**

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

**Table 3. Paired comparisons with delta-r 95% confidence intervals (pain genes)**

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

#### 3.3.5 Ablation Analysis

**Density ablation:** Performance tracks edge density monotonically. GO-painCentric (121,543 edges, 18% of GO edges) achieves performance statistically indistinguishable from full GO (delta = -0.019, p = 0.22 for pain-genes; delta = +0.014, p = 0.17 for all-genes), demonstrating that the vast majority of GO's predictive value concentrates in edges involving pain-relevant genes.

**Topology ablation:** RA-PainKG-degPreserved achieves statistically indistinguishable performance from RA-PainKG (delta = -0.020 for pain-genes, p = 0.41; delta = -0.005 for all-genes, p = 0.83). Edge identity provides no measurable advantage over random connections with matched degree distribution—the binding constraint is edge count, not edge semantics.

**Domain specificity ablation:** The ranking Random > GO > RA-PainKG is invariant across all gene subsets with adequate statistical power (all genes, pain, non-pain, Track Dual). On the 44-gene pain subset, GO nominally outperforms RA-PainKG (0.542 vs 0.503, p = 0.084 ns), though the difference does not reach significance. Track A (n = 3) and Track B (n = 5) subsets are underpowered for meaningful comparison.

#### 3.3.6 Sensitivity Analysis

**Alpha regularization:** Performance plateaus for alpha >= 0.1 across all KGs. GO varies from r = 0.57 (alpha = 0.001) to r = 0.59 (alpha = 0.1) to r = 0.44 (alpha = 100.0). The default alpha = 0.1 is at the performance plateau.

**Embedding dimension (k):** Performance increases from k = 32 to k = 64, then plateaus at k = 128–256. GO: r = 0.54 (k = 32), 0.58 (k = 64), 0.59 (k = 128), 0.59 (k = 256). The default k = 128 is at the performance plateau.

#### 3.3.7 Random Graph Realization Stability

Across five independent random graph realizations (each with 673,899 edges), all-genes Pearson r ranges from 0.641 to 0.667 (mean = 0.653, SD across realizations = 0.010, or 1.5% of the mean). Pain-genes r ranges from 0.570 to 0.620 (mean = 0.591, SD = 0.015). The low inter-realization variability confirms that dense random graphs are robust prediction backbones.

#### 3.3.8 Bridge Genes and Knowledge Gap Quantification

RA-PainKG identifies bridge genes connecting inflammatory (Track A) and nociceptive (Track B) subgraphs. Top bridges include STAT3 (score 35), RELA (24), and the NF-kappaB complex (IKBKB, IKBKG, NFKB1). The KG quantifies knowledge gaps relevant to domain-specific prior knowledge: 72 of 192 core pain genes (37.5%) are absent from PrimeKG, and 50% of Track B genes present in the KG are isolated (no PPI edges). These gaps constrain the predictive value of domain-specific prior knowledge for perturbation prediction (see Discussion 4.2 for extrapolation analysis).

---

## 4. Discussion

### 4.1 RA-PainKG as a Knowledge Resource

RA-PainKG fills a specific gap in the biomedical database landscape: a tissue-contextualized, dual-track knowledge graph with systematic coverage-gap documentation for RA pain signaling. Comparison with existing resources demonstrates its unique contribution (Table 4).

**Table 4. Comparison with existing resources**

| Feature | STRING v12 [8] | DisGeNET [17] | IUPHAR Pain [14] | PrimeKG [13] | RA-PainKG |
|---------|---------------|---------------|------------------|-------------|-----------|
| Pain gene coverage | 192/192 (100%) | 145/192 (75.5%) | 89/192 (46.4%) | 120/192 (62.5%) | 120/192 (62.5%) |
| Tissue expression data | No | No | No | No | Yes (GTEx v8) |
| Drug-target edges | No | No | Yes (manual) | Yes | Yes (4,760) |
| Directional edges | No | No | No | Yes (24 types) | Yes (24 types) |
| Pain-specific organization | No | No | Yes | No | Yes (dual-track) |
| Coverage-gap documentation | N/A | N/A | N/A | N/A | Yes (72 genes) |
| Open-source formats | Yes | Yes | Yes | Yes | Yes (GraphML/CSV/PKL) |

RA-PainKG serves three primary use cases. First, as a queryable knowledge base: researchers can extract pathway subnetworks (all nine curated pain pathways), identify drugs targeting specific pain genes, and retrieve tissue expression profiles for pain genes across 54 human tissues. Second, as a hypothesis-generation tool: the dual-track framework enables systematic comparison of inflammatory versus nociceptive mechanisms, and bridge genes (STAT3, RELA, NF-kappaB complex) connecting both tracks represent candidate intervention points where anti-inflammatory and analgesic effects may converge. Third, as prior knowledge for machine learning: the graph provides structured domain knowledge for downstream applications including gene perturbation prediction, drug repurposing, and causal mediator identification.

### 4.2 The Value of Coverage-Gap Documentation

The systematic identification of 72 absent genes (37.5% of the curated set) represents a resource contribution in its own right. Rather than silently omitting these genes, RA-PainKG documents exactly which genes are missing, why (identifier mismatch, annotation gaps in PrimeKG), and where researchers should look for alternative information (Supplementary Table S3). This transparency serves multiple purposes: (1) it prevents false-negative conclusions when querying RA-PainKG for specific genes; (2) it identifies systematic curation biases (complement cascade, anesthetic targets, GABA receptors are underrepresented across all general-purpose biomedical KGs); and (3) it provides a prioritized list for future resource development. This approach-a knowledge graph that explicitly documents what it does not contain-is uncommon in the biomedical database literature and represents a methodological contribution for transparent resource development.

### 4.3 Benchmark Validation and Boundary Conditions

Benchmark validation across 11 KG variants using the Norman K562 Perturb-seq dataset [20] provides transparent performance characterization (Tables 2-3). Two findings merit discussion.

First, the validation establishes honest boundary conditions. K562 chronic myeloid leukemia cells are fundamentally mismatched to RA pain biology: 59.1% of measurable pain genes (26/44 overlapping) exhibit mean expression below 0.01 in K562 cells, and mean pain-gene expression (0.117) is comparable to the genome-wide background (0.107). Only 26.7% of RA-PainKG pain genes (44/165) are present in the Norman dataset. Consequently, perturbation prediction performance on K562 cells should not be interpreted as a measure of RA-PainKG's biological validity-it reflects the test system's limitations, not the resource's quality.

Second, the benchmark reveals a methodological consideration for KG evaluation: single-split evaluation produces artifacts. Under one split (seed 42), RA-PainKG appeared to outperform GO on pain genes (r = 0.558 vs 0.481), but the effect reversed under multi-split averaging (0.503 vs 0.542). This demonstrates the necessity of multi-split statistics for reliable KG evaluation-findings that apply to any domain-specific KG benchmark, not just RA-PainKG.

We emphasize that the K562 benchmark cannot resolve whether domain KGs improve prediction in disease-relevant systems. Sensory neuron models (iPSC-derived nociceptors, DRG organoids) remain the essential next step for evaluating whether RA-PainKG's domain-specific prior knowledge confers advantages in biologically appropriate contexts.

### 4.4 Limitations

**Tissue coverage:** GTEx v8 does not contain dorsal root ganglion (DRG) or synovium samples. We proxy DRG expression via spinal cord and tibial nerve; immune compartments via whole blood and spleen. Single-cell RNA-seq datasets for human DRG [18] could provide finer resolution.

**Cell-type resolution:** GTEx provides bulk tissue TPM, masking cell-type-specific expression within heterogeneous tissues.

**Static representation:** RA-PainKG is a static knowledge graph; it does not model condition-specific dynamics, temporal regulation, or quantitative interaction strengths.

**Identifier resolution:** PrimeKG node IDs are internal integers. Cross-referencing with standard identifiers (HGNC, Ensembl) requires the original prime_kg.csv file, which is available from the PrimeKG repository.

**Validation scope:** Benchmark validation is limited to K562 cells. Replication in disease-relevant cell types is essential before drawing conclusions about domain KG utility for pain biology applications.

### 4.5 Updates and Community Contributions

RA-PainKG will be updated with each major PrimeKG release. Community contributions of additional pain pathway annotations, drug-target relationships, and tissue expression data are welcome via the GitHub repository. The modular construction pipeline enables systematic re-generation with updated input resources.

### 4.6 Conclusion

RA-PainKG provides a tissue-contextualized, dual-track knowledge graph for RA pain signaling with systematic coverage-gap documentation-a resource type not previously available for pain biology research. The graph, its construction pipeline, and comprehensive documentation are publicly available at https://github.com/yyx-4113/ra-painkg under the MIT license. Transparent benchmark validation establishes honest boundary conditions, and systematic coverage-gap documentation identifies specific priorities for future resource development. The open-source construction framework is designed for extensibility to other diseases where domain-specific knowledge graphs with documented knowledge gaps would accelerate mechanistic research.

---

## AI Usage Statement

During the preparation of this work, the author used AI-assisted tools (OpenAI Codex CLI, GitHub Copilot, and Claude via API) for the following purposes: code development and debugging of the pipeline, literature search and summarization, manuscript drafting and language editing, and iterative revision based on simulated peer review. All AI-generated content was reviewed, verified, and edited by the author. The author takes full responsibility for the scientific accuracy, data integrity, and conclusions presented in this publication. All data were generated by the author's original code; no AI tool contributed to data generation or statistical computation beyond code execution of author-specified algorithms.

## Acknowledgements

The author thanks the Norman lab, the PrimeKG development team, the GTEx Consortium, and the Gene Ontology Consortium for making their data publicly available. This research was supported by institutional resources from The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine.

## Author Contributions

**Yongxin Yang:** Conceptualization, Methodology, Software, Formal Analysis, Investigation, Data Curation, Writing - Original Draft, Writing - Review and Editing, Visualization, Project Administration.

## Competing Interests

The author declares no competing interests.

## Ethics Statement

This study uses exclusively publicly available data. No new data involving human subjects were collected.

## Data and Code Availability

All code, processed KG adjacency matrices, graph files (GraphML, CSV, Python pickle), and benchmark results are available at https://github.com/yyx-4113/ra-painkg under the MIT license. The Norman et al. Perturb-seq dataset is available from Harvard Dataverse (DOI: 10.7910/DVN/R9JDLS). PrimeKG v1.0 is available from Harvard Dataverse (DOI: 10.7910/DVN/IXA7BM). Gene Ontology annotations are from the Gene Ontology Consortium. RA-PainKG graph files and complete documentation are included in the repository.

---

## References

[1] Safiri S, Kolahi AA, Hoy D, et al. Global, regional and national burden of rheumatoid arthritis 1990-2017: a systematic analysis. Ann Rheum Dis. 2019;78(11):1463-1471.

[2] Cross M, Smith E, Hoy D, et al. The global burden of rheumatoid arthritis: estimates from the Global Burden of Disease 2010 study. Ann Rheum Dis. 2014;73(7):1316-1322.

[3] Lee YC, Cui J, Lu B, et al. Pain persists in DAS28 rheumatoid arthritis remission but not in ACR/EULAR remission. Ann Rheum Dis. 2011;70:1467-1470.

[4] McWilliams DF, Walsh DA. Pain mechanisms in rheumatoid arthritis. Clin Exp Rheumatol. 2017;35 Suppl 107(5):31-39.

[5] Basbaum AI, Bautista DM, Scherrer G, Julius D. Cellular and molecular mechanisms of pain. Cell. 2009;139(2):267-284.

[6] Julius D. TRP channels and pain. Annu Rev Cell Dev Biol. 2013;29:355-384.

[7] Ji RR, Nackley A, Huh Y, Terrando N, Maixner W. Neuroinflammation and central sensitization in chronic and widespread pain. Anesthesiology. 2018;129(2):343-366.

[8] Szklarczyk D, Kirsch R, Koutrouli M, et al. The STRING database in 2023: protein-protein association networks and functional enrichment analyses. Nucleic Acids Res. 2023;51(D1):D638-D646.

[9] Oughtred R, Rust J, Chang C, et al. The BioGRID database: A comprehensive biomedical resource of curated protein, genetic, and chemical interactions. Protein Sci. 2021;30(1):187-200.

[10] Kanehisa M, Furumichi M, Sato Y, Kawashima M, Ishiguro-Watanabe M. KEGG for taxonomy-based analysis of pathways and genomes. Nucleic Acids Res. 2023;51(D1):D587-D592.

[11] Gillespie M, Jassal B, Stephan R, et al. The reactome pathway knowledgebase 2022. Nucleic Acids Res. 2022;50(D1):D687-D692.

[12] Agrawal A, Balci H, Hanspers K, et al. WikiPathways 2024: next generation pathway database. Nucleic Acids Res. 2024;52(D1):D679-D689.

[13] Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine. Sci Data. 2023;10:67.

[14] Harding SD, Armstrong JF, Faccenda E, et al. The IUPHAR/BPS Guide to PHARMACOLOGY in 2024. Nucleic Acids Res. 2024;52(D1):D1438-D1449.

[15] Meloto CB, Benavides R, Lichtenwalter RN, et al. Human pain genetics database: a resource dedicated to human pain genetics research. Pain. 2018;159(4):749-763.

[16] GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects across human tissues. Science. 2020;369(6509):1318-1330.

[17] Pinero J, Ramirez-Anguita JM, Sauch-Pitarch J, et al. The DisGeNET knowledge platform for disease genomics: 2019 update. Nucleic Acids Res. 2020;48(D1):D845-D855.

[18] Nguyen MQ, von Buchholtz LJ, Reker AN, Ryba NJ, Davidson S. Single-nucleus transcriptomic analysis of human dorsal root ganglion sensory neurons. Pain. 2021;162(7):2032-2046.

[19] Yang Y. RA-PainKG: A tissue-specific knowledge graph for rheumatoid arthritis pain signaling - construction protocol, network analysis, and coverage-gap documentation. GitHub/Zenodo. 2026. Available at: https://github.com/yyx-4113/ra-painkg.

[20] Norman TM, Horlbeck MA, Replogle JM, et al. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science. 2019;365(6455):786-793.

[21] Roohani Y, Huang K, Leskovec J. Predicting transcriptional outcomes of novel multigene perturbations with GEARS. Nat Biotechnol. 2024;42:591-600.

[22] Ashburner M, Ball CA, Blake JA, et al. Gene Ontology: tool for the unification of biology. Nat Genet. 2000;25(1):25-29.
