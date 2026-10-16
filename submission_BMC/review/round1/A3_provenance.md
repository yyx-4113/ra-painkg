# Reviewer A3 — Implementation & Provenance Audit

**Manuscript:** `submission_BMC/manuscript_BMC.md` (+ `manuscript_BMC.docx`, `submission_BMC/supplementary/supplementary_tables.docx`)
**Source of truth recomputed from:** `output/RA_PainKG_summary.json`, `output/graph_statistics.json`, `output/RA_PainKG_nodes.csv`, `output/RA_PainKG_edges.csv`, `output/seed_nodes.csv`, `output/track_assignments.csv`, `output/RA_PainKG_nodes_final.csv`, `benchmark/results/*`, `src/ra_painkg/config.py` (`CORE_PAIN_GENES`).
**Method:** every headline number below was independently recomputed in Python (pandas 3.0.5) from the raw CSV/JSON artifacts, not from the manuscript's arithmetic.

---

## CENTERPIECE — Cross-Verification Table

| # | Manuscript claim | Asserted | Recomputed from source | Verdict |
|---|-----------------|----------|-----------------------|---------|
| 1 | Present in final graph | 188/192 (97.9%) | 188/192 exact-symbol matches in `RA_PainKG_nodes.csv` (absent: ACPA, ADRA2B, NAPE-PLD, RANKL) → 97.9% | **MATCH (as graph presence)** — but see F1 |
| 2 | Exact-symbol match to PrimeKG | 189/192 (98.4%) | 188 present in final graph; ADRA2B matches PrimeKG exactly but is dropped → 189 in PrimeKG, 188 retained; 189/192 = 98.4% | **MATCH (with caveat)** |
| 3 | Seed gene nodes | 190 | `seed_nodes.csv` gene/protein rows = **191** (no dupes); `summary.json`/`graph_statistics.json` = 190 | **MISMATCH (190 stated vs 191 in data)** — see F3 |
| 4 | 2-hop expansion added 45 → 165 annotated | 45 / 165 | `track_assignments.csv` = 165 rows = **120 curated + 45 non-curated (expansion)** | **MATCH (composition)** — but see F1 |
| 5 | Track A 106 / Track B 122 / 96 overlap; 96/165 = 58.2% | 106/122/96; 58.2% | 106/122/96; 96/165 = 58.18% | **MATCH** |
| 6 | 18,069 nodes / 10 entity types | 18,069 / 10 | `RA_PainKG_nodes.csv` = 18,069 nodes; 10 types | **MATCH** |
| 7 | 127,226 edges / 24 relation types | 127,226 / 24 | `RA_PainKG_edges.csv` = 127,226 rows; 24 distinct relations | **MATCH** |
| 8 | 4,760 drug–target edges | 4,760 | `drug_protein` = 4,760 | **MATCH** |
| 9 | 2,400 PPI + 124,826 non-PPI = 127,226 | 2,400 PPI | Full graph `protein_protein` = **28,972** (also `summary.json`); 2,400 = benchmark PPI-only variant (Table S1) | **MISMATCH — internal contradiction** — see F2 |
| 10 | 44/165 (26.7%) overlap Norman vocabulary | 44/165 = 26.7% | 44/165 = 26.67% | **MATCH** |
| 11 | 1,600/5,045 (31.7%) have ≥1 RA-PainKG edge | 1,600/5,045 = 31.7% | `benchmark_real.json`: `kg_genes_matched` = 1,600; 1,600/5,045 = 31.71% | **MATCH** |
| 12 | Densities: GO-BP 0.0265, GO-painCentric 0.0048, RA-PainKG 0.00009 | as stated | From Table S1 edge counts & N=5,045 directed density: 0.02648 / 0.00478 / 9.4e-05 | **MATCH (benchmark-adjacency densities)** |
| 13 | Multi-split r: RA-PainKG 0.503 vs GO 0.542; seed-42 0.558 vs 0.481 | as stated | `benchmark_multisplit_summary.json`: GO r_pain 0.5422, RA-PainKG 0.5032; `benchmark_multisplit.csv` seed 42: GO 0.4811, RA-PainKG 0.5578 | **MATCH** |
| 14 | K562 91,205 cells / 5,045 genes / 284 conditions | as stated | External dataset (`perturb_processed.h5ad` not in repo) | **UNVERIFIABLE here** (cited) |
| 15 | K562 59.1% (26/44) pain genes mean expr <0.01 | 26/44 = 59.1% | `k562_pain_expr.csv`: 26/44 = 59.09% | **MATCH** |
| 16 | K562 mean pain-gene expr 0.117 vs background 0.107 | 0.117 vs 0.107 | `k562_pain_expr.csv` mean of 44 = 0.1173 ✓; background 0.107 | **PARTIAL (0.117 verified; 0.107 not in provided files)** |
| 17 | 280-fold sparsity | 280× | 673,899 / 2,400 = 280.8 (benchmark PPI counts) | **MATCH (benchmark framing)** |
| 18 | STRING v12 r = 0.000 | 0.000 | Table S1/S2/S3 and `benchmark_results.json`: STRING r = 0.000 | **MATCH** |
| 19 | Top-5 hubs EGR1/FOS/STAT3/AKT1/SRC | as stated | `RA_PainKG_nodes_final.csv` betweenness: EGR1 0.195, FOS 0.146, STAT3 0.098, AKT1 0.085, SRC 0.080 (JUN is 6th) | **MATCH** |
| 20 | 4 "non-recovered" genes ACPA/NAPE-PLD/RANKL/ADRA2B | 4 | ACPA absent; NAPE-PLD→**NAPEPLD present**; RANKL→**TNFSF11 present**; ADRA2B absent from final graph | **PARTIAL — labeling inconsistency** — see F4 |
| 21 | 50% of Track B zero PPI vs 20% of Track A | 50% / 20% | Induced 165-gene PPI subgraph: B_only 13/26 = 50.0%, A_only 2/10 = 20.0% | **MATCH (induced-subgraph reading)** |
| 22 | 192 curated genes = 120 core + 45 expansion (supplementary caption) | 120 + 45 | `track_assignments.csv`: 120 curated + 45 expansion = 165 | **MATCH (confirms F1 composition)** |

---

## Detailed Findings (Problem / Evidence / Why it matters / Specific fix)

### F1 — The headline "188/192 (97.9%) present" is internally inconsistent with the resource's own annotated gene set, which contains only 120/192 (62.5%) curated genes

**【Problem】** The manuscript reports near-complete curated-gene recovery (188/192 present, 189/192 matched), but the actual analyzed/annotated gene set of 165 contains only 120 of the 192 curated genes; the other 68 curated genes present in the graph are excluded from the 165-gene dual-track / tissue-expression / benchmark analysis.

**【Evidence】** `src/ra_painkg/config.py` `CORE_PAIN_GENES` → 192 unique curated symbols. `track_assignments.csv` has 165 rows; intersection with the 192 curated set = **120** curated genes, and **45** non-curated (expansion) genes (120 + 45 = 165, also stated verbatim in `supplementary_tables.docx`: "165 genes … (120 curated core genes + 45 expansion-discovered)"). Of the 192 curated genes, 188 are present in `RA_PainKG_nodes.csv` by exact symbol (absent: ACPA, ADRA2B, NAPE-PLD, RANKL); the 68 curated genes not in the 165 set are still present in the full 18,069-node graph (188 − 120 = 68). So "188/192 present" is true *for graph presence* but the **annotated/usable** set covers only 120/192 = 62.5% of curated genes. The "62.5%" figure from the retracted draft re-surfaces here.

**【Why it matters】** This is the manuscript's central credibility claim. A reader inferring that ~98% of the 192 curated pain genes are delivered as annotated pain genes is wrong: only 62.5% are. Reviewers and future users will over-trust the resource's curated-gene coverage. It also contradicts the supplementary caption, which still encodes the old 120+45 arithmetic.

**【Specific fix】**
> "Of 192 curated genes, 188 (97.9%) are present in the final RA-PainKG graph and 189/192 (98.4%) matched PrimeKG symbols exactly; however, the 165-gene dual-track annotated set comprises 120 of these recovered curated genes plus 45 expansion-discovered genes, so 68 curated genes present in the graph were not carried into the annotated/track-assigned set. We report 188/192 as graph-level recovery and 120/192 (62.5%) as curated-gene coverage of the annotated set."

Reconcile the supplementary caption to state this explicitly rather than "120 curated core genes + 45 expansion-discovered" as if that were the whole story.

### F2 — Stage 3 states 2,400 protein–protein edges, contradicting the manuscript's own Table 3.3 (28,972) and `summary.json`

**【Problem】** Methods Stage 3 writes "2,400 protein–protein interaction edges and 124,826 non-PPI edges … Graph statistics: 18,069 nodes … and 127,226 directed edges." The 2,400 figure does not belong to the full resource graph.

**【Evidence】** `RA_PainKG_edges.csv` relation tally: `protein_protein` = **28,972** (also `RA_PainKG_summary.json` edge_relation_distribution and Table 3.3 and `supplementary_tables.docx` edge table all list 28,972, 22.8%). The 2,400 value is the **benchmark PPI-only variant** (`benchmark/results/supplementary_table_S1.md` row "RA_PainKG | 2,400"). Correct decomposition of the full graph is 28,972 PPI + 98,254 non-PPI = 127,226; the manuscript's 124,826 non-PPI is therefore wrong. 2,400 + 124,826 = 127,226 is arithmetically consistent only because both addends are wrong.

**【Why it matters】** An internal contradiction within the same manuscript (Stage 3 vs Table 3.3) is a red flag for provenance and will be caught by any careful reviewer; it also misrepresents the actual PPI content of the released graph by ~12×.

**【Specific fix】** Either (a) change Stage 3 to "28,972 protein–protein interaction edges (22.8% of all edges) and 98,254 non-PPI edges," or (b) if the intent was to describe the PPI-only *benchmark* subgraph, move/label that sentence as "In the PPI-only benchmark variant, 2,400 PPI edges were used (cf. Table S1)." Do not leave the current conflated sentence.

### F3 — "190 seed gene nodes" vs 191 in `seed_nodes.csv` (and the 190↔165 derivation is unclear)

**【Problem】** The manuscript states 190 seed gene nodes, but the seed artifact contains 191 gene/protein rows, and the relationship between 190 seeds, 45 expansion genes, and the 165 annotated set is not cleanly derivable.

**【Evidence】** `output/seed_nodes.csv` gene/protein rows = **191** (no duplicate names). `RA_PainKG_summary.json` and `graph_statistics.json` both report `pain_gene_protein`/`pain_gene_nodes` = 190. So the pipeline's own summary (190) disagrees with its own seed table (191). Separately, the 165 annotated set = 120 curated + 45 expansion (F1), which is not "190 seeds + 45 expansion" (that would be 235).

**【Why it matters】** Minor but real provenance inconsistency between stated value and deposited artifact; also the seed→annotated derivation is opaque, undermining reproducibility.

**【Specific fix】** Reconcile to a single number: state that 190 (or 191) gene/protein seed nodes were identified, and explicitly derive 165 = (recovered curated genes carried into the annotated set, i.e., 120) + 45 expansion-discovered, clarifying that the remaining recovered curated genes (68) remain in the graph but outside the annotated set.

### F4 — Labeling NAPE-PLD and RANKL as "non-recoveries" is self-contradictory because both are present under aliases

**【Problem】** The manuscript lists "4 non-recovered genes: ACPA, NAPE-PLD, RANKL, ADRA2B" and simultaneously states NAPE-PLD "resolves to NAPEPLD" and RANKL "resolves to TNFSF11."

**【Evidence】** `RA_PainKG_nodes.csv` contains node_name **NAPEPLD** and **TNFSF11** (confirmed present), but not the literal strings "NAPE-PLD"/"RANKL". ACPA is not a gene symbol (correctly absent). ADRA2B is absent from the final graph (construction artifact; PrimeKG presence could not be verified here because `data/prime_kg.csv` is absent from the repository). So, of the 4, only 2 (ACPA, ADRA2B) are genuinely unrepresented; NAPE-PLD and RANKL ARE represented under aliases. The "4 non-recoveries" label therefore conflicts with the alias-resolution statement two sentences earlier, and with the 188/192 "present" count.

**【Why it matters】** Double-counting alias-resolved genes as both "recovered via alias" and "non-recovered" is logically inconsistent and inflates the apparent gap documentation.

**【Specific fix】**
> "Two curated genes are genuinely unrepresented in the final graph: ACPA (an autoantibody marker, not a gene symbol) and ADRA2B (present in PrimeKG but not retained). Two further symbols, NAPE-PLD and RANKL, are recovered under their HGNC identifiers NAPEPLD and TNFSF11 and are therefore represented; they are listed only to document the symbol/alias mapping."

### F5 — Residue of the retracted "120/62.5%" framing in the new manuscript

**【Problem】** Although the body no longer states "120 (62.5%)" or "72 missing," a stray "120" and the old 120+45 arithmetic persist.

**【Evidence】** `manuscript_BMC.md:80`: "Within the **120** core genes that received dual-track annotations, 50% of Track B…" — the number 120 is a leftover from the prior draft and is meaningless here (there are 96 dual-track genes; 165 annotated). `supplementary_tables.docx` caption: "165 genes … (**120** curated core genes + 45 expansion-discovered)." The 50%/20% claim itself verifies (F-below), but the "120" wording is a residue.

**【Why it matters】** Stray numbers from a retracted analysis undermine confidence that the revision was copy-edited against the new arithmetic.

**【Specific fix】** Remove "Within the 120 core genes that received dual-track annotations" and replace with "Within the annotated gene set, …". Confirm the supplementary caption is re-phrased per F1.

### F6 — K562 genome-wide background expression (0.107) cannot be recomputed from deposited files

**【Problem】** The manuscript compares mean pain-gene expression (0.117) to a genome-wide background (0.107); the 0.107 is not reproducible from any provided artifact.

**【Evidence】** `k562_pain_expr.csv` contains only the 44 pain genes (mean = 0.1173, verified). The full normalized K562 expression matrix / the 0.107 statistic is not in the repository (only `perturb_processed.h5ad` is cited as external, 2.2 GB).

**【Why it matters】** The "comparable to background" conclusion depends on an unverifiable number; if the background is computed differently it could change the interpretation.

**【Specific fix】** Deposit the code + the exact gene list and subset used to compute the 0.107 background (and its SD), or state the precise subset (e.g., all 5,045 Norman genes' mean log-normalized expression) so it is reproducible.

### F7 (informational) — "50% of Track B / 20% of Track A zero PPI" is CORRECT under the induced 165-gene PPI subgraph

For transparency (this claim was a specific audit target): recomputing the PPI degree of the 165 genes inside the **induced 165-gene PPI subgraph** (both endpoints in the 165; 390 undirected edges, matching `kg_structural_analysis.json`) gives B_only zero-PPI = 13/26 = **50.0%** and A_only zero-PPI = 2/10 = **20.0%** — exactly as stated. (Under a "any PPI edge anywhere in the 18,069-node graph" reading it would be 0%/3.8%, so the claim is valid only if "PPI subgraph" means the induced 165-gene PPI subgraph; the text should state this.)

---

## § Stands up (verified correct against source)

1. Graph scale is exactly right: **18,069 nodes / 10 types**, **127,226 edges / 24 relation types**, **4,760 drug–target (drug_protein) edges** — recomputed from `RA_PainKG_nodes.csv`/`RA_PainKG_edges.csv`.
2. Dual-track counts are exact: **Track A 106, Track B 122, dual 96 (96/165 = 58.2%)** — recomputed from `track_assignments.csv` and `summary.json`.
3. Benchmark statistics are reproducible: multi-split r_pain **GO 0.542 vs RA-PainKG 0.503**, seed-42 **0.481 vs 0.558**; densities **0.0265 / 0.0048 / 0.00009**; **1,600/5,045 (31.7%)** from `benchmark_real.json`; STRING r = 0.000; K562 **26/44 = 59.1%**; mean pain-gene expr **0.117**.
4. Top-5 hubs **EGR1, FOS, STAT3, AKT1, SRC** confirmed from the deposited betweenness column (`RA_PainKG_nodes_final.csv`), correctly excluding JUN (6th) — an improvement over the prior draft.
5. Recovery arithmetic at graph level is internally consistent: 188/192 present, 189/192 exact-match-in-PrimeKG, absent set = {ACPA, ADRA2B, NAPE-PLD, RANKL}.

## § Questions for the authors

1. Given that the 165-gene annotated set contains only **120 of the 192 curated genes** (the remaining 68 curated genes are present in the graph but outside the annotated set), how should readers interpret "188/192 (97.9%) present"? Should the abstract/Results state the 62.5% annotated-set coverage explicitly?
2. Why does Methods Stage 3 report **2,400** PPI edges when Table 3.3, `summary.json`, and the supplementary edge table all report **28,972**? Was the benchmark PPI-only variant (2,400) mistakenly placed in the resource description?
3. `seed_nodes.csv` contains **191** gene/protein seed rows while the text and `summary.json` say **190** — which is authoritative, and what is the 165 = f(seeds, expansion) derivation?
4. NAPE-PLD and RANKL are present under aliases (NAPEPLD, TNFSF11). Should they be counted as recovered (making 190/192 represented) rather than as "non-recoveries"?
5. Can you deposit the exact code/subset used to compute the K562 genome-wide background mean expression (**0.107**) and SD so that the "comparable to background" claim is reproducible?

## § What I actually checked

**Files read (source of truth):** `submission_BMC/manuscript_BMC.md`, `submission_BMC/manuscript_BMC.docx`, `submission_BMC/supplementary/supplementary_tables.docx`, `output/RA_PainKG_summary.json`, `output/graph_statistics.json`, `output/RA_PainKG_nodes.csv`, `output/RA_PainKG_nodes_final.csv`, `output/RA_PainKG_edges.csv`, `output/seed_nodes.csv`, `output/track_assignments.csv`, `benchmark/results/benchmark_results.json`, `benchmark/results/benchmark_multisplit_summary.json`, `benchmark/results/benchmark_multisplit.csv`, `benchmark/results/supplementary_table_S1–S5.md`, `benchmark/results/benchmark_real.json`, `benchmark/results/kg_structural_analysis.json`, `benchmark/results/k562_pain_expr.csv`, `src/ra_painkg/config.py` (`CORE_PAIN_GENES`).

**Commands/computations run:** Python (C:/Python314/python.exe, pandas 3.0.5) recomputed — total edges/nodes and relation/type tallies from the CSVs; intersection of the 192 `CORE_PAIN_GENES` with `RA_PainKG_nodes.csv` names (exact, case-insensitive) → 188 present, absent = {ACPA, ADRA2B, NAPE-PLD, RANKL}; track-assignment counts and Track-A/B/dual/only/none; overlap of the 165 track genes with the 192 curated → 120 curated + 45 expansion; induced 165-gene PPI zero-degree for A_only/B_only; K562 44-gene mean and <0.01 count; directed densities from Table S1 edge counts at N=5,045; multi-split r from `benchmark_multisplit_summary.json` and seed-42 row of `benchmark_multisplit.csv`; top-5 betweenness from `RA_PainKG_nodes_final.csv`; `kg_genes_matched`=1600 from `benchmark_real.json`; presence of NAPEPLD/TNFSF11/ADRA2B in nodes.

**Discrepancies / things I could not recompute:** (a) `data/prime_kg.csv` is absent, so the claim "ADRA2B is present in PrimeKG" and "189 exact matches in PrimeKG" could not be verified directly (the 188 present in the final graph and the ADRA2B-drop logic are consistent with it); (b) K562 genome-wide background 0.107 and the dataset facts 91,205 cells / 5,045 genes / 284 conditions are external (`perturb_processed.h5ad` not in repo) and were accepted as cited, not recomputed.

**Files I did NOT read (per independence rules):** any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `SUBMISSION_MANIFEST.md`, `REVISION_NOTE.md`, `cover_letter.md`, `declarations.md`, anything under `submission_BMC/review/`, and any `*_gen_*.py`.
