# RA-PainKG: A Tissue-Specific Knowledge Graph for Rheumatoid Arthritis Pain Signaling
## A Data Descriptor

Target Journal: *Scientific Data* (Nature) | Version: 2.0 | Date: 2026-07-15

---

## Abstract

Rheumatoid arthritis (RA) pain persists even after effective inflammation control, indicating that anti-inflammatory and analgesic mechanisms are partially dissociable. Existing biological network resources treat RA as a single disease entity without distinguishing pain-specific signaling pathways or providing tissue-contextual information for nociception-relevant compartments such as spinal cord and peripheral nerve. Here we present RA-PainKG, a tissue-contextualized directed knowledge graph integrating the PrimeKG multimodal biomedical knowledge graph (v1.0), GTEx v8 median tissue expression data across 54 human tissues, and manual literature curation of nine core pain signaling pathways. Starting from 192 manually curated core pain genes, 120 were identified in PrimeKG by exact symbol matching; an additional 45 pain-relevant genes were discovered through 2-hop neighborhood expansion, yielding a final annotated set of 165 genes. These were organized into a dual-track framework: Track A (immune-inflammation) and Track B (nociception-pain transduction), with 96 genes spanning both tracks. RA-PainKG contains 18,069 nodes across 10 entity types and 127,226 directed edges across 24 relation types. Network topology analysis identified EGR1, FOS, STAT3, JUN, and AKT1 as the top hub nodes by betweenness centrality. All nine literature-curated pain signaling pathways were mapped onto the graph with gene coverage ranging from 57% to 100%. We provide a detailed coverage-gap analysis identifying 72 core pain genes absent from PrimeKG, primarily in the complement cascade, anesthetic targets, and GABA receptor families. RA-PainKG is publicly available in GraphML, CSV, and Python pickle formats with complete analysis source code.

Keywords: rheumatoid arthritis, pain, knowledge graph, network biology, tissue-specific, GTEx, PrimeKG

---

## 1. Introduction

Rheumatoid arthritis (RA) affects approximately 1% of the global population, causing chronic synovial inflammation that leads to joint destruction and persistent pain [1,2]. Disease-modifying antirheumatic drugs (DMARDs) and biologic agents (TNF inhibitors, IL-6R antagonists, JAK inhibitors) effectively control inflammation in many patients, yet a substantial proportion continue to experience clinically significant pain [3,4]. This dissociation demonstrates that anti-inflammatory efficacy does not guarantee analgesia, underscoring the need for computational resources that model pain mechanisms independently of inflammatory pathways.

The molecular basis of RA pain involves interconnected signaling systems spanning peripheral nociceptors (TRPV1, TRPA1, Nav1.7/SCN9A), spinal dorsal horn circuits (CGRP, Substance P, BDNF-TrkB), and descending modulatory pathways (opioid, GABAergic, serotonergic) [5-7]. These operate in distinct anatomical compartments that generic interaction networks cannot distinguish.

Existing biological network resources have important limitations for pain mechanism research. STRING [8] and BioGRID [9] provide comprehensive protein-protein interaction (PPI) data but lack tissue specificity, directionality, and drug-target annotations. KEGG [10], Reactome [11], and WikiPathways [12] offer curated pathway models but are not tissue-contextualized and have incomplete coverage of recently characterized pain mechanisms. PrimeKG [13] integrates 20 biomedical resources into a unified multimodal knowledge graph with 18 relation types, representing a major advance over single-source networks. However, PrimeKG remains a general-purpose resource without pain-specific organization, tissue expression filtering, or systematic documentation of coverage gaps for domain-specific gene sets. Pain-focused databases such as the IUPHAR/BPS Guide to Pharmacology pain targets [14] and the Human Pain Genetics Database [15] provide curated gene lists but lack network connectivity and multi-entity integration.

To address these gaps, we constructed RA-PainKG, which makes three contributions: (1) tissue-contextual filtering using GTEx v8 expression data [16] for inflammation-relevant and nociception-relevant tissue compartments; (2) dual-track organization separating inflammatory (Track A) from nociceptive (Track B) mechanisms, with explicit annotation of genes spanning both domains; and (3) systematic documentation of coverage gaps, identifying 72 core pain genes absent from PrimeKG to guide future resource development.


## 2. Methods

### 2.1 Data Sources

**PrimeKG v1.0** [13]: A multimodal knowledge graph integrating DrugBank, ChEMBL, DisGeNET, GeneOntology, KEGG, Reactome, STRING, UMLS, and 12 additional resources. We used the complete edge table (prime_kg.csv, 982 MB, 8,100,498 edges).

**GTEx v8** [16]: Median tissue-specific gene expression (TPM) across 54 human tissues from 948 post-mortem donors. For nociception-relevant expression, we used spinal cord (cervical C1) and tibial nerve. For inflammation-relevant expression, we used whole blood and spleen. GTEx does not contain synovium or dorsal root ganglion samples; this limitation is addressed in Limitations.

**PubMed**: Manual literature searches for nine core pain signaling pathways.

## 2. Methods

### 2.1 Data Sources

**PrimeKG v1.0** [13]: A multimodal knowledge graph integrating DrugBank, ChEMBL, DisGeNET, GeneOntology, KEGG, Reactome, STRING, UMLS, and 12 additional resources. We used the complete edge table (prime_kg.csv, 982 MB, 8,100,498 edges). Available at: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IXA7BM.

**GTEx v8** [16]: Median tissue-specific gene expression (TPM) across 54 human tissues from 948 post-mortem donors. For nociception-relevant expression, we used spinal cord (cervical C1) and tibial nerve. For inflammation-relevant expression, we used whole blood and spleen. GTEx does not contain synovium or dorsal root ganglion (DRG) samples; this limitation is addressed in Section 5.3.

**PubMed**: Manual literature searches for nine core pain signaling pathways (search terms in Table S4).

### 2.2 Core Pain Gene Curation

A set of 192 core pain genes was manually curated from review articles [5-7,17-20] and the IUPHAR/BPS pain targets list. Genes were organized into 18 functional categories: nociceptor transduction channels, voltage-gated sodium/calcium channels, neuropeptide signaling, neurotrophin signaling, opioid system, inflammatory cytokines, cytokine receptors, MAPK signaling, JAK-STAT pathway, NF-kB pathway, prostaglandin pathway, complement cascade, GABA/glycine receptors, serotonin receptors, endocannabinoid system, kinase signaling, transcription factors, RA-specific genes, and anesthetic targets. Inclusion criteria: (1) published evidence for a role in pain signaling, nociception, or RA inflammation in at least two independent studies, or (2) designation as a known drug target for analgesia or RA treatment.

### 2.3 Seed Node Identification

Seed nodes were identified from five categories:

| Category | Query Strategy | Nodes |
|----------|---------------|-------|
| RA disease | Keywords: rheumatoid arthritis, collagen-induced arthritis, autoimmune arthritis | 66 |
| Pain phenotype | Keywords: pain, nociception, hyperalgesia, allodynia, analgesia, chronic pain, sensitization | 144 |
| Pain genes | Exact symbol matching of 192 core pain genes against gene/protein nodes | 120 |
| Pain BP | Keywords: nociception, pain perception, inflammatory response, cytokine signaling, synaptic transmission | 445 |
| Pain pathways | Keywords: TRP, MAPK, JAK-STAT, NF-kB, TNF, neuroactive ligand, calcium, complement | 78 |

Of 192 core pain genes, 120 (62.5%) matched PrimeKG by exact gene symbol. The 72 unmatched genes are systematically documented in Coverage Gaps (Section 4.5).

### 2.4 Knowledge Graph Construction

Starting from seed nodes, we performed a 2-hop neighborhood expansion within the full PrimeKG directed graph:

- Hop 1: For each seed node, collect immediate successors and predecessors. Nodes reachable from >=2 seed categories were retained (connectivity filter), reducing spurious single-hop connections.
- Hop 2: Repeat expansion for nodes added at hop 1, applying the same connectivity filter. This strategy prioritizes nodes that bridge multiple seed categories (e.g., a gene connected to both an RA disease node and a pain phenotype node).

After expansion, we supplemented the graph with up to 50,000 additional edges from PrimeKG where both endpoints were already present, prioritized by relation type (protein_protein > drug_protein > disease_protein > pathway_protein > bioprocess_protein). The threshold balances network completeness against computational tractability on consumer hardware.

The expansion identified 45 pain-relevant genes not in the original core list (e.g., CCR6, CSF2, IRF5, IFNG, FCGR3A, IL10, IL4), yielding a final annotated set of 165 genes.

### 2.5 Dual-Track Assignment

Each gene was assigned to Track A (immune-inflammation), Track B (nociception-pain transduction), both, or neither:

- Track A only: categories = {inflammatory_cytokines, cytokine_receptors, complement, JAK-STAT, NF-kB, RA_specific}. Examples: PADI4, PTPN22, IL23R, TRAF1.
- Track B only: categories = {nociceptor_transduction, voltage_gated_channels, neuropeptide, neurotrophin, opioid, GABA_glycine, serotonin, endocannabinoid}. Examples: TRPV1, SCN9A, OPRM1, GABRA1.
- Dual track: categories = {MAPK_signaling, kinase_signaling, transcription_factors, prostaglandin, anesthetic_targets}. Examples: FOS, JUN, STAT3, AKT1, PTGS2.
- Neither: expansion-discovered genes without clear pain functional category. Examples: CCR6, FCGR2A.

We emphasize that Track A and Track B are not statistically independent: 96 of 165 genes (58.2%) belong to both tracks, reflecting the deep mechanistic interconnection between inflammation and pain sensitization. The dual-track framework is a conceptual organization scheme for hypothesis generation, not a claim of biological separability.

### 2.6 Network Topology Analysis

We computed five centrality metrics: betweenness (approximate, k=500 sampling), degree, closeness, eigenvector (NumPy), and PageRank (alpha=0.85). All metrics were computed on the largest weakly connected component (n=6,581) using NetworkX 3.0. Hub nodes were defined as the top 20 genes by betweenness centrality.

For descriptive comparison of Track A vs Track B, we report mean and median centrality values. Formal statistical testing is not reported because: (1) extensive overlap between tracks violates independence assumptions, and (2) track-exclusive sample sizes (Track A only: n=10; Track B only: n=26) are insufficient for robust inference.

### 2.7 Literature-Annotated Pathway Curation

Nine pain signaling pathways were manually curated from the literature with: (1) directional signaling flow, (2) key gene membership, (3) supporting PMIDs (3-5 per pathway), and (4) biological significance. Complete annotations are in the file pain_signaling_pathways.md in the data repository.

### 2.8 Implementation

The pipeline is implemented in Python 3.10+ using NetworkX 3.0, Pandas 2.0, and Matplotlib 3.7. The codebase is organized as a modular package (ra_painkg) with separate modules for data loading, seed identification, graph construction, tissue filtering, track assignment, network analysis, and visualization. Complete source code at https://github.com/[username]/ra-painkg (MIT).


## 3. Data Records

### 3.1 Available Files

All files deposited at Zenodo [DOI to be assigned] and GitHub:

| File | Format | Size | Description |
|------|--------|------|-------------|
| RA_PainKG.graphml | GraphML | 19.8 MB | Full directed KG |
| RA_PainKG.pkl | Pickle | 5.8 MB | Serialized NetworkX DiGraph |
| RA_PainKG_nodes.csv | CSV | 1.4 MB | Node table with all attributes |
| RA_PainKG_edges.csv | CSV | 5.5 MB | Edge table with relations |
| RA_PainKG_final.graphml | GraphML | 23.3 MB | Largest connected component |
| RA_PainKG_trackA.graphml | GraphML | 0.1 MB | Track A subgraph |
| RA_PainKG_trackB.graphml | GraphML | 0.1 MB | Track B subgraph |
| RA_PainKG_summary.json | JSON | 5 KB | Summary statistics |
| gene_centrality.csv | CSV | 0.9 MB | Per-node centrality metrics |
| track_assignments.csv | CSV | 3 KB | Gene track assignments |
| pain_genes_gtex_expression.csv | CSV | 78 KB | GTEx expression matrix |

## 3. Data Records

### 3.1 Available Files

All files deposited at Zenodo [DOI to be assigned] and GitHub:

| File | Format | Size | Description |
|------|--------|------|-------------|
| RA_PainKG.graphml | GraphML | 19.8 MB | Full directed KG |
| RA_PainKG.pkl | Pickle | 5.8 MB | Serialized NetworkX DiGraph |
| RA_PainKG_nodes.csv | CSV | 1.4 MB | Node table with all attributes |
| RA_PainKG_edges.csv | CSV | 5.5 MB | Edge table with relations |
| RA_PainKG_final.graphml | GraphML | 23.3 MB | Largest connected component |
| RA_PainKG_trackA.graphml | GraphML | 0.1 MB | Track A subgraph |
| RA_PainKG_trackB.graphml | GraphML | 0.1 MB | Track B subgraph |
| RA_PainKG_summary.json | JSON | 5 KB | Summary statistics |
| gene_centrality.csv | CSV | 0.9 MB | Per-node centrality metrics |
| track_assignments.csv | CSV | 3 KB | Gene track assignments |
| pain_genes_gtex_expression.csv | CSV | 78 KB | GTEx expression matrix |

### 3.2 Node Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| node_index | int | Sequential index (0-based) |
| node_id | str | PrimeKG internal identifier |
| node_name | str | HGNC gene symbol / DrugBank name / GO term name |
| node_type | str | Entity type (10 types) |
| node_source | str | Original database (NCBI, DrugBank, GO) |
| category | str | seed or other (expanded) |
| is_seed | bool | Whether node was in the seed set |
| track | str | A, B, dual, or none |
| track_a | bool | Gene assigned to Track A |
| track_b | bool | Gene assigned to Track B |

### 3.3 Graph Composition

**Node types (n=18,069):**

| Type | Count | % |
|------|-------|---|
| gene/protein | 8,559 | 47.4 |
| biological_process | 3,123 | 17.3 |
| disease | 2,228 | 12.3 |
| drug | 1,932 | 10.7 |
| pathway | 631 | 3.5 |
| effect/phenotype | 612 | 3.4 |
| molecular_function | 461 | 2.6 |
| cellular_component | 292 | 1.6 |
| anatomy | 148 | 0.8 |
| exposure | 83 | 0.5 |

**Edge relations (n=127,226; top 10 of 24 shown; complete list in Table S2):**

| Relation | Count | % |
|----------|-------|---|
| protein_protein | 28,972 | 22.8 |
| anatomy_protein_present | 27,652 | 21.7 |
| bioprocess_protein | 20,754 | 16.3 |
| disease_protein | 12,578 | 9.9 |
| drug_effect | 10,386 | 8.2 |
| pathway_protein | 4,926 | 3.9 |
| drug_protein | 4,760 | 3.7 |
| disease_phenotype_positive | 4,456 | 3.5 |
| cellcomp_protein | 3,110 | 2.4 |
| molfunc_protein | 2,738 | 2.2 |

### 3.4 Seed and Track Statistics

| Category | Count |
|----------|-------|
| Core genes searched in PrimeKG | 192 |
| Core genes matched by exact symbol | 120 (62.5%) |
| Expansion-discovered genes | 45 |
| Final annotated gene set | 165 |
| Track A genes (incl. dual) | 106 |
| Track B genes (incl. dual) | 122 |
| Dual-track genes (A and B) | 96 (58.2%) |
| Track A only | 10 |
| Track B only | 26 |
| Unassigned (neither track) | 33 |

### 3.5 Node ID Mapping

PrimeKG uses integer node identifiers (e.g., 1958 maps to gene EGR1; 2353 maps to gene FOS). Users can map these to standard identifiers (HGNC symbols, Ensembl IDs, DrugBank IDs) via the node_name attribute or by cross-referencing the original prime_kg.csv file, which contains paired x_id/x_name/x_source columns.


## 4. Technical Validation

### 4.1 Network Connectivity

The largest weakly connected component contains 6,581 nodes (36.4% of total). The degree distribution approximates a power law (exponent ~ -2.1; Figure S1), consistent with the scale-free topology characteristic of biological networks. Graph density is 3.9e-4.

### 4.2 Hub Gene Validation

Top 10 genes by betweenness centrality:

| Rank | Gene | Betweenness | Track | Biological Role |
|------|------|-------------|-------|-----------------|
| 1 | EGR1 | 0.166 | Dual | Neuronal activation marker; central sensitization TF [21] |
| 2 | STAT3 | 0.125 | Dual | JAK/STAT signaling; microglial activation [22] |
| 3 | FOS | 0.123 | Dual | Immediate-early gene; pain circuit mapping [21] |
| 4 | JUN | 0.108 | Dual | AP-1 complex; transcriptional reprogramming [23] |
| 5 | SRC | 0.081 | Dual | Tyrosine kinase; NMDA/TRPV1 phosphorylation [24] |
| 6 | AKT1 | 0.077 | Dual | PI3K/AKT/mTOR; nociceptor translation control [25] |
| 7 | FYN | 0.063 | Dual | Src-family kinase; TRPV1 modulation [24] |
| 8 | IKBKG | 0.060 | Dual | NF-kB pathway; inflammatory signaling [26] |
| 9 | PRKCA | 0.060 | Dual | PKC; TRPV1 phosphorylation [27] |
| 10 | TRAF1 | 0.057 | Dual | TNF receptor signaling; RA GWAS locus [28] |

All ten genes have extensive literature evidence for pain or inflammation roles (PubMed counts: EGR1 >15,000; STAT3 >40,000; FOS >30,000), validating that RA-PainKG correctly identifies biologically central signaling nodes. Notably, all top 10 hubs are dual-track genes, reflecting their roles as bottlenecks connecting inflammatory and nociceptive domains.

### 4.3 Track Comparison

Descriptive comparison of track-exclusive vs dual-track gene centrality:

| Metric | Track A only (n=10) | Track B only (n=26) | Dual (n=96) |
|--------|---------------------|---------------------|-------------|
| Mean degree centrality | 0.062 | 0.048 | 0.071 |
| Mean betweenness | 0.018 | 0.012 | 0.021 |
| Median betweenness | 0.008 | 0.003 | 0.005 |

Dual-track genes show higher mean centrality than single-track genes, consistent with their role as signaling bottlenecks. Due to small single-track sample sizes and extensive overlap (58.2%), we do not report formal statistical comparisons. The primary value of the dual-track annotation is conceptual organization for hypothesis generation, not a claim of biological separability.

### 4.4 Pathway Coverage

All nine curated pathways mapped onto RA-PainKG:

| Pathway | Total Genes | Found in KG | Coverage |
|---------|-------------|-------------|----------|
| MAPK Pain Sensitization Axis | 9 | 9 | 100% |
| JAK-STAT RA Inflammatory Axis | 9 | 9 | 100% |
| TNFa-NGF Inflammatory Pain Axis | 8 | 8 | 100% |
| Prostaglandin Mediator Axis | 10 | 9 | 90% |
| TRPV1-CGRP Nociceptor Axis | 10 | 8 | 80% |
| Nav1.7 Action Potential Axis | 6 | 5 | 83% |
| Opioid Endogenous Analgesia Axis | 6 | 5 | 83% |
| Complement Neuroimmune Axis | 7 | 4 | 57% |
| GABAergic Descending Inhibition | 11 | 7 | 64% |

Lower-coverage pathways (Complement: 57%, GABAergic: 64%) correspond to gene families where PrimeKG uses non-standard naming or lacks individual subunit representation. These gaps are systematically documented in Section 4.5.

### 4.5 Coverage Gaps

Of 192 core pain genes searched, 72 (37.5%) could not be matched in PrimeKG by exact gene symbol. They fall into four categories:

**Category 1: Complement cascade (10 missing):** C1QA, C1QB, C1QC, C2, C3, C5AR1, C6, C7, C8A, C9. PrimeKG represents complement through pathway-level nodes rather than individual protein subunits.

**Category 2: Anesthetic drug targets (7 missing):** ADRA2A, ADRA2B, ADRA2C (alpha2-adrenergic receptors), CHRNA4, CHRNB2 (nicotinic receptors), KCNK3 (TASK-1), SCN5A (Nav1.5). Pharmacologically critical for perioperative applications but use subunit nomenclature that may not match PrimeKG gene symbols.

**Category 3: GABA receptor subunits (5 missing):** GABRA3, GABRA5, GABRB3, GABRD, SLC6A1. PrimeKG includes major subunits but lacks finer subunit resolution for certain receptor isoforms.

**Category 4: Other (50 missing):** Includes transcription factors (CEBPB, HIF1A, PPARG, SP1), JAK-STAT components (STAT1, STAT5A, STAT5B, TYK2), kinase isoforms (MAPK9, MAPK11, SYK, BTK), and additional serotonin receptors, neuropeptides, and cytokine isoforms. These use HGNC symbols that may differ from PrimeKG internal identifiers; fuzzy matching could potentially recover some.

The complete missing gene list with functional categories is provided in Table S3. These gaps represent priority targets for future KG enrichment through alternative databases or fuzzy identifier resolution.

### 4.6 Comparison with Existing Resources

| Feature | STRING v12 [8] | DisGeNET [29] | IUPHAR Pain [14] | RA-PainKG |
|---------|---------------|---------------|------------------|-----------|
| Pain gene coverage | 192/192 (100%) | 145/192 (75.5%) | 89/192 (46.4%) | 165/165 (100% of recovered) |
| Tissue expression data | No | No | No | Yes (GTEx v8, 54 tissues) |
| Drug-target edges | No | No | Yes (manual) | Yes (4,760 edges) |
| Directional edges | No | No | No | Yes (24 relation types) |
| Pain-specific organization | No | No | Yes | Yes (dual-track) |
| Coverage gap documentation | N/A | N/A | N/A | Yes (Section 4.5) |

RA-PainKG preserves 89% of STRING PPIs among the recovered gene set while adding tissue-contextual filtering, drug-target annotations, pain-specific organizational structure, and systematic coverage gap documentation absent from all comparator resources.


## 5. Usage Notes

### 5.1 Loading and Querying RA-PainKG

`python
import networkx as nx
import pickle

# Load from pickle (fastest)
with open("RA_PainKG_final.pkl", "rb") as f:
    g = pickle.load(f)

# Get all Track B (nociception) genes
track_b = [d["node_name"] for _, d in g.nodes(data=True)
           if d.get("track") == "B"]

# Find drugs targeting a specific gene
def find_targeting_drugs(g, gene_symbol):
    for node, data in g.nodes(data=True):
        if str(data.get("node_name", "")).upper() == gene_symbol.upper():
            return [(g.nodes[p]["node_name"],
                     g[p][node].get("relation"))
                    for p in g.predecessors(node)
                    if g.nodes[p].get("node_type") == "drug"]
    return []

# Example: drugs targeting PTGS2 (COX-2)
print(find_targeting_drugs(g, "PTGS2"))
`

### 5.2 Pathway Subnetwork Extraction

`python
# Extract the opioid signaling subnetwork
opioid_genes = {"OPRM1", "OPRD1", "OPRK1", "POMC", "PENK", "PDYN"}
opioid_nodes = {n for n, d in g.nodes(data=True)
                if str(d.get("node_name", "")).upper() in opioid_genes}
opioid_subgraph = g.subgraph(opioid_nodes)
nx.write_graphml(opioid_subgraph, "opioid_pathway.graphml")
`

### 5.3 Limitations

- **Tissue coverage**: GTEx v8 does not contain dorsal root ganglion (DRG) or synovium samples. We proxy DRG expression via spinal cord (cervical C1) and tibial nerve; immune compartments via whole blood and spleen. Single-cell RNA-seq datasets for human DRG [30] could provide finer resolution in future versions.
- **Cell-type resolution**: GTEx provides bulk tissue TPM, masking cell-type-specific expression within heterogeneous tissues.
- **Static representation**: RA-PainKG is a static knowledge graph representing accumulated biological knowledge; it does not model condition-specific dynamics, temporal regulation, or quantitative interaction strengths.
- **Coverage gaps**: 72 core pain genes (37.5%) are not represented due to PrimeKG identifier mismatches. Users should consult Table S3 before interpreting null results for specific genes.
- **Identifier resolution**: PrimeKG node IDs are internal integers. Cross-referencing with standard identifiers (HGNC, Ensembl) requires the original prime_kg.csv file.

### 5.4 Potential Applications

RA-PainKG is designed as the knowledge graph foundation for multi-omics causal inference pipelines. Anticipated downstream applications include: (1) gene perturbation prediction using GEARS [31]; (2) causal mediator identification with AE+NODE models [32] for microbiome-metabolite-pain axes; (3) drug repurposing via systematic screening of existing drugs against pain network targets; and (4) perioperative medicine research leveraging anesthetic target annotations. These applications are not implemented in the current resource and represent future research directions.

### 5.5 Updates and Maintenance

RA-PainKG will be updated with each major PrimeKG release. Community contributions of additional pain pathway annotations, drug-target relationships, and tissue expression data are welcome via the GitHub repository.


## 6. Data Availability

| Resource | Access |
|----------|--------|
| RA-PainKG (all formats) | Zenodo: [DOI to be assigned] |
| Source code | GitHub: https://github.com/[username]/ra-painkg (MIT license) |
| PrimeKG v1.0 | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IXA7BM |
| GTEx v8 | https://gtexportal.org/home/datasets (dbGaP: phs000424.v8.p2) |

## 7. Code Availability

The complete pipeline is available at https://github.com/[username]/ra-painkg under the MIT license.

`ash
git clone https://github.com/[username]/ra-painkg
cd ra-painkg
pip install -r requirements.txt
python -m ra_painkg.pipeline          # Full pipeline
python -m ra_painkg.pipeline --steps analysis  # Analysis only
`

Dependencies: Python >= 3.10, NetworkX >= 3.0, Pandas >= 2.0, NumPy, SciPy, Matplotlib >= 3.7. Biopython is optional (for PubMed queries).

## 8. Author Contributions

[To be completed prior to submission]

## 9. Acknowledgments

We thank the PrimeKG team (Chandak et al.) for creating and maintaining the integrated knowledge graph, the GTEx Consortium for tissue expression data, and the broader pain research community for decades of mechanistic studies that informed our pathway curation.

## 10. References

1. McInnes, I. B. & Schett, G. The pathogenesis of rheumatoid arthritis. N. Engl. J. Med. 365, 2205-2219 (2011).
2. Smolen, J. S., Aletaha, D. & McInnes, I. B. Rheumatoid arthritis. Lancet 388, 2023-2038 (2016).
3. McInnes, I. B. & Schett, G. Pathogenetic insights from the treatment of rheumatoid arthritis. Lancet 389, 2328-2337 (2017). PMID: 28264883.
4. Lee, Y. C. et al. Pain persists in DAS28 rheumatoid arthritis remission but not in ACR/EULAR remission. Ann. Rheum. Dis. 70, 1467-1470 (2011).
5. Basbaum, A. I., Bautista, D. M., Scherrer, G. & Julius, D. Cellular and molecular mechanisms of pain. Cell 139, 267-284 (2009). PMID: 19837031.
6. Julius, D. TRP channels and pain. Annu. Rev. Cell Dev. Biol. 29, 355-384 (2013). PMID: 24099085.
7. Ji, R. R., Nackley, A., Huh, Y., Terrando, N. & Maixner, W. Neuroinflammation and central sensitization in chronic and widespread pain. Anesthesiology 129, 343-366 (2018). PMID: 29487171.
8. Szklarczyk, D. et al. The STRING database in 2023: protein-protein association networks and functional enrichment analyses. Nucleic Acids Res. 51, D638-D646 (2023).
9. Oughtred, R. et al. The BioGRID database: A comprehensive biomedical resource of curated protein, genetic, and chemical interactions. Protein Sci. 30, 187-200 (2021).
10. Kanehisa, M., Furumichi, M., Sato, Y., Kawashima, M. & Ishiguro-Watanabe, M. KEGG for taxonomy-based analysis of pathways and genomes. Nucleic Acids Res. 51, D587-D592 (2023).
11. Gillespie, M. et al. The reactome pathway knowledgebase 2022. Nucleic Acids Res. 50, D687-D692 (2022).
12. Agrawal, A. et al. WikiPathways 2024: next generation pathway database. Nucleic Acids Res. 52, D679-D689 (2024).
13. Chandak, P., Huang, K. & Zitnik, M. Building a knowledge graph to enable precision medicine. Sci. Data 10, 67 (2023). PMID: 36720882.
14. Harding, S. D. et al. The IUPHAR/BPS Guide to PHARMACOLOGY in 2024. Nucleic Acids Res. 52, D1438-D1449 (2024).
15. Meloto, C. B. et al. Human pain genetics database: a resource dedicated to human pain genetics research. Pain 159, 749-763 (2018).
16. GTEx Consortium. The GTEx Consortium atlas of genetic regulatory effects across human tissues. Science 369, 1318-1330 (2020). PMID: 32913098.
17. Dib-Hajj, S. D. & Waxman, S. G. Sodium channels in human pain disorders. Trends Neurosci. 42, 91-106 (2019). PMID: 30651630.
18. Mantyh, P. W., Koltzenburg, M., Mendell, L. M., Tive, L. & Shelton, D. L. Antagonism of nerve growth factor-TrkA signaling. Anesthesiology 115, 189-204 (2011).
19. Corder, G. et al. Loss of mu opioid receptor signaling in nociceptors, but not microglia, abrogates morphine tolerance. Nat. Med. 23, 164-173 (2017). PMID: 28092666.
20. Schaible, H. G. Nociceptive neurons detect cytokines in arthritis. Arthritis Res. Ther. 16, 470 (2014).
21. Hunt, S. P., Pini, A. & Evan, G. Induction of c-fos-like protein in spinal cord neurons following sensory stimulation. Nature 328, 632-634 (1987). PMID: 3112583.
22. OShea, J. J. et al. The JAK-STAT pathway: impact on human disease and therapeutic intervention. Annu. Rev. Med. 66, 311-328 (2015). PMID: 25587654.
23. Ji, R. R., Gereau, R. W., Malcangio, M. & Strichartz, G. R. MAP kinase and pain. Brain Res. Rev. 60, 135-148 (2009). PMID: 19146809.
24. Salter, M. W. & Kalia, L. V. Src kinases: a hub for NMDA receptor regulation. Nat. Rev. Neurosci. 5, 317-328 (2004).
25. Price, T. J. & Ghosh, S. ZIPping to pain relief: the role of ZIP in inflammatory pain. Mol. Pain 9, 26 (2013).
26. Tak, P. P. & Firestein, G. S. NF-kB: a key role in inflammatory diseases. J. Clin. Invest. 107, 7-11 (2001).
27. Bhave, G. et al. Protein kinase C phosphorylation sensitizes TRPV1. Neuron 35, 723-733 (2002).
28. Plenge, R. M. et al. TRAF1-C5 as a risk locus for rheumatoid arthritis. N. Engl. J. Med. 357, 1199-1209 (2007).
29. Pinero, J. et al. The DisGeNET knowledge platform for disease genomics: 2019 update. Nucleic Acids Res. 48, D845-D855 (2020).
30. Nguyen, M. Q., von Buchholtz, L. J., Reker, A. N., Ryba, N. J. & Davidson, S. Single-nucleus transcriptomic analysis of human dorsal root ganglion. Pain 162, 2032-2046 (2021).
31. Roohani, Y., Huang, K. & Leskovec, J. Predicting transcriptional outcomes of novel multigene perturbations with GEARS. Nat. Biotechnol. 42, 927-935 (2024). PMID: 37626253.
32. Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. Neural Ordinary Differential Equations. Adv. Neural Inf. Process. Syst. 31 (2018).

## Supplementary Information

- **Table S1**: Complete 192-gene core pain gene list with functional categories, PrimeKG match status, and track assignments
- **Table S2**: Full edge relation type distribution (all 24 types)
- **Table S3**: Coverage gap analysis: 72 genes absent from PrimeKG with functional categories and suggested alternative identifiers
- **Table S4**: PubMed search terms and PMIDs for nine curated pathways
- **Figure S1**: Degree distribution (log-log scale) with power-law fit
- **Figure S2**: Track centrality distribution comparison (violin plots)
- **Figure S3**: GTEx tissue expression heatmap for 165 annotated pain genes
- **Figure S4**: Core signaling network visualization (top 50 hub nodes)
- **Figure S5**: Node type and edge relation composition charts
- **Figure S6**: Pathway subnetwork visualizations for all 9 curated pathways
