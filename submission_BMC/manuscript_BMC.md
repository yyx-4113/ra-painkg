# RA-PainKG: a tissue-contextualized knowledge graph for rheumatoid arthritis pain signaling with transparent benchmark characterization

**Yongxin Yang**^1,^✉

^1^ Department of Anesthesiology, The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou 350003, Fujian, China

✉ Corresponding author: Yongxin Yang, 960856791@qq.com

ORCID: 0009-0004-9698-6552

## Abstract

**Background:** Rheumatoid arthritis (RA) pain often persists despite adequate inflammation control, yet existing biological network resources treat RA as a single disease entity without separating pain-specific signaling from general inflammatory pathways or providing tissue context for nociception-relevant compartments. We aimed to build a tissue-contextualized knowledge graph that integrates curated pain gene annotations with multimodal biomedical network data and transparently documents gene recovery.

**Results:** We present RA-PainKG, a directed knowledge graph integrating PrimeKG v1.0, GTEx v8 tissue expression across 54 human tissues, and manual curation of 192 pain-relevant genes in 20 functional categories spanning nine pain signaling pathways. Of 192 curated genes, 188 (97.9%) are present in the final graph (189/192, 98.4%, matched PrimeKG symbols exactly; the remainder are identifier artifacts). A 2-hop expansion added 45 genes, yielding 165 annotated genes organized as Track A (immune-inflammation, 106) and Track B (nociception, 122; 96 overlapping). The graph comprises 18,069 nodes (10 types) and 127,226 directed edges (24 types), with 4,760 drug–target edges. Betweenness centrality identified EGR1, FOS, STAT3, AKT1, and SRC as top hubs. All nine pathways mapped at 57–100% gene coverage. Benchmark validation across 11 knowledge-graph variants using the Norman K562 Perturb-seq dataset established transparent boundary conditions.

**Conclusions:** RA-PainKG provides a tissue-contextualized, dual-track knowledge graph for RA pain with transparent recovery and gap documentation. It is released in GraphML, CSV, and pickle formats with complete source code, serving as structured prior knowledge for pain mechanism research and machine-learning applications.

**Keywords:** knowledge graph; rheumatoid arthritis; pain signaling; PrimeKG; GTEx; tissue-specific; network biology

## Background

Rheumatoid arthritis (RA) affects approximately 0.5–1.0% of adults worldwide, causing chronic synovial inflammation, joint destruction, and persistent pain [1,2]. Disease-modifying antirheumatic drugs and biologics control inflammation in many patients, yet a substantial proportion continue to experience clinically significant pain [3,4]. This dissociation reveals a specific knowledge gap: pain signaling pathways in RA are not adequately captured by existing biological network resources.

The molecular basis of RA pain spans multiple anatomical compartments. Peripheral nociceptors express transduction channels (TRPV1, TRPA1, Nav1.7/SCN9A) [5,6]; spinal dorsal horn circuits process these signals through neuropeptide and neurotrophin mediators (CGRP, Substance P, BDNF–TrkB) [7]; descending modulatory pathways (opioid, GABAergic, serotonergic) regulate transmission from supraspinal centers. These mechanisms operate in distinct tissue contexts that generic interaction networks cannot distinguish.

Existing resources have critical limitations for pain mechanism research. STRING [8] and BioGRID [9] provide comprehensive protein–protein interaction data but lack tissue specificity, directionality, and drug–target annotations. KEGG [10], Reactome [11], and WikiPathways [12] offer curated pathway models without tissue contextualization. PrimeKG [13] integrates 20 biomedical resources into a unified multimodal knowledge graph, yet remains a general-purpose resource: it does not separate pain-specific signaling from inflammatory pathways, lacks tissue-expression filtering, and provides no systematic mapping of curated pain gene sets. Pain-focused resources such as the IUPHAR/BPS Guide to Pharmacology [14] and the Human Pain Genetics Database [15] curate pain-relevant genes, while DisGeNET [16] provides gene–disease associations, but these lack network connectivity and multi-entity integration.

The consequence is fragmentation: researchers must choose between general-purpose knowledge graphs that lack pain-specific organization or pain-specific gene lists that lack network structure. A resource integrating curated pain gene annotations with multimodal network data, providing tissue-contextual filtering and transparently documenting recovery and residual gaps, would fill a well-defined need. We present RA-PainKG, a tissue-contextualized dual-track knowledge graph integrating PrimeKG v1.0 [13] with GTEx v8 tissue-expression data [17] and manual curation of 192 pain-relevant genes in 20 functional categories spanning nine core pain signaling pathways.

## Methods

### Knowledge graph construction

RA-PainKG was constructed in three stages.

**Stage 1: Core gene curation.** 192 pain genes were manually curated from 20 literature-defined functional categories: nociceptor transduction channels, voltage-gated sodium and calcium channels, neuropeptide signaling, neurotrophin signaling, the opioid system, inflammatory cytokines and receptors, MAPK, JAK–STAT, and NF-κB pathways, the prostaglandin pathway, complement cascade, GABA/glycine and serotonin receptors, the endocannabinoid system, kinase signaling, transcription factors, RA-specific genes, and anesthetic targets. These 20 categories were organized into nine core pain signaling pathways: (1) the TRPV1–CGRP nociceptor axis, (2) the Nav1.7 sodium-channel action-potential axis, (3) the TNFα–NGF inflammatory pain axis, (4) the opioid endogenous-analgesia axis, (5) the JAK–STAT RA-inflammatory axis, (6) the MAPK pain-sensitization axis, (7) the complement neuroimmune axis, (8) GABAergic descending inhibition, and (9) the prostaglandin inflammatory-mediator axis. These are enumerated explicitly to aid reproducibility. Inclusion required (1) published experimental evidence for a role in pain signaling, nociception, or RA inflammation in at least two independent studies (PubMed: "gene_symbol AND (pain OR nociception OR rheumatoid arthritis)"), or (2) designation as a known analgesic or RA drug target in the IUPHAR/BPS Guide to Pharmacology [14] or DrugBank. The full list with functional assignments and PMIDs is in Supplementary Table S1.

**Stage 2: PrimeKG integration and track assignment.** Of 192 curated genes, 189 (98.4%) matched PrimeKG v1.0 node symbols by exact, case-insensitive matching; 188 of 192 are present in the final RA-PainKG graph by exact symbol (one matched gene, ADRA2B, was not retained during construction). The pipeline identified 190 seed gene/protein nodes; 120 of the 192 curated genes were retained as the curated core of the annotated set. A 2-hop neighborhood expansion with a connectivity filter (nodes reachable from at least two seed categories) added 45 additional pain-relevant genes (e.g., CCR6, CSF2, IRF5, IFNG, FCGR3A), yielding a final annotated set of 165 genes (120 curated + 45 expansion). Of the 192 curated genes, 72 were not retained in the dual-track annotated set; 68 of these are present in the graph but were not assigned dual-track annotations, and 4 are identifier or construction artifacts (ACPA is a non-gene autoantibody marker; NAPE-PLD and RANKL are present under the aliases NAPEPLD and TNFSF11; ADRA2B is a construction artifact. All four are resolved in the Recovery and residual-gap analysis). Among the 165 annotated genes, 106 were assigned to Track A (immune-inflammation), 122 to Track B (nociception–pain transduction), with 96 in both; 33 annotated genes were assigned to neither track pending further curation.

**Tissue-contextual filtering.** GTEx v8 median tissue-expression data [17] annotated each pain gene across 54 human tissues. For nociception-relevant compartments we used spinal cord (cervical C1), tibial nerve, whole blood, and spleen as proxies. A gene was classified as tissue-expressed at median TPM ≥ 1.0, following standard GTEx thresholds [17]. These annotations are node attributes in the GraphML and CSV formats but were not used to filter edges in the current release, because removing edges on bulk tissue expression risks discarding valid low-expression interactions; future versions will incorporate single-cell data.

**Stage 3: Edge integration.** All PrimeKG edge types were integrated. The full graph contains 127,226 directed edges across 24 relation types, comprising 28,972 protein–protein interaction (PPI) edges and 98,254 edges of other types (pathway, biological process, anatomy, disease, phenotype, and drug–target); 4,760 are drug–target edges. The 165 annotated pain genes are labeled as nodes carrying dual-track and tissue-expression attributes, but the graph integrates the entire PrimeKG edge set rather than only edges incident to those genes. For benchmarking, a PPI-only variant retaining 2,400 edges among the annotated genes was used (see Perturbation data and benchmark validation). Only 44 of 165 annotated genes (26.7%) overlap the Norman K562 Perturb-seq gene vocabulary (Supplementary Table S6).

### Recovery and residual-gap analysis

A systematic recovery analysis (1) matched all 192 curated genes to PrimeKG gene/protein nodes by exact, case-insensitive HGNC symbol; (2) categorized unmatched genes by pathway and attempted alias resolution (e.g., NAPE-PLD→NAPEPLD, RANKL→TNFSF11); and (3) documented, for each unrecovered gene, the likely reason (genuine absence vs. symbol/alias mismatch). The recovery map is Supplementary Table S3.

For benchmark validation, gene–gene adjacency matrices for 5,045 Norman genes were computed across 11 knowledge-graph variants in three factor categories. (A) Density factor: GO-BP (673,899 edges, density 0.0265), five random realizations, GO-painCentric (edges with ≥1 pain-gene endpoint, 121,543 edges, density 0.0048), RA-PainKG (2,400 PPI edges, density 0.00009), and an Identity matrix. (B) Domain specificity factor: RA-PainKG gene nodes (type "gene/protein") extracted and HGNC-matched, retaining only PPI edges; the pain gene pool for GO-painCentric defined as the 44 pain-annotated genes present in the Norman vocabulary; of 5,045 Norman genes, 1,600 (31.7%) have ≥1 edge in RA-PainKG. (C) Structural topology factor (ablations): RA-PainKG-degPreserved (degree-preserving rewiring) and GO-painCentric tested whether edge identity or degree distribution drives performance. STRING PPI v12 was the 11th variant but yielded negligible predictive signal (overall Pearson r = 0.0003; pain-gene subset r = 0.0008), attributed to ENSP-to-symbol mapping ambiguity at the 5,045-gene scale.

### Perturbation data and benchmark validation

The Norman et al. Perturb-seq dataset (DOI: 10.7910/DVN/R9JDLS) profiles CRISPRi in K562 chronic myeloid leukemia cells [18]. The processed file (perturb_processed.h5ad, 2.2 GB; Harvard Dataverse datafile 6154020) contains 5,045 genes across 91,205 cells with 284 perturbation conditions. We aggregate cells by condition to compute mean post-perturbation expression changes (delta = condition_mean − ctrl_mean); control expression variance is 0.194 (SD 0.441) from log-normalized values.

For validation, 128-dimensional gene embeddings were computed via spectral decomposition of the normalized graph Laplacian (k = 128) for each KG. Perturbation effects were predicted by ridge regression (λ = 0.1) across 10 independent train/test splits (80%/20%). This linear architecture isolates KG contribution from model capacity. Paired t-tests with Bonferroni correction (α = 0.01, m = 5) and Kendall's W ranked consistency were used for comparison. Sensitivity analyses for regularization (α = 0.001–100.0) and embedding dimension (k = 32–512) confirmed robustness. K562 pain-gene expression was quantified for all 44 pain-annotated genes. Full methods, including spectral decomposition details, nonlinear model comparison (MLP vs ridge), GEARS architecture comparison [19], evaluation protocol, and power analysis, are in Supplementary Methods.

### Implementation and AI-use disclosure

Python 3.10+, ScanPy 1.12, NetworkX 3.6, NumPy, SciPy, and scikit-learn were used; total compute was approximately 12 minutes (Intel i9-13900K, 64 GB RAM). Full pipeline and processed data are at https://github.com/yyx-4113/ra-painkg. During manuscript preparation the author used AI-assisted tools (OpenAI Codex CLI, GitHub Copilot, and Claude via API) for code development, literature search, and language editing. All AI-generated content was reviewed and verified by the author, who takes full responsibility for scientific accuracy, data integrity, and conclusions. No AI tool contributed to data generation or statistical computation beyond executing author-specified algorithms.

## Results

### RA-PainKG resource description

RA-PainKG is publicly available in GraphML, CSV, and Python pickle (NetworkX) formats. The resource includes (1) the full graph (18,069 nodes, 127,226 directed edges); (2) GTEx v8 tissue-expression annotations for 165 pain-annotated genes across 54 tissues; (3) dual-track gene assignments with literature evidence; and (4) mapping of nine curated pain pathways onto the graph.

The graph spans 10 entity types (gene/protein, drug, disease, pathway, biological process, molecular function, cellular component, anatomy, phenotype, and exposure) and 24 relation types; 4,760 drug–target edges enable direct pharmacological queries. Betweenness centrality identified EGR1, FOS, STAT3, AKT1, and SRC as the top five hubs (Figure 1); the degree distribution follows a scale-free pattern (Figure 2).

All nine curated pathways mapped onto RA-PainKG at 57% (complement cascade) to 100% (TRP channels, voltage-gated sodium channels, neurotrophin signaling) gene coverage. The 165 annotated genes span 20 functional categories (Supplementary Table S1). Track A comprises 106 genes and Track B 122, with 96 (58.2%) overlapping both (a further 33 annotated genes were assigned to neither track and are pending further curation). This substantial overlap is biologically expected: transcription factors (FOS, JUN, STAT3) activated by inflammatory cytokines also drive nociceptive sensitization, MAP kinases transduce both inflammatory and pain signals, and prostaglandins (via COX-2/PTGS2) bridge immune activation and nociceptor sensitization [5,7]. The dual-track framework is a conceptual lens for hypothesis generation: genes exclusive to one track may mark intervention points where anti-inflammatory and analgesic effects partially decouple, whereas dual-track hubs are convergence nodes.

### Recovery and residual-gap analysis

Of 192 curated genes, 189 (98.4%) matched PrimeKG symbols exactly; 188 of 192 are present in the final graph by exact symbol. Applying alias resolution, all 192 curated entries are represented in PrimeKG: NAPE-PLD and RANKL are present under the HGNC symbols NAPEPLD and TNFSF11, respectively, and ADRA2B is present but was not retained in the final graph during construction. ACPA is an autoantibody marker rather than a gene symbol. No curated gene is therefore genuinely absent from the underlying knowledge base; the only residual items are (i) one construction artifact (ADRA2B, re-includable in a future release) and (ii) identifier/alias notes (ACPA; NAPE-PLD→NAPEPLD; RANKL→TNFSF11). The principal added value of RA-PainKG is therefore not the recovery of absent genes, but the organization, tissue contextualization, and transparent annotation of an already well-covered gene set.

A secondary structural asymmetry remains. Within the protein–protein interaction (PPI) subgraph induced by the 165 annotated genes (780 PPI edges), 24.6% of Track B genes (30/122) and 17.9% of Track A genes (19/106) have no PPI edges. Nociception-specific prior knowledge is thus sparser in direct connectivity than inflammation-specific prior knowledge. This gap should be a target for future edge curation.

### Benchmark validation

Validation used the Norman K562 Perturb-seq dataset [18] (91,205 cells, 5,045 genes, 284 CRISPRi conditions). Embeddings via spectral decomposition (k = 128) and ridge regression across 10 splits (80%/20%) yielded full results in Supplementary Tables S1–S6.

Two findings are relevant. First, RA-PainKG is 280-fold sparser than GO (2,400 vs 673,899 PPI edges in their respective benchmark PPI variants), with 68.3% of Norman genes having zero edges. Among 44 pain genes measurably expressed in Norman (26.7% of 165 annotated), 59.1% (26/44) show mean K562 expression below 0.01, and mean pain-gene expression (0.117) is comparable to the genome-wide background (0.107). These data establish that K562 performance reflects test-system limitations, not resource quality (see Discussion).

Second, the benchmark reveals a methodological consideration: single-split evaluation produces artifacts. Under one split (seed 42), RA-PainKG appeared to outperform GO on pain genes (r = 0.558 vs 0.481), but the effect reversed under multi-split averaging (0.503 vs 0.542, Supplementary Table S5). Multi-split statistics are therefore needed for reliable knowledge-graph evaluation.

## Discussion

### RA-PainKG as a knowledge resource

RA-PainKG fills a specific gap: a tissue-contextualized, dual-track knowledge graph with transparent recovery and gap documentation for RA pain signaling (Table 1). It recovers 188/192 (97.9%) of curated pain genes, maps all nine pathways (57–100% coverage), and provides 4,760 drug–target edges. Comparator coverage (IUPHAR Pain, DisGeNET) was computed by querying each resource for the same 192-gene set (Supplementary Methods).

RA-PainKG serves three use cases: (1) a queryable knowledge base for extracting pathway subnetworks, identifying drugs targeting specific pain genes, and retrieving tissue-expression profiles across 54 tissues; (2) a hypothesis-generation tool where the dual-track framework compares inflammatory versus nociceptive mechanisms and bridge genes (STAT3, RELA, NF-κB complex) mark candidate intervention points; and (3) structured prior knowledge for machine learning, including gene perturbation prediction and drug-repurposing pipelines.

### Value of transparent recovery and gap documentation

Systematic documentation of which curated genes are recovered, and the small residual set that is not, is a contribution in itself. Rather than assuming completeness, RA-PainKG documents exactly which genes are present, which are identifier/symbol artifacts (ACPA, NAPE-PLD, RANKL), and which were present in PrimeKG but not retained (ADRA2B). This transparency prevents false-negative conclusions when querying the graph, surfaces the genuine asymmetry that nociception-specific genes have sparser PPI connectivity, and provides a prioritized list for future development. A knowledge graph that explicitly documents what it does and does not contain is rarely implemented; resources such as the IUPHAR/BPS Guide to Pharmacology [14] acknowledge incomplete coverage narratively, but systematic per-gene recovery documentation with categorized absence reasons has few precedents.

### Benchmark validation and boundary conditions

Benchmark validation across 11 KG variants [18] provides transparent performance characterization (Supplementary Tables S4–S5). K562 cells were selected not as a biologically appropriate test system for RA pain (they are not), but as the most thoroughly characterized publicly available genome-scale Perturb-seq dataset with sufficient perturbation diversity for multi-split benchmarking. The purpose is to characterize the resource's predictive properties in a standardized setting and establish baselines against which future disease-relevant evaluations can be compared. K562 cells are fundamentally mismatched to RA pain biology: 59.1% of measurable pain genes show mean expression below 0.01, and only 26.7% of RA-PainKG pain genes (44/165) are measurably expressed in Norman. Perturbation-prediction performance on K562 should therefore not be interpreted as a measure of RA-PainKG's biological validity. It reflects test-system limitations.

The benchmark also shows that single-split evaluation produces artifacts (seed 42: RA-PainKG r = 0.558 vs GO 0.481; multi-split average: 0.503 vs 0.542). This argues for multi-split statistics in knowledge-graph evaluation, and it applies to any domain-specific KG benchmark. The multi-split comparison is not directly comparable across knowledge graphs, because RA-PainKG was evaluated on a 265-gene vocabulary while GO and STRING were evaluated on a 2,000-gene vocabulary. The appropriate reference is the within-vocabulary null. Note also that RA-PainKG's 265-gene benchmark vocabulary is drawn entirely from its own construction. It comprises all 165 dual-track annotated genes plus 100 additional RA-PainKG genes and contains no external validation genes (Supplementary Table S6). This benchmark is therefore an in-construction sanity check rather than an independent external evaluation, which limits claims of external generalizability. Within the 265-gene vocabulary, random graphs and a degree-preserving random rewiring of RA-PainKG both matched or exceeded RA-PainKG's predictive performance (random vs RA-PainKG Δr = +0.115, p < 0.001; RA-PainKG vs degree-preserved Δr = +0.005, p = 0.83; Supplementary Table S4). RA-PainKG therefore confers no predictive advantage over a structureless or degree-matched null on this task. We report this transparently as a boundary condition, not as evidence of resource quality.

The K562 benchmark cannot resolve whether domain KGs improve prediction in disease-relevant systems. Sensory neuron models (iPSC-derived nociceptors, DRG organoids) remain the essential next step.

### Limitations

- **Tissue coverage:** GTEx v8 lacks dorsal root ganglion (DRG) and synovium; we proxy DRG via spinal cord and tibial nerve, immune compartments via whole blood and spleen. Human DRG single-cell RNA-seq [20] could improve resolution.
- **Cell-type resolution:** GTEx provides bulk tissue TPM, masking cell-type-specific expression.
- **Static representation:** RA-PainKG is static; it does not model condition-specific dynamics or quantitative interaction strengths.
- **Identifier resolution:** PrimeKG node IDs are internal integers; cross-referencing with HGNC/Ensembl requires the original prime_kg.csv from the PrimeKG repository.
- **Coverage verification scope:** Recovery was assessed by exact symbol matching against PrimeKG; genes absent by exact symbol may be present under alternative identifiers or as protein complexes and were not exhaustively cross-referenced.
- **Curation completeness:** The initial 192-gene curation omits the canonically implicated analgesia gene DRD2 (descending dopaminergic analgesia), which should be incorporated in a future release. COMT, another frequently cited human pain-genetics locus, was recovered through the 2-hop expansion rather than the original curation and is therefore represented in the annotated set; the nine curated pathways are enumerated in Stage 1 to support reproducibility.

### Future updates

RA-PainKG will be updated with each major PrimeKG release; community contributions of pathway annotations, drug–target relations, and tissue-expression data are welcome via the GitHub repository. The modular pipeline enables systematic regeneration with updated inputs.

## Conclusions

RA-PainKG provides a transparently documented, tissue-contextualized, dual-track knowledge graph for RA pain signaling. It recovers 188/192 (97.9%) of curated pain genes, maps all nine pathways (57–100% coverage), and provides 4,760 drug–target edges for pharmacological queries. Transparent benchmark validation establishes honest boundary conditions for downstream use, including that graph structure adds little beyond node degree and edge density on the K562 test system. The open-source construction framework is extensible to other diseases where domain-specific knowledge graphs with documented recovery and gaps would accelerate mechanistic research.

## List of abbreviations

RA: rheumatoid arthritis; KG: knowledge graph; PPI: protein–protein interaction; GTEx: Genotype-Tissue Expression; TRP: transient receptor potential; SCN9A: sodium voltage-gated channel alpha subunit 9; TPM: transcripts per million; DRG: dorsal root ganglion; GO: Gene Ontology; BP: biological process; MLP: multilayer perceptron.

## Figure captions

**Figure 1.** Top 20 hub nodes ranked by betweenness centrality in RA-PainKG. Node size is proportional to betweenness score. The five highest-ranked hubs are EGR1, FOS, STAT3, AKT1, and SRC.

**Figure 2.** Degree distribution of RA-PainKG (log–log scale) with power-law fit. The scale-free topology is characteristic of biological networks.

**Figure 3.** Centrality distributions between Track A (immune-inflammation, n = 106) and Track B (nociception–pain transduction, n = 122). Track B genes show systematically lower centrality, consistent with sparser representation in the PPI subgraph.

**Figure 4.** Node type composition (10 entity types) and edge relation composition (24 relation types) of RA-PainKG.

**Figure 5.** Core signaling network visualization (top 50 hub nodes) with dual-track annotations.

**Figure 6.** Pathway subnetwork visualizations for all nine curated pain signaling pathways.

**Figure S1–S6** (Supplementary Material): degree distribution with power-law fit; track centrality comparison; GTEx tissue-expression heatmap for 165 annotated pain genes; core signaling network (top 50 hubs); node-type and edge-relation composition charts; and pathway subnetwork visualizations.

## Declarations

### Ethics approval and consent to participate
Not applicable.

### Consent for publication
Not applicable.

### Availability of data and materials
All code, processed adjacency matrices, and benchmark results are available in the repository at https://github.com/yyx-4113/ra-painkg under the MIT license. The knowledge-graph files (GraphML, CSV, pickle) are archived as GitHub Release v1.0.0 assets at https://github.com/yyx-4113/ra-painkg/releases/tag/v1.0.0, with SHA-256 checksums listed in MANIFEST_SHA256.txt. The Norman et al. Perturb-seq dataset is at Harvard Dataverse (DOI: 10.7910/DVN/R9JDLS); PrimeKG v1.0 at Harvard Dataverse (DOI: 10.7910/DVN/IXA7BM); Gene Ontology annotations are from the Gene Ontology Consortium [21].

### Competing interests
The author declares no competing interests.

### Funding
The author received no specific funding for this work; institutional resources from The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine supported the research.

### Authors' contributions
Yongxin Yang: Conceptualization, Methodology, Software, Formal Analysis, Investigation, Data Curation, Writing – Original Draft, Writing – Review and Editing, Visualization, Project Administration.

### Acknowledgements
The author thanks the Norman lab, the PrimeKG development team, the GTEx Consortium, and the Gene Ontology Consortium for public data. This research was supported by institutional resources from The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine.

## References

[1] Safiri S, Kolahi AA, Hoy D, et al. Global, regional and national burden of rheumatoid arthritis 1990–2017: a systematic analysis. Ann Rheum Dis. 2019;78(11):1463–1471.

[2] Cross M, Smith E, Hoy D, et al. The global burden of rheumatoid arthritis: estimates from the Global Burden of Disease 2010 study. Ann Rheum Dis. 2014;73(7):1316–1322.

[3] Lee YC, Cui J, Lu B, et al. Pain persists in DAS28 rheumatoid arthritis remission but not in ACR/EULAR remission. Ann Rheum Dis. 2011;70:1467–1470.

[4] McWilliams DF, Walsh DA. Pain mechanisms in rheumatoid arthritis. Clin Exp Rheumatol. 2017;35 Suppl 107(5):31–39.

[5] Basbaum AI, Bautista DM, Scherrer G, Julius D. Cellular and molecular mechanisms of pain. Cell. 2009;139(2):267–284.

[6] Julius D. TRP channels and pain. Annu Rev Cell Dev Biol. 2013;29:355–384.

[7] Ji RR, Nackley A, Huh Y, Terrando N, Maixner W. Neuroinflammation and central sensitization in chronic and widespread pain. Anesthesiology. 2018;129(2):343–366.

[8] Szklarczyk D, Kirsch R, Koutrouli M, et al. The STRING database in 2023: protein–protein association networks and functional enrichment analyses. Nucleic Acids Res. 2023;51(D1):D638–D646.

[9] Oughtred R, Rust J, Chang C, et al. The BioGRID database: A comprehensive biomedical resource of curated protein, genetic, and chemical interactions. Protein Sci. 2021;30(1):187–200.

[10] Kanehisa M, Furumichi M, Sato Y, Kawashima M, Ishiguro-Watanabe M. KEGG for taxonomy-based analysis of pathways and genomes. Nucleic Acids Res. 2023;51(D1):D587–D592.

[11] Gillespie M, Jassal B, Stephan R, et al. The reactome pathway knowledgebase 2022. Nucleic Acids Res. 2022;50(D1):D687–D692.

[12] Agrawal A, Balci H, Hanspers K, et al. WikiPathways 2024: next generation pathway database. Nucleic Acids Res. 2024;52(D1):D679–D689.

[13] Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine. Sci Data. 2023;10:67.

[14] Harding SD, Armstrong JF, Faccenda E, et al. The IUPHAR/BPS Guide to PHARMACOLOGY in 2024. Nucleic Acids Res. 2024;52(D1):D1438–D1449.

[15] Meloto CB, Benavides R, Lichtenwalter RN, et al. Human pain genetics database: a resource dedicated to human pain genetics research. Pain. 2018;159(4):749–763.

[16] Pinero J, Ramirez-Anguita JM, Sauch-Pitarch J, et al. The DisGeNET knowledge platform for disease genomics: 2019 update. Nucleic Acids Res. 2020;48(D1):D845–D855.

[17] GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects across human tissues. Science. 2020;369(6509):1318–1330.

[18] Norman TM, Horlbeck MA, Replogle JM, et al. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science. 2019;365(6455):786–793.

[19] Roohani Y, Huang K, Leskovec J. Predicting transcriptional outcomes of novel multigene perturbations with GEARS. Nat Biotechnol. 2024;42:591–600.

[20] Nguyen MQ, von Buchholtz LJ, Reker AN, Ryba NJ, Davidson S. Single-nucleus transcriptomic analysis of human dorsal root ganglion sensory neurons. Pain. 2021;162(7):2032–2046.

[21] Ashburner M, Ball CA, Blake JA, et al. Gene Ontology: tool for the unification of biology. Nat Genet. 2000;25(1):25–29.
