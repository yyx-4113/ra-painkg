# A2 — Independent Design & Statistics Re-review (Round 2)

**Reviewer role:** Independent design/statistics reviewer, judging the *revised* manuscript's benchmark & statistical claims solely from the manuscript (`manuscript_BMC.md`) and raw data. Prior-round reviews and response notes were **not** read.

**Scope:** BMC Bioinformatics (SCIE, soundness-only). Verdict concerns whether the benchmark is *honestly and reproducibly* reported, not whether RA-PainKG "works."

---

## Issue 1 — Honest-reframing numbers (Task 1): VERIFIED, reproducible

**【Problem】** None. Confirm the manuscript's two headline within-vocabulary deltas are exactly the values in `supplementary_table_S4.md` and reproducible from `full_benchmark_results.json`.

**【Evidence】**
- Manuscript line 101: *"random vs RA-PainKG Δr = +0.115, p < 0.001; RA-PainKG vs degree-preserved Δr = +0.005, p = 0.83."*
- S4 row 9 (`Random_R1 vs RA_PainKG`, `r_all`): Mean Δr **+0.115**, 95% CI [+0.076, +0.155], t=5.75, df=9, **p(unadjusted)=0.0003** → p<0.001. ✓
- S4 row 13 (`RA_PainKG vs RA_PainKG_degPreserved`, `r_all`): Mean Δr **+0.005**, 95% CI [−0.041, +0.052], t=0.23, df=9, **p(unadjusted)=0.8268** → 0.83. ✓
- Both are on the **265-gene** RA-PainKG vocabulary (see Issue 5), so the "within-vocabulary null" framing is internally consistent.

**【Why it matters】** These are the central honesty claims; they are stated verbatim and match the data.

**【Specific fix】** None required. Optionally, note in S4 that the quoted p-values are *unadjusted* (S4 header already says the Bonferroni threshold is p<0.01); the manuscript prose repeats them without the "unadjusted" qualifier, which is acceptable but worth a footnote.

---

## Issue 2 — T1-1 LEAKAGE honesty gap (Task 2): REMAINING GAP — flag

**【Problem】** The manuscript does **not explicitly state** that the RA-PainKG benchmark *test vocabulary is itself a subset of RA-PainKG's own construction genes*. It states the two ingredients separately but never connects them.

**【Evidence】**
- Manuscript line 43: *"For benchmarking, a PPI-only variant retaining 2,400 edges **among the annotated genes** was used."*
- Manuscript line 49: benchmark adjacency matrices built by *"RA-PainKG gene nodes (type 'gene/protein') extracted and HGNC-matched, retaining only PPI edges."* → the RA-PainKG benchmark graph is literally RA-PainKG's own gene nodes.
- `benchmark_metadata.json` `gene_vocabulary` = 165 entries, all pain genes (AKT1, TRPV1, SCN9A, …) = the 165 construction/annotated genes (track counts 106+122−96 = 132 in tracks + 33 neither = 165, confirmed from `RA_PainKG_summary.json`).
- The 265-gene RA-PainKG benchmark vocabulary = those construction genes present in Norman (44/165, line 43) **plus their PPI neighbours within Norman**. So the test set is drawn from the graph's own nodes — a self-referential evaluation.
- What the manuscript *does* say about overlap (line 43, 99, 101) is only (a) "44/165 annotated genes overlap Norman" and (b) "RA-PainKG 265-gene vocab vs GO/STRING 2000-gene vocab" (a *size* mismatch). It never states the deeper point that the 265-gene test set = RA-PainKG's own genes, which is why even the within-vocabulary null is the only fair reference.

**【Why it matters】** A reader can walk away thinking the K562 benchmark independently tests RA-PainKG against *external* biology, when in fact it tests RA-PainKG against a vocabulary that is part of RA-PainKG itself. The "non-comparable universe" caveat (line 101) addresses cross-KG comparability but understates the *self-referential* nature of the within-KG test. This is the single most important remaining honesty gap.

**【Specific fix】** Add one explicit sentence in the Discussion (around line 101), e.g.:

> *"Crucially, the 265-gene RA-PainKG benchmark vocabulary is itself a subset of RA-PainKG's own gene nodes (the 44 annotated pain genes present in Norman plus their PPI neighbours); the benchmark therefore evaluates RA-PainKG against a vocabulary that overlaps its own construction genes and cannot demonstrate independent, externally-validated predictive performance. It can only show that RA-PainKG's internal structure is no better than a density- or degree-matched null of the same vocabulary."*

This sentence converts an implied caveat into an explicit, defensible boundary condition.

---

## Issue 3 — 280-fold sparsity & "68.3% zero edges" (Task 3): VERIFIED (one minor auditability gap)

**【Problem】** Confirm 673,899 / 2,400 ≈ 280 and "68.3% of Norman genes have zero edges" from `benchmark_metadata.json`.

**【Evidence】**
- 673,899 ÷ 2,400 = **280.79 ≈ 280**. ✓ (`benchmark_metadata.json` `kg_edges`: RA-PainKG 2400, GO-BP/STRING 673899; manuscript line 81.)
- "68.3% zero edges" is the complement of manuscript line 49: *"of 5,045 Norman genes, 1,600 (31.7%) have ≥1 edge in RA-PainKG."* 1,600 / 5,045 = 0.3171; 1 − 0.3171 = **0.6829 ≈ 68.3%**. ✓ internally consistent.
- **Gap:** `benchmark_metadata.json` does **not** store a field for `n_genes_with_edges` (1600) or `pct_zero_edges` (68.3%). These numbers live only in the manuscript prose (line 49/81), so they are *not directly auditable* from the metadata as the task asked.

**【Why it matters】** The arithmetic is correct and reproducible from line 49, but the metadata should carry the source count so a reader can verify without cross-referencing prose.

**【Specific fix】** Add to `benchmark_metadata.json`: `"n_norman_genes_with_edges": 1600` and/or `"pct_norman_genes_zero_edges": 68.3` (with a one-line derivation note). No manuscript change strictly needed.

---

## Issue 4 — Multi-split r and seed-42 (Task 4): VERIFIED

**【Problem】** Confirm multi-split means (RA-PainKG 0.503 vs GO 0.542) and seed-42 (0.558 vs 0.481) from S5 / `benchmark_multisplit_*`.

**【Evidence】**
- `benchmark_multisplit_summary.json` → `r_pain` means: GO **0.5422**, RA_PainKG **0.5032**. ✓ matches manuscript line 83 & 101.
- `benchmark_multisplit.csv` split 0 (seed 42): GO `r_pain` **0.4811**, RA_PainKG `r_pain` **0.5578**. ✓ matches manuscript line 83 ("0.558 vs 0.481").
- (Both also present as `r_all` in the summary; the manuscript consistently cites `r_pain` for these comparisons — internally consistent.)

**【Why it matters】** The "single-split artifact" narrative (seed 42 reverses under multi-split averaging) is the manuscript's second honesty demonstration; the numbers are exact.

**【Specific fix】** None.

---

## Issue 5 — Prediction-array shapes (Task 5): VERIFIED — validates non-comparable universe

**【Problem】** Load `predictions_*.npy` and confirm RA-PainKG/Random are on ~265-gene vocab while GO/STRING are on ~2000.

**【Evidence】** (via `C:/Python314/python.exe`, numpy)
- `predictions_RA-PainKG.npy` → **(411, 265)** float64
- `predictions_Random.npy` → **(411, 265)** float64 (within-265-gene vocab null, as claimed in Task 1)
- `predictions_GO-BP_original_GEARS.npy` → **(1072, 2000)** float64
- `predictions_STRING_v12.npy` → **(1072, 2000)** float64

**【Why it matters】** This directly validates the manuscript's central "non-comparable universe" point (line 101): RA-PainKG and its within-vocab nulls sit on a 265-gene space; GO and STRING on a 2000-gene space. Cross-KG r comparisons are therefore not directly comparable — the manuscript's disclaimers are data-supported. The 411 vs 1072 row counts (test perturbation–gene pairs) further confirm the vocabulary-size asymmetry is real, not asserted.

**【Specific fix】** None. This is strong, reproducible support for the honest framing.

---

## Issue 6 — Bonferroni α=0.01, m=5 (Task 6): ACCEPTABLE but under-justified (minor)

**【Problem】** Assess whether m=5 is justified.

**【Evidence】**
- Manuscript line 55: *"Paired t-tests with Bonferroni correction (α = 0.01, m = 5)."*
- S4 header: *"Bonferroni-adjusted significance threshold: p < 0.01 (5 primary comparisons)."*
- S4 contains **14** rows (7 `r_all` + 7 `r_pain`), yet only "5 primary comparisons" are named for the threshold. The 5 are plausibly the KG-vs-KG head-to-heads (Random vs GO; Random vs RA_PainKG; GO vs RA_PainKG; RA_PainKG vs degPreserved; GO vs GO_painCentric), with the two extra rows (Random vs degPreserved; Random vs GO_painCentric) treated as secondary. The `r_pain` column doubles every comparison but is not separately accounted for in m.

**【Why it matters】** m=5 is defensible *if* the 5 are pre-specified KG head-to-heads, but the manuscript/S4 never **enumerate which 5**. With 14 tests, a strict family-wise count would give α≈0.0036, not 0.01. However, the two headline conclusions are robust either way: null-beats-real p=0.0003 (≪0.0036) and structure=degree p=0.83 (ns at any threshold). So the choice does not change conclusions.

**【Specific fix】** Minor: in S4 (and ideally line 55) explicitly enumerate the 5 primary comparisons (e.g., "the five KG-vs-KG head-to-heads: Random vs GO, Random vs RA_PainKG, GO vs RA_PainKG, RA_PainKG vs degPreserved, GO vs GO_painCentric; `r_pain` reported as a secondary metric on the same splits"). This removes ambiguity. No change to conclusions.

---

## Issue 7 — Does the benchmark read as honest boundary conditions? (Task 7): YES (acceptable for soundness-only)

**【Problem】** Assess whether the section still implies a positive performance claim that would mislead, vs. honest boundary conditions.

**【Evidence】**
- Abstract line 15: *"Benchmark validation … established transparent boundary conditions."*
- Results line 81: *"These data establish that K562 performance reflects test-system limitations, not resource quality."*
- Results line 83: seed-42 over-performance is immediately corrected by the multi-split reversal.
- Discussion line 101: *"RA-PainKG therefore confers no predictive advantage over a structureless or degree-matched null on this task; we report this transparently as a boundary condition, not as evidence of resource quality."* — an explicit, strong, honest statement.
- Line 99–103 consistently frame K562 as a *mismatched* test system and explicitly decline to claim biological validity.

**【Why it matters】** No residual positive-performance claim was found. The only over-statement risk is the *implied* independence of the test set (Issue 2), not an explicit performance boast. As written, the benchmark is appropriately self-deprecating and fits a soundness-only policy.

**【Specific fix】** Adopt the Issue 2 sentence; otherwise the framing is sound.

---

## §Stands up (verified-true claims)

1. Within-265-gene-vocab null deltas: random − RA-PainKG Δr=+0.115 (p=0.0003<0.001); RA-PainKG − degPreserved Δr=+0.005 (p=0.83). Exact, reproducible (S4 rows 9, 13).
2. 280-fold sparsity (673,899/2,400=280.79). Exact.
3. 68.3% of Norman genes have zero edges (= 1 − 1,600/5,045). Consistent with line 49.
4. Multi-split r_pain: RA-PainKG 0.503 vs GO 0.542 (summary JSON). Exact.
5. Seed-42 r_pain: RA-PainKG 0.558 vs GO 0.481 (multisplit.csv). Exact.
6. Prediction shapes (265 vs 2000) validate the non-comparable-universe disclaimers.
7. Graph provenance (18,069 nodes / 127,226 edges; hubs EGR1/FOS/STAT3/AKT1/SRC; tracks 106/122/96) matches `RA_PainKG_summary.json`.

## §Residual risk

- **R1 (moderate):** Self-referential benchmark vocabulary not explicitly stated (Issue 2) — the most important honesty gap; fixed by one Discussion sentence.
- **R2 (minor):** `benchmark_metadata.json` lacks `n_genes_with_edges` / zero-edge percentage fields (Issue 3) — add for auditability.
- **R3 (minor):** Bonferroni m=5 not enumerated (Issue 6) — add the list of 5; conclusions unaffected.
- **R4 (none observed):** No positive-performance claim, no leakage of *prior* reviews, no fabricated statistics detected.

## Verdict: **Minor**

The revised benchmark is honestly reframed, fully reproducible from the supplied data, and contains no misleading positive-performance claim — consistent with BMC Bioinformatics' soundness-only policy. All seven verification tasks either pass or reveal only minor transparency gaps. One substantive honesty wording gap remains (the self-referential nature of the RA-PainKG test vocabulary, Issue 2/T1-1); addressing it (plus the two minor metadata/enumeration notes) would make the benchmark unassailable. Recommend **minor revision**; no major or reject-level concerns.
