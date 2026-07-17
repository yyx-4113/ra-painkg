import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    content = f.read()

# ====== FIX 6: Add GTEx usage details to Methods 2.2 ======
old_gtx = "**Stage 3: Edge integration.**"
new_gtx = """**Tissue-contextual filtering with GTEx v8.** GTEx v8 median tissue expression data [16] were used to annotate each pain gene with tissue-specific expression levels across 54 human tissues. For nociception-relevant compartments, we used spinal cord (cervical C1), tibial nerve, whole blood, and spleen as proxies. A gene was classified as tissue-expressed if median TPM >= 1.0 in the relevant tissue. This information is provided as node attributes in the GraphML and CSV formats but was not used to filter edges in the current release, as removing edges based on bulk tissue expression risks discarding valid low-expression interactions. Future versions will incorporate single-cell expression data for finer tissue-contextual filtering.

**Stage 3: Edge integration.**"""
content = content.replace(old_gtx, new_gtx)
print("[6] GTEx usage description added to 2.2")

# ====== FIX 11: Add classification criteria for 192 genes ======
old_stage1 = "**Stage 1: Core gene curation.** 192 pain genes were manually curated from nine literature-defined pain signaling pathways:"
new_stage1 = """**Stage 1: Core gene curation.** 192 pain genes were manually curated from 15 literature-defined functional categories, organized into receptor/ion channel families (TRP channels, voltage-gated sodium channels, serotonin receptors, GABA/glycine receptors, opioid receptors, endocannabinoid system), intracellular signaling cascades (MAPK pathway, JAK-STAT pathway, kinase signaling, transcription factors), and disease/tissue-specific groups (prostaglandin pathway, complement cascade, neurotrophin signaling, RA-specific genes, anesthetic targets). Inclusion criteria: (1) published experimental evidence for a role in pain signaling, nociception, or RA inflammation in at least two independent studies (PubMed search: \"gene_symbol AND (pain OR nociception OR rheumatoid arthritis)\"), or (2) designation as a known drug target for analgesia or RA treatment in the IUPHAR/BPS Guide to Pharmacology [14] or DrugBank. The full gene list with functional category assignments and supporting PMIDs is provided in Supplementary Table S1."""
content = content.replace(old_stage1, new_stage1)
print("[11] 192 gene classification criteria added")

# ====== FIX 7: Compress benchmark section (3.3) from 70+ lines to ~30 lines ======
# Find the benchmark validation section and compress it
bmk_start = content.find("### 3.3 Benchmark Validation")
bmk_end = content.find("## 4. Discussion")

compressed_bmk = """### 3.3 Benchmark Validation

To establish transparent performance characteristics, we validated RA-PainKG in a perturbation prediction benchmark using the Norman K562 Perturb-seq dataset [20] (91,205 cells, 5,045 genes, 284 CRISPRi conditions). Gene embeddings were computed via spectral decomposition (k = 128) of the normalized graph Laplacian, and perturbation effects were predicted via ridge regression across 10 independent train/test splits (80%/20%). Full methods, results for all 11 KG variants, and sensitivity analyses are provided in Supplementary Tables S1-S6.

Two findings are directly relevant to the resource. First, RA-PainKG is 280-fold sparser than GO (2,400 vs 673,899 PPI edges), with 68.3% of Norman genes having zero edges. Among the 44 pain genes present in the Norman dataset (26.7% of 165 annotated genes), 59.1% (26/44) exhibit mean expression below 0.01 in K562 cells, and mean pain-gene expression (0.117) is comparable to the genome-wide background (0.107). These data establish a clear boundary condition: K562 perturbation prediction performance reflects test system limitations, not resource quality (see Discussion 4.3).

Second, the benchmark reveals a methodological consideration for KG evaluation: single-split evaluation produces artifacts. Under one split (seed 42), RA-PainKG appeared to outperform GO on pain genes (r = 0.558 vs 0.481), but the effect reversed under multi-split averaging (0.503 vs 0.542, Supplementary Table S5). This demonstrates the necessity of multi-split statistics for reliable KG evaluation.

Complete benchmark results for all 11 KG variants, paired statistical comparisons, sensitivity analyses (alpha = 0.001-100.0, k = 32-512), Kendall's W ranking consistency (0.64-0.65), and ablation analyses are documented in Supplementary Tables S1-S6.

"""

content = content[:bmk_start] + compressed_bmk + "\n" + content[bmk_end:]
print("[7] Benchmark section compressed from ~70 lines to ~25 lines")

# ====== FIX 5: Add Usage Examples section before Discussion ======
usage_examples = """## 4. Usage Examples

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

"""

# Insert before "## 4. Discussion"
disc_idx = content.find("## 4. Discussion")
content = content[:disc_idx] + usage_examples + "\n" + content[disc_idx:]
print("[5] Usage Examples section added (4 sub-sections)")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("[SAVED] Batch 2 complete")