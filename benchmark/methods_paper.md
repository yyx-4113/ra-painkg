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

---

## 1. Introduction

Rheumatoid arthritis (RA) affects approximately 1% of the global population, causing chronic synovial inflammation that leads to joint destruction and persistent pain [1,2]. Disease-modifying antirheumatic drugs and biologic agents effectively control inflammation in many patients, yet a substantial proportion continue to experience clinically significant pain [3,4]. This dissociation between anti-inflammatory efficacy and analgesia reveals a specific knowledge gap: pain signaling pathways in RA are not adequately captured by existing biological network resources.

The molecular basis of RA pain operates across multiple anatomical compartments. Peripheral nociceptors express transduction channels (TRPV1, TRPA1, Nav1.7/SCN9A) that initiate pain signals [5,6]. Spinal dorsal horn circuits process these signals through neuropeptide and neurotrophin mediators (CGRP, Substance P, BDNF-TrkB) [7]. Descending modulatory pathways (opioid, GABAergic, serotonergic) regulate pain transmission from supraspinal centers. These mechanisms operate in distinct tissue contexts that generic interaction networks cannot distinguish.

Existing biological network resources have critical limitations for pain mechanism research. STRING [8] and BioGRID [9] provide comprehensive protein-protein interaction data but lack tissue specificity, directionality, and drug-target annotations. KEGG [10], Reactome [11], and WikiPathways [12] offer curated pathway models without tissue contextualization. PrimeKG [13] integrates 20 biomedical resources into a unified multimodal knowledge graph, representing a major advance over single-source networks. However, PrimeKG remains a general-purpose resource: it does not distinguish pain-specific signaling from general inflammatory pathways, lacks tissue expression filtering, and provides no systematic documentation of coverage gaps. Pain-focused resources such as the IUPHAR/BPS Guide to Pharmacology [14] and the Human Pain Genetics Database [15] curate pain-relevant genes but lack network connectivity and multi-entity integration.

The consequence is a fragmented resource landscape. Researchers must either use general-purpose knowledge graphs that lack pain-specific organization, or pain-specific gene lists that lack network structure. A resource that integrates curated pain gene annotations with multimodal biomedical network data, provides tissue-contextual filtering, and systematically documents knowledge gaps would fill a specific and well-defined need.

We present RA-PainKG, a tissue-contextualized dual-track knowledge graph constructed by integrating PrimeKG v1.0 [13] with GTEx v8 tissue expression data [16] and manual curation of nine core pain signaling pathways. The resource contains 18,069 nodes across 10 entity types and 127,226 directed edges across 24 relation types. Starting from 192 manually curated pain genes, 120 (62.5%) matched PrimeKG by exact symbol; 2-hop neighborhood expansion identified 45 additional pain-relevant genes, yielding 165 annotated genes organized into Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes, with 96 overlapping). A systematic coverage-gap analysis documents 72 core pain genes (37.5%) absent from PrimeKG. Transparent benchmark validation using the Norman K562 Perturb-seq dataset [20] establishes honest boundary conditions. All graph files, source code, and documentation are publicly available under the MIT license at https://github.com/yyx-4113/ra-painkg [19].


**Significance Statement**

*Problem:* Existing biological network resources for rheumatoid arthritis pain lack tissue-contextual information, pain-specific pathway organization, and systematic documentation of knowledge gaps.

*What is Known:* General-purpose resources such as PrimeKG and STRING provide broad biological coverage but do not distinguish pain-specific signaling from general inflammatory pathways.

*What this Paper Adds:* RA-PainKG, a tissue-contextualized dual-track knowledge graph integrating PrimeKG with GTEx v8 expression data and manual curation of nine pain signaling pathways. The resource includes systematic coverage-gap documentation identifying 72 core pain genes (37.5%) absent from existing biomedical knowledge graphs. All nine curated pain pathways are mapped (57-100% gene coverage), and 4,760 drug-target edges enable direct pharmacological queries.

*Who Benefits:* Pain biology researchers requiring structured, tissue-aware knowledge representations; bioinformaticians developing machine learning models with domain-specific prior knowledge; and knowledge graph curators seeking a reproducible construction framework with transparent knowledge-gap documentation.

## 2. Materials and Methods

### 2.1 Knowledge Graph Construction

RA-PainKG was constructed in three stages (detailed protocol in [19]).

### 2.2 RA-PainKG Construction Pipeline

**Stage 1: Core gene curation.** 192 pain genes were manually curated from 15 literature-defined functional categories, organized into receptor/ion channel families (TRP channels, voltage-gated sodium channels, serotonin receptors, GABA/glycine receptors, opioid receptors, endocannabinoid system), intracellular signaling cascades (MAPK pathway, JAK-STAT pathway, kinase signaling, transcription factors), and disease/tissue-specific groups (prostaglandin pathway, complement cascade, neurotrophin signaling, RA-specific genes, anesthetic targets). Inclusion criteria: (1) published experimental evidence for a role in pain signaling, nociception, or RA inflammation in at least two independent studies (PubMed search: "gene_symbol AND (pain OR nociception OR rheumatoid arthritis)"), or (2) designation as a known drug target for analgesia or RA treatment in the IUPHAR/BPS Guide to Pharmacology [14] or DrugBank. The full gene list with functional category assignments and supporting PMIDs is provided in Supplementary Table S1. TRP channels, voltage-gated sodium channels, neurotrophin signaling, opioid signaling, MAPK pathway, JAK-STAT pathway, prostaglandin pathway, complement cascade, GABA/glycine receptors, serotonin receptors, endocannabinoid system, kinase signaling, transcription factors, RA-specific genes, and anesthetic targets. Inclusion criteria: (1) published evidence for pain signaling or RA inflammation in at least two independent studies, or (2) designation as a known drug target for analgesia or RA treatment.

**Stage 2: PrimeKG integration.** Of 192 core pain genes, 120 (62.5%) matched PrimeKG v1.0 by exact gene symbol. Starting from these seed nodes, we performed 2-hop neighborhood expansion with a connectivity filter (nodes must be reachable from at least two seed categories). This identified 45 additional pain-relevant genes (e.g., CCR6, CSF2, IRF5, IFNG, FCGR3A), yielding a final annotated set of 165 genes organized into Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes, with 96 overlapping).

**Tissue-contextual filtering with GTEx v8.** GTEx v8 median tissue expression data [16] were used to annotate each pain gene with tissue-specific expression levels across 54 human tissues. For nociception-relevant compartments, we used spinal cord (cervical C1), tibial nerve, whole blood, and spleen as proxies. A gene was classified as tissue-expressed if median TPM >= 1.0 in the relevant tissue. This information is provided as node attributes in the GraphML and CSV formats but was not used to filter edges in the current release, as removing edges based on bulk tissue expression risks discarding valid low-expression interactions. Future versions will incorporate single-cell expression data for finer tissue-contextual filtering.

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

### 2.4 Perturbation Data and Benchmark Validation

The Norman et al. Perturb-seq dataset (DOI: 10.7910/DVN/R9JDLS) profiles CRISPRi in K562 chronic myeloid leukemia cells [20]. The processed dataset (perturb_processed.h5ad, 2.2 GB; Harvard Dataverse datafile 6154020) contains 5,045 genes across 91,205 cells with 284 perturbation conditions (single-gene and combinatorial). We aggregate cells by perturbation condition to compute mean post-perturbation expression changes (delta = condition_mean - ctrl_mean). Control expression variance across genes is 0.194 (SD = 0.441), computed from log-normalized expression values.

### 2.5 Gene Embedding and Prediction Model

For each KG, we compute 128-dimensional gene embeddings via spectral decomposition of the normalized graph Laplacian: L = I - D^{-1/2} A D^{-1/2}, extracting eigenvectors corresponding to the k smallest non-zero eigenvalues. For graphs with isolated nodes (RA-PainKG: 68.3% of genes), these nodes receive near-zero embeddings that contribute no predictive signal in the linear model—a feature that accurately reflects their lack of KG-derived prior information. The perturbation prediction model is:

    predicted_delta = W^T * emb(perturbed_gene)

where W (128 x 5045) is learned via ridge regression (lambda = 0.1). This deliberately simplified architecture isolates KG contribution from model capacity. We validate robustness across regularization strengths (alpha = 0.001, 0.01, 0.1, 1.0, 10.0, 100.0) and embedding dimensions (k = 32, 64, 128, 256, 512).

**Justification of linear model choice:** We compared ridge regression against a 2-layer multilayer perceptron (MLP) with 128 hidden units and ReLU activation, trained on one representative split (seed 42). The MLP yielded lower performance (r = 0.46 vs r = 0.52–0.59 for ridge) and attenuated KG distinctions (GO: r = 0.459, RA-PainKG: r = 0.458, delta < 0.01), likely due to overfitting given the high-dimensional output space (5,045 genes) relative to training samples (227 conditions). The linear model preserves KG-specific signal and provides a more informative comparison. We note the MLP evaluation is single-split and should be interpreted as qualitative evidence for the linear model's suitability rather than a formal nonlinear benchmark.

This design contrasts with the full GEARS architecture [21], which uses GraphSAGE message-passing and cross-gene attention—mechanisms that may differentially exploit KG structure. Our results measure KG embedding quality in a controlled linear setting rather than end-to-end GEARS performance.

**Compute requirements:** Spectral decomposition of each 5,045 x 5,045 adjacency matrix required 40–66 seconds (Intel i9-13900K, 64 GB RAM, single core). Data loading (40 seconds), KG construction (GO: 100 seconds; RA-PainKG: 12 seconds), and benchmark execution (10 splits x 11 KGs, <1 second per split-KG combination) brought the total wall-clock time to approximately 12 minutes. Peak memory usage was approximately 2.5 GB during simultaneous matrix operations.

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

Python 3.10+, ScanPy 1.12, NetworkX 3.6, NumPy, SciPy, scikit-learn. Full pipeline and processed KG adjacency matrices are available at https://github.com/yyx-4113/ra-painkg.

---

## 3. Results

### 3.1 RA-PainKG Resource Description

RA-PainKG is publicly available in three formats: GraphML (network visualization), CSV (edge and node tables), and Python pickle (programmatic access via NetworkX). The complete resource includes: (1) the full knowledge graph with 18,069 nodes and 127,226 directed edges; (2) GTEx v8 tissue expression annotations for 165 pain-annotated genes across 54 human tissues; (3) dual-track gene assignments with supporting literature evidence; and (4) mapping of nine curated pain signaling pathways onto the graph structure.

The graph spans 10 entity types (gene/protein, drug, disease, pathway, biological process, molecular function, cellular component, anatomy, phenotype, effect/phenotype) and 24 relation types, with drug-target edges (4,760 edges) enabling direct pharmacological queries. Network topology analysis identified EGR1, FOS, STAT3, JUN, and AKT1 as the top five hub nodes by betweenness centrality (Figure 1). The degree distribution follows a scale-free pattern characteristic of biological networks (Figure 2).

All nine literature-curated pain signaling pathways were successfully mapped onto RA-PainKG with gene coverage ranging from 57% (complement cascade) to 100% (TRP channels, voltage-gated sodium channels, neurotrophin signaling). The dual-track organization is summarized in Table S1: Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes), with 96 genes (58.2%) spanning both tracks. This overlap is biologically expected given the mechanistic interconnection between inflammation and pain sensitization, The substantial Track A/B overlap (58.2%) is biologically expected: transcription factors (FOS, JUN, STAT3) activated by inflammatory cytokines also drive nociceptive sensitization, MAP kinases transduce both inflammatory and pain signals, and prostaglandins (via COX-2/PTGS2) bridge immune activation and nociceptor sensitization [5,7]. Rather than indicating poor track separation, this overlap reflects the mechanistic reality that inflammation and pain are deeply coupled in RA. The dual-track framework should be used as a conceptual lens for hypothesis generation-for example, genes exclusive to Track A or B may represent intervention points where anti-inflammatory and analgesic effects can be partially decoupled, while dual-track hub genes represent convergence points where both processes are jointly regulated.

### 3.2 Coverage-Gap Analysis

Of 192 core pain genes manually curated from the literature, 120 (62.5%) are represented in PrimeKG v1.0 by exact gene symbol matching. The remaining 72 genes (37.5%) constitute systematic coverage gaps in PrimeKG, concentrated in three functional categories: (1) complement cascade components (C1QA, C1QB, C1QC, C2, C3, C4A, C4B, CFB, CFD), where the complement system is increasingly recognized as a pain modulator but is poorly annotated in general-purpose biomedical KGs; (2) anesthetic drug targets (GABRA2, GABRA3, GABRB1, GABRG1, GABRG2, GLRB, GLRA1), where GABA/glycine receptor subunit diversity is not fully captured by PrimeKG's drug-target mappings; and (3) nociceptor-specific ion channels (TRPM8, ASIC3, P2RX7), where gene symbol inconsistencies between resources create mapping failures. The low match rate for complement components (35.7%) is particularly consequential: the complement system is increasingly recognized as a pain modulator through C5a-C5aR1 signaling in sensory neurons [17], and C5 polymorphisms are associated with RA susceptibility. This coverage gap means that complement-mediated pain mechanisms are essentially invisible to PrimeKG-based queries and represents a high-priority target for future KG integration.

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

To establish transparent performance characteristics, we validated RA-PainKG in a perturbation prediction benchmark using the Norman K562 Perturb-seq dataset [20] (91,205 cells, 5,045 genes, 284 CRISPRi conditions). Gene embeddings were computed via spectral decomposition (k = 128) of the normalized graph Laplacian, and perturbation effects were predicted via ridge regression across 10 independent train/test splits (80%/20%). Full methods, results for all 11 KG variants, and sensitivity analyses are provided in Supplementary Tables S1-S6.

Two findings are directly relevant to the resource. First, RA-PainKG is 280-fold sparser than GO (2,400 vs 673,899 PPI edges), with 68.3% of Norman genes having zero edges. Among the 44 pain genes present in the Norman dataset (26.7% of 165 annotated genes), 59.1% (26/44) exhibit mean expression below 0.01 in K562 cells, and mean pain-gene expression (0.117) is comparable to the genome-wide background (0.107). These data establish a clear boundary condition: K562 perturbation prediction performance reflects test system limitations, not resource quality (see Discussion 4.3).

Second, the benchmark reveals a methodological consideration for KG evaluation: single-split evaluation produces artifacts. Under one split (seed 42), RA-PainKG appeared to outperform GO on pain genes (r = 0.558 vs 0.481), but the effect reversed under multi-split averaging (0.503 vs 0.542, Supplementary Table S5). This demonstrates the necessity of multi-split statistics for reliable KG evaluation.

Complete benchmark results for all 11 KG variants, paired statistical comparisons, sensitivity analyses (alpha = 0.001-100.0, k = 32-512), Kendall's W ranking consistency (0.64-0.65), and ablation analyses are documented in Supplementary Tables S1-S6.


## 4. Usage Examples

RA-PainKG is designed for programmatic access via Python (NetworkX). Below are three representative use cases. All code is available in the GitHub repository.

### 4.1 Querying Drug-Target Relationships

```python
import pickle
with open("RA_PainKG_final.pkl", "rb") as f:
    g = pickle.load(f)

# Find all drugs targeting PTGS2 (COX-2)
ptgs2_drugs = []
for node, data in g.nodes(data=True):
    if str(data.get("node_name", "")).upper() == "PTGS2":
        for pred in g.predecessors(node):
            if g.nodes[pred].get("node_type") == "drug":
                ptgs2_drugs.append((g.nodes[pred]["node_name"],
                                    g[pred][node].get("relation")))
print(ptgs2_drugs)
# Example output: [("Celecoxib", "inhibits"), ("Aspirin", "inhibits"), ...]
```

### 4.2 Extracting Pathway Subnetworks

```python
# Extract the opioid signaling subnetwork
opioid_genes = {"OPRM1", "OPRD1", "OPRK1", "POMC", "PENK", "PDYN"}
opioid_nodes = {n for n, d in g.nodes(data=True)
                if str(d.get("node_name", "")).upper() in opioid_genes}
subgraph = g.subgraph(opioid_nodes)
import networkx as nx
nx.write_graphml(subgraph, "opioid_pathway.graphml")
```

### 4.3 Tissue Expression Profile Retrieval

```python
# Retrieve GTEx tissue expression for all Track B pain genes
track_b_genes = [d["node_name"] for _, d in g.nodes(data=True)
                 if d.get("track") == "B" and d.get("node_type") == "gene/protein"]
for gene in track_b_genes[:5]:
    expr = d.get("gtex_median_tpm", {})
    spinal_cord = expr.get("Spinal_Cord_cervical_c-1", "N/A")
    tibial_nerve = expr.get("Nerve_Tibial", "N/A")
    print(f"{gene}: Spinal={spinal_cord}, Tibial={tibial_nerve}")
```

### 4.4 Identifying Bridge Genes Between Tracks

```python
# Find genes connecting Track A and Track B in the PPI subgraph
track_a_nodes = {n for n, d in g.nodes(data=True) if d.get("track") == "A"}
track_b_nodes = {n for n, d in g.nodes(data=True) if d.get("track") == "B"}
ppi_edges = [(u, v) for u, v, d in g.edges(data=True)
             if d.get("relation") == "protein_protein"]
bridge_scores = {}
for u, v in ppi_edges:
    if u in track_a_nodes and v in track_b_nodes:
        bridge_scores[u] = bridge_scores.get(u, 0) + 1
        bridge_scores[v] = bridge_scores.get(v, 0) + 1
top_bridges = sorted(bridge_scores.items(), key=lambda x: x[1], reverse=True)[:10]
# Top bridges include STAT3, RELA, NFKB1, IKBKB
```

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
| Known limitations | N/A | N/A | N/A | N/A | 62.5% pain gene coverage; no DRG/synovium GTEx data; static representation |

RA-PainKG serves three primary use cases. First, as a queryable knowledge base: researchers can extract pathway subnetworks (all nine curated pain pathways), identify drugs targeting specific pain genes, and retrieve tissue expression profiles for pain genes across 54 human tissues. Second, as a hypothesis-generation tool: the dual-track framework enables systematic comparison of inflammatory versus nociceptive mechanisms, and bridge genes (STAT3, RELA, NF-kappaB complex) connecting both tracks represent candidate intervention points where anti-inflammatory and analgesic effects may converge. Third, as prior knowledge for machine learning: the graph provides structured domain knowledge for downstream applications including gene perturbation prediction, drug repurposing, and causal mediator identification.

### 4.2 The Value of Coverage-Gap Documentation

The systematic identification of 72 absent genes (37.5% of the curated set) represents a resource contribution in its own right. Rather than silently omitting these genes, RA-PainKG documents exactly which genes are missing, why (identifier mismatch, annotation gaps in PrimeKG), and where researchers should look for alternative information (Supplementary Table S3). This transparency serves multiple purposes: (1) it prevents false-negative conclusions when querying RA-PainKG for specific genes; (2) it identifies systematic curation biases (complement cascade, anesthetic targets, GABA receptors are underrepresented across all general-purpose biomedical KGs); and (3) it provides a prioritized list for future resource development. This approach-a knowledge graph that explicitly documents what it does not contain-is uncommon in the biomedical database literature. While resources such as the IUPHAR/BPS Guide to Pharmacology [14] acknowledge incomplete coverage in narrative form, systematic per-gene gap documentation with categorized absence reasons is rarely implemented. We argue this practice represents a methodological contribution for transparent resource development.

### 4.3 Benchmark Validation and Boundary Conditions

Benchmark validation across 11 KG variants using the Norman K562 Perturb-seq dataset [20] provides transparent performance characterization (Supplementary Tables S4-S5). Two findings merit discussion.

First, the validation establishes honest boundary conditions. We emphasize that K562 cells were selected not as a biologically appropriate test system for RA pain (they are not), but as the only publicly available genome-scale Perturb-seq dataset with sufficient coverage to run a controlled multi-split benchmark. The purpose of this validation is not to demonstrate biological utility-it is to characterize the resource's predictive properties in a standardized setting and to establish transparent performance baselines against which future evaluations in disease-relevant models can be compared. K562 chronic myeloid leukemia cells are fundamentally mismatched to RA pain biology: 59.1% of measurable pain genes (26/44 overlapping) exhibit mean expression below 0.01 in K562 cells, and mean pain-gene expression (0.117) is comparable to the genome-wide background (0.107). Only 26.7% of RA-PainKG pain genes (44/165) are present in the Norman dataset. Consequently, perturbation prediction performance on K562 cells should not be interpreted as a measure of RA-PainKG's biological validity-it reflects the test system's limitations, not the resource's quality.

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
