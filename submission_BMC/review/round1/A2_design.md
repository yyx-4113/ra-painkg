# Independent Review — A2 (Design & Statistical Methodology)

**Manuscript:** RA-PainKG: a tissue-contextualized knowledge graph for rheumatoid arthritis pain signaling with benchmark validation
**Reviewer role:** Network-science / benchmark-design / leakage & statistical-inference expert
**Scope of this report:** design-layer defects only (double-dipping/leakage, centrality robustness, benchmark statistics, fairness of comparisons, unsupported conclusion). I did not review biological novelty, clinical claims, or writing quality except where they bear on design validity.

**Headline verdict:** The benchmark as designed cannot support any claim that RA-PainKG is a useful prior for perturbation prediction, because (a) the evaluated genes are the construction genes, (b) the comparator baselines are evaluated on different gene universes, (c) random graphs beat the curated graph, and (d) the curated edges are statistically indistinguishable from a random rewiring. The central "benchmark validation" section measures an artifact, not generalizability.

---

## DESIGN DEFECTS (each with Problem / Evidence / Why-it-matters / Specific-fix)

### D1. CRITICAL — The benchmark evaluates on the genes RA-PainKG was built from (train/test circularity)

- **【Problem】** RA-PainKG is constructed from the 165 curated/annotated pain genes, yet the benchmark's evaluation gene set is exactly those same 165 genes, so the graph features used to predict a gene's perturbation response were derived from a graph whose edges were built *using that same gene*.
- **【Evidence】** `benchmark/results/gene_vocab.csv` contains 265 genes = 165 pain genes (identical to `output/track_assignments.csv`, confirmed by set overlap 165/165) + 100 `CTRL_*` genes. Cross-referencing the 265-gene vocabulary against `RA_PainKG_edges.csv`/`RA_PainKG_nodes.csv`: **165/165 pain genes have ≥1 edge in RA-PainKG; 0/100 CTRL genes have any edge.** `predictions_RA-PainKG.npy` is shape (411, 265) — i.e., the RA-PainKG evaluation is over these 265 genes. The 100 CTRL genes are isolated nodes with zero embedding and contribute no graph signal.
- **【Why it matters】** This is unambiguous double-dipping. The 2,400 PPI edges of RA-PainKG connect precisely the 165 construction genes (manuscript line 43: "All PrimeKG edges involving the 165 annotated genes were retained: 2,400 … PPI edges"). Predicting perturbation effects of those genes from an embedding of a graph built *around* those genes reconstructs curated co-annotation rather than testing generalization to unseen biology. The benchmark therefore cannot validate the resource; it validates the curation loop.
- **【Specific fix】** Re-run the benchmark in a held-out (inductive) regime: (i) remove all 165 RA-PainKG construction genes from the graph, embed, and predict only on those held-out genes; or (ii) use leave-one-gene-family / disease-module-out cross-validation. Report performance **only on genes not used to build the graph**. Until then, any statement that the benchmark "validates" RA-PainKG must be removed.

### D2. CRITICAL — RA-PainKG and GO are benchmarked on different gene universes, invalidating the headline comparison

- **【Problem】** The manuscript compares RA-PainKG vs GO as if both are evaluated on the same 5,045-gene Norman set, but the posted prediction arrays show the two variants were run on different gene counts, so their `r_all` values are not comparable.
- **【Evidence】** `predictions_RA-PainKG.npy` = (411, **265**); `predictions_GO-BP_original_GEARS.npy` = (1072, **2000**); `predictions_STRING_v12.npy` = (1072, 2000); `predictions_Random_same_density.npy` = (1072, 2000); `predictions_Random.npy` / `predictions_Identity.npy` = (411, 265). RA-PainKG/Random/Identity were evaluated on 265 genes; GO-BP/STRING/density-matched-random on 2,000 genes. The manuscript ("adjacency matrices for 5,045 Norman genes", lines 49, 86) claims a third, larger number never realized in the posted artifacts.
- **【Why it matters】** Pearson `r` aggregated over 265 vs 2,000 genes measures different quantities and is not a valid paired contrast. The reported "RA-PainKG 0.551 vs GO 0.589" (multi-split) and the S4 paired t-test (GO vs RA_PainKG, p=0.0842 ns) are therefore computed on mismatched gene sets and are not interpretable.
- **【Specific fix】** Evaluate **every** KG variant on the *identical* gene set (the intersection of genes present in all graphs, or a fixed 5,045-gene matrix actually constructed for all variants). Recompute all pairwise comparisons on that common set and re-tabulate S4/S5.

### D3. CRITICAL — The fair comparator (GO-painCentric) already beats RA-PainKG on pain genes, but the manuscript hides it

- **【Problem】** The only legitimate "domain-focused vs domain-focused" comparison is RA-PainKG vs GO-painCentric (both restricted to pain-gene endpoints), and GO-painCentric wins — yet the Results/Discussion headline only the genome-wide GO contrast.
- **【Evidence】** `benchmark_jbi.csv` (10-split means): `r_pain` = **GO_painCentric 0.5234** > **RA_PainKG 0.5032**; `r_all` = GO_painCentric 0.6035 > RA_PainKG 0.5512. GO_painCentric is a GO-BP subgraph restricted to edges with ≥1 pain-gene endpoint (manuscript line 49), i.e., the correct apples-to-apples baseline. STRING also beats RA-PainKG on pain genes (`r_pain` = 0.5586 vs 0.5032) despite the manuscript asserting STRING gave "zero predictive signal" (see D6).
- **【Why it matters】** A reader is led to believe RA-PainKG is competitive with GO; the data actually show a *pain-focused* GO subgraph, built with no manual curation, outperforms the manually curated RA-PainKG. This reverses the paper's implied claim of added value.
- **【Specific fix】** Replace the GO-vs-RA-PainKG headline with the GO-painCentric-vs-RA-PainKG contrast and state plainly that the pain-focused GO subgraph matches or exceeds RA-PainKG on pain-gene prediction. Add GO-painCentric to S4 with its own paired test against RA-PainKG.

### D4. CRITICAL — Random graphs outperform the curated knowledge graph (benchmark lacks construct validity)

- **【Problem】** Five random-graph realizations predict perturbation effects better than both GO and RA-PainKG, which is impossible if the benchmark measured biologically meaningful graph structure.
- **【Evidence】** `benchmark_jbi.csv` 10-split means: `r_all` Random_1..5 = 0.640–0.667; `r_pain` = 0.570–0.620. These exceed GO (0.589 / 0.542) and RA-PainKG (0.551 / 0.503) in **every** realization. (S4 confirms Random_R1 > GO and Random_R1 > RA_PainKG at p<0.0001.)
- **【Why it matters】** A randomly wired graph contains no pain biology, yet wins. This indicates the benchmark's `r` is driven by a graph property unrelated to curation — most likely edge count / node degree / embedding norm correlating with perturbation-effect magnitude — not by the *identity* of curated edges. The benchmark therefore has no construct validity for ranking knowledge graphs.
- **【Specific fix】** Report a **density-matched** random baseline (a random graph with the same number of edges / same degree sequence as RA-PainKG; `predictions_Random_same_density.npy` exists but is absent from every reported table — see D5) and show RA-PainKG's `r` against it. Until RA-PainKG beats a density-matched random graph, no statement about KG "quality" is supportable.

### D5. HIGH — RA-PainKG is statistically indistinguishable from a random rewiring; the one decisive control is omitted from tables

- **【Problem】** The degree-preserving rewiring ablation shows RA-PainKG's *specific* curated edges add nothing beyond its degree distribution, and the single most informative control (density-matched random) is computed but never reported.
- **【Evidence】** `benchmark_jbi.csv`: `r_all` KG_degPreserved = 0.5459 vs RA_PainKG = 0.5512 (Δ +0.005, S4: p=0.8268 ns); `r_pain` 0.4835 vs 0.5032 (p=0.4088 ns). So the curated edge identity is not distinguishable from a random rewiring preserving degrees. Separately, `predictions_Random_same_density.npy` exists (1072×2000) but `benchmark_jbi.csv` contains only Random_1..5 (which are at GO density, not RA-PainKG density) — the density-matched random is missing from S4/S5/summary.
- **【Why it matters】** The honest reading of the authors' own ablations is that RA-PainKG's edges carry no predictive signal beyond their degree sequence, and that a same-density random graph is the correct null. Omitting the density-matched random from reporting conceals the strongest evidence that RA-PainKG adds nothing over noise.
- **【Specific fix】** Add `Random_same_density` (and, ideally, 5 such realizations) to `benchmark_jbi.csv` and S4/S5, with a paired test of RA-PainKG vs density-matched-random. State explicitly whether RA-PainKG exceeds the density-matched null.

### D6. HIGH — Text contradicts posted data on the STRING variant (integrity inconsistency)

- **【Problem】** The manuscript states the STRING variant "yielded zero predictive signal (r = 0.000 on all subsets)" due to mapping ambiguity, but the repository's own benchmark table shows STRING performing well.
- **【Evidence】** Manuscript line 49: "STRING PPI v12 … yielded zero predictive signal (r = 0.000 on all subsets)." Yet `benchmark_jbi.csv` reports STRING `r_all` = 0.5886, `r_pain` = 0.5586 (10-split means) — higher than RA-PainKG on pain genes. `predictions_STRING_v12.npy` is (1072, 2000), confirming it was run and scored.
- **【Why it matters】** Either the reported STRING result is wrong or the manuscript text is wrong; both are unacceptable. It also undermines the "ENSP mapping ambiguity" explanation and suggests unstable reporting between manuscript and artifacts.
- **【Specific fix】** Reconcile STRING: report its actual `r` from `benchmark_jbi.csv` in the text, or explain why the "r=0.000" run differs from the posted `predictions_STRING_v12.npy`. Remove the "zero predictive signal" sentence if the posted predictions are the intended result.

### D7. HIGH — The reported betweenness top-5 hubs are not robust to the k=500 sampling seed, and the seed is unreported

- **【Problem】** `network_analysis.py` reports a single top-5 betweenness hub list from k=500 approximated betweenness without reporting the sampling seed, variance, or confidence, yet the ranking is seed-sensitive and is partly driven by non-gene phenotype nodes the manuscript omits from the figure.
- **【Evidence】** `network_analysis.py:69-71`: `if n>5000: k=min(500,n); bc=nx.betweenness_centrality(self.graph, k=k, weight=None)`. Recomputing on the full 18,069-node / 127,226-edge graph with k=500 across three seeds: the **union of the top-5 across seeds = {AKT1, EGR1, FOS, HEADACHE, PAIN, SRC, STAT3}** — seven distinct nodes occupy the top-5 depending on seed. EGR1 and FOS are stable (top-5 in 3/3 seeds); **SRC appears in the top-5 in only 1/3 seeds** (best rank 3); and phenotype/effect nodes **HEADACHE and PAIN** rank *above* SRC in some seeds. The manuscript (Figure 1 caption, line 132) presents "EGR1, FOS, STAT3, AKT1, and SRC" as definitive, omits phenotype nodes, and never states the seed.
- **【Why it matters】** (a) Betweenness on this graph is materially shaped by high-degree disease/phenotype hubs (HEADACHE, PAIN), so "top gene hubs" is a misnomer — the true top-betweenness nodes are not all genes. (b) Reporting a single seed-dependent top-5 without a seed or stability interval is not defensible; SRC in particular is not a robust top-5 hub. (c) Figure 1 silently filters out phenotype hubs, biasing the reader toward a gene-only interpretation.
- **【Specific fix】** Report the exact `seed` used for `betweenness_centrality`, and additionally report the top-5 (or top-20) across ≥10 seeds with the frequency each node appears in the top-5 (e.g., "SRC: top-5 in 4/10 seeds"). Include phenotype/effect nodes in the ranking or explicitly state they were filtered and why. Better: compute exact betweenness on the gene-only subgraph (feasible) and use that for the gene-hub claim.

### D8. MEDIUM — The 280-fold sparsity / density comparison is apples-to-oranges across different gene universes

- **【Problem】** Density and edge-count comparisons between RA-PainKG, GO-painCentric, and GO-BP conflate two different things: edge semantics (PPI-only vs all-GO-co-annotation) and the gene universe each graph is sized over.
- **【Evidence】** Manuscript cites densities GO-BP 0.0265, GO-painCentric 0.0048, RA-PainKG 0.00009 and "280-fold sparser." These densities are computed over a 5,045×5,045 matrix, but RA-PainKG only has edges among 165 genes in the actual benchmark; its *effective* density over the 165 populated genes is 2400/(165·164) ≈ **0.089**, ~1000× larger than the reported 0.00009. GO-BP edges can connect any of 5,045 genes; RA-PainKG edges can only ever connect the 165 curated genes, so padding its matrix to 5,045 artificially deflates its density. (Reconstructed full-graph directed density = 0.00039, still reflecting the 18,069-node construction graph, not the benchmark matrix.)
- **【Why it matters】** The "280-fold sparser" framing implies RA-PainKG is information-poor relative to GO; in fact the sparsity is an artifact of sizing RA-PainKG's matrix to a genome it does not cover. It misleads the reader about the graph's actual connectivity among its target genes.
- **【Specific fix】** Report density computed over the *actual evaluated gene set* for each variant (e.g., RA-PainKG over its 165-gene populated block, GO-BP over its 2,000-gene set), and state explicitly that raw edge-count/density comparisons are not meaningful across graphs with different edge semantics and gene coverage. Drop the "280-fold sparser" headline or qualify it as "over the full 5,045-gene padding only."

### D9. MEDIUM — "Only 44/165 overlap the Norman vocabulary" contradicts the benchmark's own gene vocabulary

- **【Problem】** The manuscript states only 44 of 165 annotated genes overlap the Norman K562 vocabulary, but the posted benchmark vocabulary contains all 165 pain genes (165/165 with graph edges).
- **【Evidence】** Manuscript line 43: "Only 44 of 165 annotated genes (26.7%) overlap the Norman K562 Perturb-seq gene vocabulary." Counter-evidence: `gene_vocab.csv` lists all 165 curated pain genes; `RA_PainKG_edges.csv` confirms 165/165 of them have edges. The "44/165" figure is irreconcilable with the benchmark actually run. (Possibly "44" refers to pain genes expressed above threshold in K562 per S5, but that is a different statement and is not what the sentence says.)
- **【Why it matters】** This is a direct internal contradiction about the most important number in the leakage analysis. A reader cannot tell whether the benchmark used 44, 165, 265, 2,000, or 5,045 genes, which is the crux of D1–D2.
- **【Specific fix】** State precisely, in one place, the benchmark gene set actually used per variant (265 for RA-PainKG/Random/Identity; 2,000 for GO/STRING/density-matched-random per the npy shapes), and correct the "44/165 overlap" sentence to refer to K562 *expression* threshold, not vocabulary overlap.

### D10. MEDIUM — The conclusion "K562 performance reflects test-system limitations, not resource quality" is unsupported by the data

- **【Problem】** The Discussion (lines 86, 104, 108) attributes RA-PainKG's unimpressive benchmark to K562 being a mismatched test system, but the data point to a different cause: the benchmark lacks construct validity (random graphs win; curated edges ≈ random rewiring).
- **【Evidence】** The data show (i) random graphs beat RA-PainKG (D4); (ii) RA-PainKG ≈ degree-preserving random (D5); (iii) a pain-focused GO subgraph beats RA-PainKG (D3). None of these are explained by "K562 biology." A genuine test-system limitation would depress *all* KGs similarly or would show RA-PainKG underperforming only where K562 under-expresses pain genes — but the dominant signal is that graph *density/degree*, not *curation*, drives `r`.
- **【Why it matters】** The hedge lets the authors avoid the real null result (as a perturbation predictor, RA-PainKG's curated edges add no signal beyond a random graph of equal density). Presenting it as a "boundary condition" rather than a failed validation overstates the resource's utility.
- **【Specific fix】** Rewrite the conclusion to reflect what the benchmark actually shows: RA-PainKG's edge structure is not distinguishable from a density-matched random graph on this task, and the K562 result cannot be isolated from the benchmark's lack of construct validity. Either remove claims that the benchmark "validates" the resource, or restrict them to the recovery/documentation contributions.

### D11. LOW–MEDIUM — Multiple-comparison correction is under-specified and Kendall's W is the wrong emphasis

- **【Problem】** S4 claims Bonferroni at α=0.01 with m=5 "primary comparisons" but lists 14 pairwise tests; the correction does not cover all tests, and Kendall's W is emphasized over the more informative ordering result.
- **【Evidence】** `supplementary_table_S4.md`: header "Bonferroni-adjusted significance threshold: p < 0.01 (5 primary comparisons)" yet 14 rows of pairwise t-tests are presented. m=5 over 14 tests does not control family-wise error at 0.01 for the full table. Kendall's W (rank consistency across splits) is adequate as a consistency metric, but the substantive finding — the *stable* ordering Random > GO ≥ RA-PainKG, and GO-painCentric > RA-PainKG — is what matters and is under-discussed.
- **【Why it matters】** Under-correction inflates the chance of spurious significance among the 14 contrasts; more importantly, emphasizing consistency (W) distracts from the ordering, which contradicts the paper's narrative.
- **【Specific fix】** Either set m equal to the number of tests actually reported (or pre-register the 5 primary contrasts and label the rest as exploratory), or apply a correction covering all 14. Report the stable ordering explicitly and discuss its implication for the resource claim.

---

## § Stands up (aspects that are sound / worth keeping)

1. **Transparent per-gene recovery documentation** (Methods "Recovery and residual-gap analysis"; S3): the systematic, categorized documentation of which curated genes are recovered vs absent for identifier/construction reasons is a genuine, well-executed contribution and is independent of the flawed benchmark.
2. **Multi-split evaluation protocol** (10 × 80/20): the decision to average over 10 splits rather than report a single seed is methodologically correct and the seed-42 caveat (manuscript lines 88, 106) is a real and useful point — though it is presented as the *main* lesson when the deeper issues (D1–D5) are the actual problems.
3. **Degree-preserving rewiring ablation (KG_degPreserved)** was the right control to include; its result (D5) is informative even though the manuscript frames it as a minor "boundary condition" rather than the central negative finding it is.
4. **Reproducible, modular code**: `kg_builder.py` / `network_analysis.py` / `seed_nodes.py` / `track_assigner.py` are clear, config-driven, and the posted artifacts (edges, nodes, predictions, vocab, jbi) make independent recomputation possible — which is how the above discrepancies were found.

---

## § Questions for the authors

1. What is the **actual** benchmark gene set? The artifacts show 265 genes for RA-PainKG/Random/Identity and 2,000 for GO/STRING/density-matched-random, while the text claims 5,045. Please provide the exact gene list and count used for each variant and reconcile with "5,045 Norman genes."
2. Why are RA-PainKG and GO evaluated on **different gene counts** (265 vs 2,000)? Was `r_all` truly comparable across variants, and if not, how should the GO-vs-RA-PainKG contrast be interpreted?
3. `predictions_Random_same_density.npy` exists but **Random_same_density is absent from `benchmark_jbi.csv` and all tables** — what was its `r`, and why was it omitted?
4. The text says **STRING "yielded zero predictive signal (r = 0.000)"** but `benchmark_jbi.csv` reports STRING `r_all` = 0.589, `r_pain` = 0.559. Which is correct?
5. Reconcile **"44/165 overlap the Norman vocabulary"** with `gene_vocab.csv` containing all 165 pain genes (165/165 with graph edges). Does the benchmark evaluate on the construction genes?
6. For the betweenness top-5: **what `seed` was passed to `betweenness_centrality`?** Across seeds the top-5 includes phenotype nodes HEADACHE/PAIN and SRC is unstable (top-5 in only 1/3 seeds I tested). Were phenotype/effect nodes filtered from Figure 1, and if so, why?
7. Given that random graphs beat RA-PainKG and RA-PainKG ≈ its degree-preserving rewiring, **what positive evidence remains that RA-PainKG's curated edges improve perturbation prediction** beyond a density-matched random graph?

---

## § What I actually checked

**Manuscript:** `submission_BMC/manuscript_BMC.md` (full read), focusing on Methods/Benchmark/Results/Discussion lines cited above.

**Source code read:** `src/ra_painkg/network_analysis.py` (betweenness k=500 path at lines 66–76, `get_top_hubs`, `compare_tracks`), `kg_builder.py` (2-hop expansion, edge retention, subgraph extraction), `seed_nodes.py` (curated-gene seed identification), `track_assigner.py` (Track A/B assignment, manual overrides).

**Benchmark artifacts examined:**
- `benchmark/results/benchmark_multisplit.csv` (per-split r; verified means match `benchmark_multisplit_summary.json`: GO r_all 0.5892 / r_pain 0.5422; RA_PainKG 0.5512 / 0.5032; Random 0.6469 / 0.5750; seed-42 split0 confirms "0.558 vs 0.481" claim).
- `benchmark/results/benchmark_multisplit_summary.json`, `supplementary_table_S4.md` (paired t-tests), `supplementary_table_S5.md` (pain-gene K562 expression; EGR1 0.107, FOS 0.018, etc.).
- `benchmark/results/benchmark_jbi.csv` (11 variants; computed per-KG 10-split means for r_all/r_pain/r_nonpain/r_trackA/r_trackB/r_trackDual; identified GO_painCentric, KG_degPreserved, Random_1..5, STRING, and the absence of Random_same_density).
- `benchmark/results/gene_vocab.csv` (265 genes: 165 pain + 100 CTRL), `track_assignments.csv` (165), `benchmark_metadata.json`, `split_info.json`.
- `benchmark/results/predictions_*.npy`: shapes (411,265) for RA-PainKG/Random/Identity; (1072,2000) for GO-BP/Random_same_density/STRING — establishing the mismatched gene universes (D2, D6).

**Recomputations performed independently:**
- Reconstructed the full RA-PainKG directed graph (18,069 nodes / 127,226 edges; directed density 0.00039) from `RA_PainKG_edges.csv` + `RA_PainKG_nodes.csv`.
- Recomputed approximated betweenness centrality with k=500 across multiple sampling seeds; confirmed the top-5 is seed-dependent, that SRC is unstable (top-5 in 1/3 seeds), and that phenotype nodes HEADACHE/PAIN enter the top-5 (D7).
- Computed the overlap between the benchmark vocabulary and RA-PainKG's node/edge set: **165/165 pain genes have edges; 0/100 CTRL genes have edges** (D1).
- Verified the multi-split r values in the summary JSON against the raw per-split CSV (exact match) (D3 statistics).
- Confirmed density arithmetic: 673,899 / 2,400 ≈ 280.8 ("280-fold"); RA-PainKG effective density over its 165 populated genes ≈ 0.089 vs the reported 0.00009 over the padded 5,045 matrix (D8).

**Discrepancies found (summary):** (i) benchmark gene set 265/2000 vs claimed 5,045; (ii) RA-PainKG vs GO evaluated on different gene counts; (iii) STRING text "r=0.000" vs data r≈0.59; (iv) "44/165 overlap Norman" vs 165/165 in benchmark vocab; (v) density-matched random computed but omitted from tables; (vi) betweenness top-5 seed-unreported and unstable; (vii) random graphs beat curated graph; (viii) RA-PainKG ≈ degree-preserving random (non-significant).

**Note on independence:** I did not open any REVIEW_*/RESPONSE_*/REVISION_* files, the submission manifest, cover letter, declarations, or other reviewers' reports; this assessment is based solely on the manuscript, source code, and benchmark artifacts listed above.
