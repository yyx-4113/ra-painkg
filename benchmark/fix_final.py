import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    c = f.read()

# ====== FIX 1: Rename Usage Examples from ## 4. to ## 5. ======
c = c.replace("## 4. Usage Examples", "## 5. Usage Examples")
c = c.replace("### 4.1 Querying Drug-Target", "### 5.1 Querying Drug-Target")
c = c.replace("### 4.2 Extracting Pathway", "### 5.2 Extracting Pathway")
c = c.replace("### 4.3 Tissue Expression", "### 5.3 Tissue Expression")
c = c.replace("### 4.4 Identifying Bridge", "### 5.4 Identifying Bridge")
print("[1] Usage Examples: ## 4 -> ## 5")

# ====== FIX 2: Merge duplicate dual-track overlap text in 3.1 ======
old_dup = """This overlap is biologically expected given the mechanistic interconnection between inflammation and pain sensitization, The substantial Track A/B overlap (58.2%) is biologically expected: transcription factors (FOS, JUN, STAT3) activated by inflammatory cytokines also drive nociceptive sensitization, MAP kinases transduce both inflammatory and pain signals, and prostaglandins (via COX-2/PTGS2) bridge immune activation and nociceptor sensitization [5,7]. Rather than indicating poor track separation, this overlap reflects the mechanistic reality that inflammation and pain are deeply coupled in RA. The dual-track framework should be used as a conceptual lens for hypothesis generation-for example, genes exclusive to Track A or B may represent intervention points where anti-inflammatory and analgesic effects can be partially decoupled, while dual-track hub genes represent convergence points where both processes are jointly regulated."""
new_merge = """The substantial Track A/B overlap (58.2%) is biologically expected: transcription factors (FOS, JUN, STAT3) activated by inflammatory cytokines also drive nociceptive sensitization, MAP kinases transduce both inflammatory and pain signals, and prostaglandins (via COX-2/PTGS2) bridge immune activation and nociceptor sensitization [5,7]. Rather than indicating poor track separation, this overlap reflects the mechanistic reality that inflammation and pain are deeply coupled in RA. The dual-track framework serves as a conceptual lens for hypothesis generation: genes exclusive to Track A or B may represent intervention points where anti-inflammatory and analgesic effects can be partially decoupled, while dual-track hub genes represent convergence points where both processes are jointly regulated."""
c = c.replace(old_dup, new_merge)
print("[2] Merged duplicate dual-track text")

# ====== FIX 3: Author name encoding ======
c = c.replace("Yongxin Yang (栦蚗陔)", "Yongxin Yang")
print("[3] Fixed author name encoding")

# ====== FIX 4: Fix complement reference [17] -> [7] ======
c = c.replace("C5a-C5aR1 signaling in sensory neurons [17]", "C5a-C5aR1 signaling in sensory neurons [7]")
print("[4] Fixed complement reference: [17](DisGeNET) -> [7](Ji, neuroinflammation)")

# ====== FIX 5: Renumber Table 4 -> Table 2 ======
c = c.replace("**Table 4. Comparison with existing resources**", "**Table 2. Comparison with existing resources**")
c = c.replace("demonstrates its unique contribution (Table 4)", "demonstrates its unique contribution (Table 2)")
print("[5] Table 4 -> Table 2")

# ====== FIX 6: De-duplicate K562 discussion in 4.1 vs 4.3 ======
# In 4.1, remove the K562 constraint paragraph (it belongs in 4.3)
old_k562_41 = """RA-PainKG serves three primary use cases. First, as a queryable knowledge base: researchers can extract pathway subnetworks (all nine curated pain pathways), identify drugs targeting specific pain genes, and retrieve tissue expression profiles for pain genes across 54 human tissues. Second, as a hypothesis-generation tool: the dual-track framework enables systematic comparison of inflammatory versus nociceptive mechanisms, and bridge genes (STAT3, RELA, NF-kappaB complex) connecting both tracks represent candidate intervention points where anti-inflammatory and analgesic effects may converge. Third, as prior knowledge for machine learning: the graph provides structured domain knowledge for downstream applications including gene perturbation prediction, drug repurposing, and causal mediator identification."""
new_k562_41 = """RA-PainKG serves three primary use cases. First, as a queryable knowledge base: researchers can extract pathway subnetworks (all nine curated pain pathways), identify drugs targeting specific pain genes, and retrieve tissue expression profiles across 54 human tissues. Second, as a hypothesis-generation tool: the dual-track framework enables systematic comparison of inflammatory versus nociceptive mechanisms, and bridge genes (STAT3, RELA, NF-kappaB complex) connecting both tracks represent candidate intervention points. Third, as structured prior knowledge for machine learning: the graph provides domain-specific features for gene perturbation prediction, drug repurposing pipelines, and causal mediator identification. Transparent benchmark validation (Section 4.3) establishes the boundary conditions under which each use case applies."""
c = c.replace(old_k562_41, new_k562_41)
print("[6] Removed K562 redundancy from 4.1")

# ====== FIX 7: Fix abstract encoding "57每100%" -> "57-100%" =====
c = c.replace("57每100%", "57-100%")
# Also fix other encoding artifacts
c = c.replace("每", "-")
c = c.replace("〞", "\u201D")
print("[7] Fixed abstract encoding")

# ====== FIX 8: Add Setup section to Usage Examples =====
old_usage_intro = "RA-PainKG is designed for programmatic access via Python (NetworkX). Below are three representative use cases. All code is available in the GitHub repository."
new_usage_intro = """RA-PainKG is designed for programmatic access via Python (NetworkX). Below are four representative use cases. All code is available in the GitHub repository.

**Setup.** Download RA_PainKG_final.pkl from the GitHub repository and place it in your working directory:

```python
import pickle
import networkx as nx

with open("RA_PainKG_final.pkl", "rb") as f:
    G = pickle.load(f)
```

All subsequent examples assume `G` is loaded and `networkx` is imported as `nx`."""
c = c.replace(old_usage_intro, new_usage_intro)

# Fix variable names in examples to use G consistently
c = c.replace("""```python
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
print(ptgs2_drugs)""", """```python
# Find all drugs targeting PTGS2 (COX-2)
ptgs2_drugs = []
for node, data in G.nodes(data=True):
    if str(data.get("node_name", "")).upper() == "PTGS2":
        for pred in G.predecessors(node):
            if G.nodes[pred].get("node_type") == "drug":
                ptgs2_drugs.append((G.nodes[pred]["node_name"],
                                    G[pred][node].get("relation")))
print(ptgs2_drugs)""")

c = c.replace("""```python
# Extract the opioid signaling subnetwork
opioid_genes = {"OPRM1", "OPRD1", "OPRK1", "POMC", "PENK", "PDYN"}
opioid_nodes = {n for n, d in g.nodes(data=True)
                if str(d.get("node_name", "")).upper() in opioid_genes}
subgraph = g.subgraph(opioid_nodes)
import networkx as nx
nx.write_graphml(subgraph, "opioid_pathway.graphml")""", """```python
# Extract the opioid signaling subnetwork
opioid_genes = {"OPRM1", "OPRD1", "OPRK1", "POMC", "PENK", "PDYN"}
opioid_nodes = {n for n, d in G.nodes(data=True)
                if str(d.get("node_name", "")).upper() in opioid_genes}
subgraph = G.subgraph(opioid_nodes)
nx.write_graphml(subgraph, "opioid_pathway.graphml")""")

c = c.replace("""```python
# Retrieve GTEx tissue expression for all Track B pain genes
track_b_genes = [d["node_name"] for _, d in g.nodes(data=True)
                 if d.get("track") == "B" and d.get("node_type") == "gene/protein"]
for gene in track_b_genes[:5]:
    expr = d.get("gtex_median_tpm", {})
    spinal_cord = expr.get("Spinal_Cord_cervical_c-1", "N/A")
    tibial_nerve = expr.get("Nerve_Tibial", "N/A")
    print(f"{gene}: Spinal={spinal_cord}, Tibial={tibial_nerve}")""", """```python
# Retrieve GTEx tissue expression for all Track B pain genes
for node, data in G.nodes(data=True):
    if data.get("track") == "B" and data.get("node_type") == "gene/protein":
        gene = data["node_name"]
        expr = data.get("gtex_median_tpm", {})
        spinal = expr.get("Spinal_Cord_cervical_c-1", "N/A")
        tibial = expr.get("Nerve_Tibial", "N/A")
        print(f"{gene}: Spinal={spinal}, Tibial={tibial}")""")

c = c.replace("""```python
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
top_bridges = sorted(bridge_scores.items(), key=lambda x: x[1], reverse=True)[:10]""", """```python
# Find genes connecting Track A and Track B in the PPI subgraph
track_a = {n for n, d in G.nodes(data=True) if d.get("track") == "A"}
track_b = {n for n, d in G.nodes(data=True) if d.get("track") == "B"}
ppi = [(u, v) for u, v, d in G.edges(data=True)
       if d.get("relation") == "protein_protein"]
scores = {}
for u, v in ppi:
    if u in track_a and v in track_b:
        scores[u] = scores.get(u, 0) + 1
        scores[v] = scores.get(v, 0) + 1
top_bridges = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]""")

print("[8] Added Setup section; fixed variable names (g->G, d scoping)")
print("[9] Fixed variable 'd' scoping in Usage 5.3")

# ====== FIX 10: Add Figure Captions section ======
fig_captions = """

---

## Figure Captions

**Figure 1.** Top 20 hub nodes ranked by betweenness centrality in RA-PainKG. Node size is proportional to betweenness score.

**Figure 2.** Degree distribution of RA-PainKG (log-log scale) with power-law fit. The scale-free topology is characteristic of biological networks.

**Figure 3.** Comparison of centrality distributions between Track A (immune-inflammation) and Track B (nociception-pain transduction) gene subsets.

**Figure 4.** Node type composition and edge relation distribution in RA-PainKG. The graph spans 10 entity types and 24 relation types.

**Figure 5.** Core signaling network visualization showing the top 50 hub nodes and their interconnections. Node color indicates track assignment.

**Figure 6.** Pathway subnetwork visualizations for nine curated pain signaling pathways mapped onto RA-PainKG.
"""
# Insert before ## AI Usage Statement
c = c.replace("\n## AI Usage Statement", fig_captions + "\n## AI Usage Statement")
print("[10] Added Figure Captions section")

# ====== FIX 11: Remove duplicate title (L7) ======
c = c.replace("""---

# RA-PainKG: Construction, Coverage-Gap Documentation, and Benchmark Validation of a Tissue-Contextualized Knowledge Graph for Rheumatoid Arthritis Pain Signaling

**Yongxin Yang**<sup>1,*</sup>""", """---

**Yongxin Yang**<sup>1,*</sup>""")
print("[11] Removed duplicate title")

# ====== FIX 12: Fix entity type name ======
c = c.replace("effect/phenotype", "phenotype")
print("[12] Fixed entity type: effect/phenotype -> phenotype")

# ====== EXTRA: Fix any remaining encoding issues =====
# Fix em-dash rendering
c = c.replace("\u2014", "--")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(c)
print("\n[DONE] All 12 fixes applied")