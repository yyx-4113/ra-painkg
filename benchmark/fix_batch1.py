import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    content = f.read()

# ====== FIX 3: Remove duplicate Keywords ======
old = "**Keywords:** knowledge graph; rheumatoid arthritis; pain signaling; PrimeKG; GTEx; coverage-gap analysis; tissue-specific; database resource\n\n**Keywords:** knowledge graphs; perturbation prediction; benchmark methodology; ablation study; multi-split validation; rheumatoid arthritis"
new = "**Keywords:** knowledge graph; rheumatoid arthritis; pain signaling; PrimeKG; GTEx; coverage-gap analysis; tissue-specific; database resource"
content = content.replace(old, new)
print("[3] Duplicate keywords removed")

# ====== FIX 15: Fix encoding artifacts ======
content = content.replace("每", "-")
content = content.replace("〞", "\"")
content = content.replace("鈥", "--")
print("[15] Encoding artifacts cleaned")

# ====== FIX 1: Rewrite Introduction ======
# Find old intro boundaries (from "## 1. Introduction" to "## 2. Materials and Methods")
intro_start = content.find("## 1. Introduction")
methods_start = content.find("## 2. Materials and Methods")

new_intro = """## 1. Introduction

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

"""

content = content[:intro_start] + new_intro + content[methods_start:]
print("[1] Introduction rewritten")
print("[4] References fixed in new Introduction")

# ====== FIX 2: Reorder Methods subsections ======
# Current: 2.1 KG Construction -> 2.4 Perturbation Data -> 2.2 Construction Pipeline -> 2.3 Coverage-Gap
# Target: 2.1 KG Construction -> 2.2 Construction Pipeline -> 2.3 Coverage-Gap -> 2.4 Perturbation Data

# Find and reorder sections
# First, extract the sections
sec_21 = content[content.find("### 2.1 Knowledge Graph Construction"):content.find("### 2.4 Perturbation Data and Benchmark Validation")]
sec_24 = content[content.find("### 2.4 Perturbation Data and Benchmark Validation"):content.find("### 2.2 RA-PainKG Construction Pipeline")]
sec_22 = content[content.find("### 2.2 RA-PainKG Construction Pipeline"):content.find("### 2.3 Coverage-Gap Analysis")]
sec_23 = content[content.find("### 2.3 Coverage-Gap Analysis"):content.find("### 2.5 Gene Embedding")]

# Rebuild Methods section in correct order
pre_methods = content[:content.find("### 2.1 Knowledge Graph Construction")]
post_23 = content[content.find("### 2.5 Gene Embedding"):]

new_methods = pre_methods
# 2.1 KG Construction (brief intro)
new_methods += "### 2.1 Knowledge Graph Construction\n\nRA-PainKG was constructed in three stages (detailed protocol in [19]).\n\n"
# 2.2 Construction Pipeline (the stages)
new_methods += "### 2.2 RA-PainKG Construction Pipeline\n\n"
# Extract just the stage text from sec_22 (skip the header)
stage_text = sec_22[sec_22.find("\n"):]  
new_methods += stage_text.strip() + "\n\n"
# 2.3 Coverage-Gap Analysis
new_methods += sec_23.strip() + "\n\n"
# 2.4 Perturbation Data and Benchmark Validation
new_methods += sec_24.strip().replace("### 2.4 Perturbation Data and Benchmark Validation", "### 2.4 Perturbation Data and Benchmark Validation") + "\n\n"
# Rest
new_methods += post_23

# Fix section numbers in remaining content
new_methods = new_methods.replace("### 2.5 Gene Embedding and Prediction Model", "### 2.5 Gene Embedding and Prediction Model")
new_methods = new_methods.replace("### 2.6 Evaluation Protocol", "### 2.6 Evaluation Protocol")
new_methods = new_methods.replace("### 2.7 K562 Pain Gene Expression Quantification", "### 2.7 K562 Pain Gene Expression Quantification")
new_methods = new_methods.replace("### 2.8 Implementation", "### 2.8 Implementation")

content = new_methods
print("[2] Methods sections reordered: 2.1 -> 2.2 -> 2.3 -> 2.4 -> 2.5 -> 2.6 -> 2.7 -> 2.8")

# Save intermediate
with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("[SAVED] Batch 1 complete")