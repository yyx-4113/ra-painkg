# RA-PainKG → BMC Bioinformatics — Consolidated Independent Review (Round 1)

**Date:** 2026-10-16 | **Editor:** Yongxin Yang (acting editor) | **Panel:** A1 domain, A2 design/statistics, A3 provenance/recompute, A4 venue/reporting
**Manuscript:** `submission_BMC/manuscript_BMC.md` (+ `.docx`), target *BMC Bioinformatics* (SCIE, JIF 2025 = 4.4; soundness-only)

## 1. Independence statement
Each expert received a self-contained brief forbidding all prior-review/meta files (`REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `SUBMISSION_MANIFEST.md`, `REVISION_NOTE.md`, other reviewers' outputs, `*_gen_*.py`). Each recomputed numbers from raw sources. **Evidence independence worked:** the single most damaging defect — the 165-gene composition mis-accounting — was hit independently by A1 (track arithmetic 106+122−96=132≠165), A3 (only 120/192 core genes carry full annotation; the "62.5%" fingerprint re-surfaces), and A4 (190+45≠165). A2 independently caught the benchmark leakage / non-comparable gene universes. Clusters on different angles of the same defect = the discipline held.

## 2. Verdict table
| Expert | Layer | Recommendation | Basis |
|---|---|---|---|
| A1 | Domain | Major revision | Canonical pain genes (DRD2, COMT) missing; "nine pathways" never enumerated; 20-cat vs 9-pathway undefined; 58% track overlap under-motivated |
| A2 | Design/Stats | Major revision (near DESK-REJECT on benchmark) | Train/test circularity (benchmark vocab overlaps construction genes); RA-PainKG vs GO compared on different gene universes; RA-PainKG ≈ random graph, hidden |
| A3 | Provenance | Major revision | 2,400 vs 28,972 PPI contradiction; 124,826 vs 98,254 non-PPI; 190+45≠165; "120" residue at line 80; 62.5% fingerprint reappears |
| A4 | Venue | Major revision | Article-type mismatch (Database vs Research); overclaim "not previously available" contradicts own "already well-covered"; placeholder self-citation [19]; abstract ≈235 w (OK) |

## 3. Cross-verification table (manuscript claim vs independently recomputed)
| # | Location | Manuscript claim | Recomputed (editor-verified) | Verdict |
|---|---|---|---|---|
| 1 | Methods/Results | 188/192 (97.9%) present in final graph | config 192; summary total_nodes 18069; presence 188 ✓ | OK |
| 2 | Methods | 189/192 (98.4%) exact-symbol match | plausibly OK (not re-run; needs `data/prime_kg.csv`) | OK* |
| 3 | Methods | 190 seed gene nodes | summary seed_nodes.pain_gene_protein=190 ✓ | OK |
| 4 | Methods | 2-hop added 45 → 165 annotated | track_assignments=165; 120 core + 45 expansion ✓ BUT "190+45=165" false | CONTRADICTION |
| 5 | Methods/Results | 2,400 PPI edges + 124,826 non-PPI | full graph `protein_protein`=**28,972**; non-PPI=127,226−28,972=**98,254**; 2,400 is the *benchmark PPI-only variant* | CONTRADICTION (T0) |
| 6 | Results | Track A 106 / B 122 / 96 overlap | CSV: TA106, TB122, both96 ✓ | OK |
| 7 | Results | 165 organized as dual-track | 33/165 in NEITHER track (CALCA, CCR6, CSF2, GABRA1, GRIN2A…) | MISLEADING |
| 8 | Methods | "120 core + 45 expansion = 165" | editor recompute: 120 of 165 ARE core; 45 expansion ✓ | OK (but unstated in MS) |
| 9 | Abstract/Results | 18,069 nodes/10 types; 127,226 edges/24 types | summary: 18069/10, 127226/24 ✓ | OK |
| 10 | Results | 4,760 drug–target edges | summary edge_relation `drug_protein`=4760 ✓ | OK |
| 11 | Methods | 44/165 (26.7%) overlap Norman vocab | S5/GitHub; cross-check OK | OK |
| 12 | Methods | 1,600/5,045 (31.7%) have ≥1 RA-PainKG edge | benchmark metadata OK | OK |
| 13 | Methods | densities 0.0265 / 0.0048 / 0.00009 | benchmark files OK | OK |
| 14 | Results | multi-split r: RA-PainKG 0.503 vs GO 0.542 | S4/S5 OK — BUT on different gene universes (265 vs 2000) | INVALID COMPARISON (T0) |
| 15 | Results | seed-42 r: 0.558 vs 0.481 | S4 OK | OK (illustrative) |
| 16 | Results | K562 91,205 cells/5,045 genes/284 cond | external .h5ad, accepted | OK* |
| 17 | Results | 59.1% (26/44) pain genes <0.01 expr | S5 OK | OK |
| 18 | Results | mean pain-gene expr 0.117 vs bg 0.107 | A3 could not reproduce bg 0.107 from deposited files | UNVERIFIED |
| 19 | Results | 280-fold sparsity | 673,899/2,400≈280 ✓ | OK |
| 20 | Results | STRING r = 0.000 | `full_benchmark_results.json` STRING v12 pearson_r=0.0002656 ✓ (A2's "≈0.59" was a misread — demoted) | OK |
| 21 | Results | top-5 hubs EGR1/FOS/STAT3/AKT1/SRC | summary top_hubs = EGR1,FOS,STAT3,AKT1,SRC,JUN… ✓ (full-graph) | OK (but sampled k=500 seed-dependent per A2) |
| 22 | Results | 4 "non-recovered" ACPA/NAPE-PLD/RANKL/ADRA2B | NAPE-PLD=NAPEPLD, RANKL=TNFSF11 present under alias → self-contradiction; only ACPA+ADRA2B genuinely absent | CONTRADICTION (T1) |

\* accepted as cited; not re-derivable from deposited artifacts.

## 4. Graded issue list
### Tier 0 — conclusion-invalidating / integrity
- **T0-1 (A3 F2, editor-confirmed):** Methods Stage 3 states "2,400 protein–protein interaction edges and 124,826 non-PPI edges." The full graph has **28,972** PPI edges (`protein_protein` in `RA_PainKG_summary.json`) and **98,254** non-PPI. 2,400 is the *benchmark PPI-only subgraph*, not the resource. Internal self-contradiction in one section. → Fix numbers; reserve 2,400 for the benchmark variant only.
- **T0-2 (A2 D1/D2/D3, editor-confirmed):** Benchmark compares RA-PainKG (predictions on **265-gene** vocab) vs GO/STRING (on **2000-gene** vocab). The headline "RA-PainKG 0.503 vs GO 0.542" is **not comparable**. Within the same 265-gene vocab, **Random beats RA-PainKG** (S4: +0.115, p=0.0003) and RA-PainKG is statistically indistinguishable from a degree-preserving random rewiring (Δr=+0.005, p=0.83). The manuscript's "boundary conditions" narrative hides that random controls outperform the curated graph. → Reframe benchmark as a within-vocab comparison vs random/degree-matched controls; state plainly that KG structure added little beyond degree/density on K562.
- **T0-3 (A1/A3/A4, editor-confirmed):** "190 seed gene nodes … 2-hop expansion identified 45 … yielding 165" implies 190+45=165 (false). Correct chain: **120 curated genes retained** (of 192) + **45 expansion = 165**. Also **72 of 192 curated genes are present in the graph but receive NO dual-track/tissue/benchmark annotation**; and **33 of the 165 annotated genes belong to NEITHER track**. The "62.5%" fingerprint (120/192) reappears — now *true*, but must be clearly distinguished from the retracted "72 absent / 62.5% matched" false claim. → Rewrite composition paragraph with the exact, honest derivation and the 72-present-but-unannotated gap.

### Tier 1 — analyses to add / claims to correct
- **T1-1 (A2 D1):** Leakage risk — benchmark vocab overlaps the construction genes. Either (a) explicitly state the benchmark is an *in-construction* sanity check and report a **held-out** evaluation (genes in graph but outside the 165 curation, or external pain genes not curated), or (b) reframe scope. Add a paragraph on leakage limitation.
- **T1-2 (A3 F4, editor-confirmed):** "NAPE-PLD (resolves to NAPEPLD), RANKL (resolves to TNFSF11)" are listed as *non-recoveries* yet are present under alias — self-contradiction. Restrict the "non-recovered" list to **ACPA** (autoantibody, not a gene) and **ADRA2B** (construction artifact). Remove NAPE-PLD/RANKL from the non-recovery list; cite them as alias-recovered.
- **T1-3 (A1 #2/#3):** "Nine pain signaling pathways" is asserted 5× but **never enumerated**; "20 functional categories" vs "nine pathways" relationship undefined. Enumerate the nine pathways and map them to the 20 categories (or correct the counts). The "57–100% coverage" floor is irreconcilable with "no gene genuinely absent" — define the coverage metric precisely (per-pathway *curated-gene* coverage vs *graph-node* coverage).
- **T1-4 (A1 #1):** Canonical, replicated pain genes **DRD2** and **COMT** are absent from the 192 curation (COMT is the strongest human pain-genetics finding; DRD2 = descending dopaminergic analgesia). Add them (and re-run recovery) or explicitly justify exclusion in Limitations.
- **T1-5 (A2 D7):** Betweenness top-5 from k=500 sampled centrality is seed-dependent (A2: SRC in only 1/3 seeds; phenotype nodes displace). Report the sampling seed, or compute full-graph betweenness (summary already has full-graph top hubs) and state method explicitly.
- **T1-6 (A4 F5):** Self-citation [19] is a placeholder (GitHub/Zenodo 2026), never cited in text. Replace with a real archived DOI (Zenodo) or delete.

### Tier 2 — wording
- **T2-1 (A4 F4/F7):** Conclusions claim "a resource type not previously available for pain biology" while the body (line 78) says "already well-covered gene set" and the benchmark "cannot resolve" (line 108). Reconcile: the contribution is *transparent organization + dual-track lens + documented recovery*, not novelty of the gene set.
- **T2-2 (A1 #4):** "Tissue-contextualized" overstated — GTEx is descriptive node metadata only ("not used to filter edges", line 41). Soften to "tissue-annotated."
- **T2-3 (A1 #6):** 58% track overlap under-motivated; enumerate the 10 inflammation-only + 26 nociception-only genes that ground the "decoupling" claim, or temper the claim.

### Tier 3 — format
- **T3-1 (A4 F1):** Consider BMC "Database" article type (resource + negative benchmark fits Database better than Research). If staying Research, title should not foreground "benchmark validation" as the contribution.
- **T3-2 (A3 F5):** Remove stray "120" residue at `manuscript_BMC.md:80` and the "120 + 45" supplementary caption leftover.
- **T3-3:** Reference [19] dangling; verify reference order/DOI for [13] PrimeKG (Sci Data 2023, correct).

## 5. Consensus / Complementarity / Disagreement
- **Consensus:** The benchmark section is the weakest part (A2, A3, A4 all flag it); the recovery/composition accounting is materially mis-stated (A1, A3, A4 converge); overclaim language must be cut (A1, A4).
- **Complementarity:** A3 quantified the exact edge-count contradiction; A2 diagnosed *why* the benchmark is invalid (leakage + non-comparable universes); A1 supplied the biological "so what"; A4 tied it to BMC's soundness-only acceptance bar.
- **Disagreement (adjudicated):** A2 D6 claimed STRING r≈0.59; A3 (and editor) found `full_benchmark_results.json` STRING v12 pearson_r=0.0002656. **Ruled: A3/editor correct; A2 misread. Demote D6.** Severity disagreement on article type (A4 says Database; editor: Research is defensible if benchmark reframed honestly) — adopt Research but soften title.

## 6. Priority must-fix list
- **DESK-REJECT risks if unaddressed:** T0-2 (invalid benchmark comparison + hidden null), T0-1 (internal arithmetic contradiction). Both are fixable by honest reframing + number correction; not grounds for rejection once corrected.
- **Must add analysis:** T1-1 (held-out / leakage statement), T1-3 (enumerate 9 pathways), T1-4 (DRD2/COMT).
- **Must reword:** T0-3, T1-2, T1-5, T2-1/2/3, T3-2.
- **Must correct numbers:** T0-1 (28,972 / 98,254), T0-3 (120+45 chain; 72 unannotated; 33 trackless).

## 7. What stands up (do NOT change)
- 188/192 (97.9%) graph presence; 18,069/10, 127,226/24; 4,760 drug–target; Track A106/B122/96; top-5 hubs; multi-split r direction; densities; 280-fold sparsity; STRING r=0.000; "50% Track B / 20% Track A zero-PPI" (verified under 165-gene PPI-subgraph reading); data-availability release integrity (A4 verified SHA-256 match); AI-use disclosure placement; structured abstract compliance.

## 8. Recommended handling path
**A) Restructure & resubmit as the same (Research) article type**, with: (i) benchmark reframed as an honest within-vocab comparison vs random/degree-matched controls stating RA-PainKG ≈ random on K562; (ii) composition rewritten with the exact 120+45 / 72-unannotated / 33-trackless derivation; (iii) nine pathways enumerated; (iv) overclaim cut. **B) Downgrade to Database** is viable if the authors prefer to foreground the resource and demote the benchmark to a brief validation note. Editorial recommendation: **Path A** — the resource + transparent recovery is a legitimate BMC soundness-only contribution once the benchmark is honest and the arithmetic is corrected.

## 9. Process lessons (what gates could not catch)
- A gate checks arithmetic of *enumerated* strings; it did not catch that "2,400 PPI" (benchmark variant) was pasted into the resource description. → Assert that edge counts must cite their *scope* (full graph vs variant).
- The retracted "62.5%" fingerprint silently re-entered as a *true* 120/192 — gates cannot tell a resurrected false number from a coincidentally equal true one. → Require a provenance note whenever a number equals a previously-retracted value.
- Benchmark leakage (construction genes in test vocab) is a design-layer defect invisible to any consistency gate. → Add a "train/test gene-overlap" assertion to the benchmark gate.
