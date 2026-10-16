# Revision Note — RA-PainKG (BMC Bioinformatics submission)

## 1. Critical data-integrity correction (carried from the IBM attempt)

The earlier draft (target *Intelligence-Based Medicine*) contained a **false central claim**: that 120/192 (62.5%) of curated pain genes matched PrimeKG and **72 (37.5%) were absent**, with the paper's contribution framed as "systematic documentation of 72 missing genes." Verification against the code and data proved this false:

- Final RA-PainKG graph contains **188/192 (97.9%)** curated pain genes.
- **189/192 (98.4%)** match PrimeKG v1.0 node symbols exactly (case-insensitive).
- 190 seed gene nodes were identified in the pipeline.
- Of 39 genes the old draft explicitly listed as "absent," **37 are actually present** (e.g., C1QA, C3, C5AR1, ADRA2A, GABRA3, TRPM8, STAT1).
- The 4 genuine non-recoveries are **not biological absences**: identifier/symbol artifacts (ACPA, NAPE-PLD→NAPEPLD, RANKL→TNFSF11) and one construction artifact (ADRA2B present in PrimeKG but not retained in the final graph).

**Resolution:** The manuscript now states, with transparent documentation, that no curated gene is genuinely absent and that the resource's value is the *organization, tissue contextualization, and transparent annotation* of an already well-covered gene set. All stale "72/62.5%" content was removed from the manuscript and supplementary tables. The reframing was **ratified by the author on 2026-10-15/16**.

## 2. Journal switch: IBM → BMC Bioinformatics

On 2026-10-16 the author elected to switch from *Intelligence-Based Medicine* (IBM) to **BMC Bioinformatics** after online verification showed IBM is **not indexed in Web of Science / has no JCR Impact Factor** (Scopus CiteScore 2025 = 4.7 only), whereas BMC Bioinformatics is **SCIE (2025 JIF 4.4)** and follows a **soundness-only** editorial policy well suited to a computational knowledge-graph + benchmark paper. This also avoids the user's empirically documented desk-reject risks with *Scientific Reports* and the methodological-rejection risk with *PLOS ONE* for computational work, and respects the *PeerJ* blacklist.

## 3. Reformatting performed for BMC Bioinformatics

- Restructured from IBM's numbered sections (1, 1.1…) to BMC's named sections: Background / Methods / Results / Discussion / Conclusions.
- Abstract rewritten as structured **Background / Results / Conclusions** (248 words, no reference citations).
- Embedded Python "Usage Examples" code block removed from the main text (code remains in the public repository).
- AI-use disclosure moved from a standalone end-section into the **Methods** section (BMC requirement).
- Added BMC-mandated **Declarations** block (Ethics: Not applicable; Consent: Not applicable; Availability of data and materials; Competing interests; Funding; Authors' contributions; Acknowledgements).
- Added **List of abbreviations**.
- Body prose trimmed from 4,473 to **3,282 words** (≤3,500 target); all verified numbers preserved unchanged.
- Elsevier-style **Highlights** omitted (not required by BMC).
- All figures (fig1–fig6) and supplementary tables copied unchanged.

## 4. Unchanged verified numbers (audit trail)

188/192 (97.9%); 189/192 (98.4%); 192 genes; 20 functional categories; 9 pathways (now enumerated in Stage 1); 120 curated + 45 expansion → 165 annotated (72 curated not in dual-track set, 68 present-but-unannotated); Track A 106 / Track B 122 / overlap 96 (58.2%) / 33 in neither track; 18,069 nodes (10 types); 127,226 edges (24 types); full-graph **28,972 PPI + 98,254 non-PPI** edges; **2,400 PPI is the benchmark PPI-only variant only** (not the resource); 4,760 drug–target edges; top hubs EGR1, FOS, STAT3, AKT1, SRC; pathway coverage 57–100%; 11 KG variants benchmark; Norman K562 91,205 cells / 5,045 genes / 284 conditions; k=128 embeddings; ridge λ=0.1; 10 splits; Bonferroni α=0.01 (m=5); 280-fold sparser than GO (benchmark PPI variants); 68.3% zero-edge; 44/165 (26.7%) in Norman; 59.1% (26/44) K562 expr <0.01; mean pain-gene expr 0.117 vs background 0.107; seed-42 split r=0.558 vs 0.481, multi-split 0.503 vs 0.542; within-265-gene-vocab random beats RA-PainKG (Δr=+0.115, p<0.001), RA-PainKG ≈ degree-preserved random (Δr=+0.005, p=0.83).

## 5. Round 1 independent expert panel review (2026-10-16)

Acting as editor, I convened a 4-expert independent panel (A1 domain / A2 design-statistics / A3 provenance-recompute / A4 venue-reporting) with enforced independence (no cross-reading of prior reviews; every claim recomputed from raw sources). Consolidated report: `review/round1/REVIEW_round1_2026-10-16.md`; expert files `review/round1/A1_domain.md`…`A4_venue.md`.

**Editor-verified worst findings (independently reproduced):**
- **T0-1 (CONFIRMED):** Methods mis-stated PPI/non-PPI edges. Full graph = **28,972 PPI + 98,254 non-PPI** (from `RA_PainKG_summary.json`); the "2,400 PPI" belongs only to the *benchmark PPI-only variant*. Fixed.
- **T0-3 (CONFIRMED):** Composition arithmetic was false ("190 seed + 45 = 165"). Correct chain: 120 curated retained + 45 expansion = 165; **72 of 192 curated genes are present in the graph but received no dual-track annotation**; **33 of 165 annotated genes belong to neither track**. The "62.5%" fingerprint reappears as a *true* 120/192 — distinct from the retracted false "72 absent" claim; rewrote without re-asserting 62.5% as a positive.
- **T0-2 (CONFIRMED):** Benchmark invalid as cross-KG comparison — RA-PainKG on 265-gene vocab, GO/STRING on 2,000-gene vocab; within-vocab random ≥ RA-PainKG. Reframed benchmark as honest within-vocab vs random/degree-matched null.
- **T1-2 (CONFIRMED):** NAPE-PLD/RANKL were listed as "non-recoveries" yet present under aliases NAPEPLD/TNFSF11 — self-contradiction. Reduced residual list to ADRA2B (construction artifact) + ACPA (non-gene); alias resolution noted.
- **A2 vs A3 disagreement on STRING r:** editor resolved in favor of A3 — `full_benchmark_results.json` shows STRING v12 pearson_r = 0.0002656 ≈ 0.000 (A2 misread). Demoted.

**Fixes applied in `manuscript_BMC.md`/`.docx` (all 14 docx checks pass):** corrected edge counts (28,972/98,254); corrected composition derivation + 72-unannotated + 33-trackless; honest benchmark reframing with random-control result; alias-resolved recovery; enumerated 9 pathways in Stage 1; added DRD2/COMT omission to Limitations; removed "resource type not previously available" overclaim; cited [19] at repo URL (resolved dangling reference); removed stray "120 core genes" wording.

**Open items for Round 2 / author decision:**
- T1-5: betweenness top-5 method clarity (full-graph vs k=500 sampled) — summary uses full-graph values; caption should state method + sampling seed.
- T1-4: DRD2/COMT are flagged as future-release additions (not silently inserted); author to confirm inclusion or keep as stated limitation.
- T3-1: article type kept as Research (editor ruling); if BMC desk-check prefers, switch to Database.
- T2-3: optionally enumerate the 10 inflammation-only / 26 nociception-only genes grounding the decoupling claim.

## 6. Round 2 independent expert panel review (2026-10-16)

Re-convened the same 4-expert independent panel (A1–A4) with enforced independence (no access to Round 1 files) to re-verify the revised manuscript and catch residual defects. Consolidated report: `review/round2/REVIEW_round2_2026-10-16.md`; expert files `review/round2/A1_domain.md`…`A4_venue.md`.

**All four returned Minor revision.** Round 1 Tier-0 defects confirmed FIXED (A3: every graph/track number matches raw data exactly; forbidden fingerprints absent; A2: benchmark honest-reframing numbers reproduced, vocab mismatch 265 vs 2000 confirmed).

**Editor-verified recomputation (independence check) and fixes applied in `manuscript_BMC.md`/`.docx` (14/14 docx checks pass):**
- **Zero-PPI (L75):** Round 1 audit-trail "50% Track B / 20% Track A" was itself wrong. Induced 165-gene PPI subgraph (780 edges): Track B 30/122 = **24.6%**, Track A 19/106 = **17.9%**. Corrected with explicit definition; decoupling conclusion (Track B sparser) holds.
- **COMT/DRD2 (L112):** COMT is present in `track_assignments.csv` (recovered via expansion); only **DRD2** is genuinely omitted. Corrected — DRD2-only limitation; COMT noted as expansion-recovered.
- **9 pathways (L37):** re-enumerated to match the coverage-mapped 9 in `pain_signaling_pathways.md` (TRPV1-CGRP, Nav1.7, TNFα–NGF, Opioid, JAK-STAT, MAPK, Complement, GABAergic, Prostaglandin); 20 categories pointed to Supplementary Table S1.
- **Entity types (L67):** now lists all 10 (added `exposure`).
- **STRING r (L49):** corrected "r = 0.000" → "overall r = 0.0003; pain-subset r = 0.0008" (verified from `full_benchmark_results.json`).
- **Artifact reconciliation (L39):** "4 artifacts" reworded so NAPE-PLD/RANKL are shown alias-resolved as present (NAPEPLD/TNFSF11); ADRA2B = construction artifact; ACPA = non-gene.
- **Leakage (Discussion):** explicit sentence added — RA-PainKG's 265-gene benchmark vocabulary is drawn from its own construction genes (in-construction sanity check, not independent external evaluation).
- **Title:** "with benchmark validation" → "with transparent benchmark characterization".
- **[19] self-citation:** "GitHub/Zenodo" → "GitHub" (no real Zenodo DOI yet; BMC accepts software citation).
- **References:** full Vancouver renumber to ascending first-appearance order (DisGeNET [16]→L27, GTEx [17]→L29, Norman [18]→L53, GEARS [19]→L55, self [20]→L59, Nguyen [21]→L107, GO [22]→L151); list physically reordered to match.
- **Decoupling lists verified:** 10 inflammation-only + 26 nociception-only genes enumerable; 10+26+96+33 = 165.

**Residual pre-submission items (not manuscript defects):**
- Confirm Supplementary Tables S1 (192-gene list), S3 (recovery map), S6 (Norman overlap) are present in `submission_BMC/supplementary/supplementary_tables.docx` so deposited files reproduce the headline numbers; deposit separately if absent.
- Optional: mint a real Zenodo DOI for [19]; add zero-edge field to `benchmark_metadata.json`.

**Editor decision:** All integrity-critical and minor clarity items resolved. Manuscript is scientifically honest, internally consistent, and compliant with BMC Bioinformatics soundness-only standards — **Accept pending the deposition-completeness check above**; submit as a Research article. Local commit `fa3dadf` (Round 1) and `a33d73a` (release) now pushed to GitHub (origin/master).

## 7. Round 3 focused integrity verification (2026-10-16)

Pre-submission deposition-completeness check (requested as "continue"). Confirmed S1 (165-gene list), S3 (192-gene recovery map), S6 (structural characteristics) are present in `submission_BMC/supplementary/supplementary_tables.docx`. This surfaced one Tier-1 honesty/reproducibility gap, now fixed.

**Finding:** The Round 2 Discussion caveat (L101) asserted the 265-gene benchmark vocabulary = "the 44 annotated genes present in Norman plus their PPI neighbours" — a **factually wrong decomposition**, and no deposited file quantified the overlap. Editor recomputed from deposited `benchmark/results/gene_vocab.csv` (265) × `output/track_assignments.csv` (165): **265-vocab = 165 dual-track annotated genes (100%) + 100 additional RA-PainKG genes; 0 external genes.** The "44/165" stat is a separate, correctly-computed *measurably-expressed-in-Norman* metric (expressed ⊆ present-in-265-vocab), consistent once terminology is disambiguated.

**Fixes applied (verified in `.docx`, 7/7 checks pass):**
- **L101:** rewritten with verified 165+100 decomposition + cites S6; removed false "PPI neighbours" mechanism.
- **S6 note:** appended reproducible composition (165 annotated + 100 RA-PainKG genes; no external validation genes → within-construction evaluation).
- **L81 & L99:** "present in Norman" → "measurably expressed in Norman" to disambiguate from the 265-vocab.

**Editor decision:** Round 3 closes the final reproducibility gap. Manuscript is scientifically honest, internally consistent, and compliant with BMC Bioinformatics soundness-only standards — **Accept**; submit as a Research article. Optional follow-ups (non-defects): mint a real Zenodo DOI for [19]; add zero-edge field to `benchmark_metadata.json`.

**All review rounds complete.** Round 1 fixed conclusion-invalidating (Tier-0) defects; Round 2 fixed all residual clarity/honesty/format items; Round 3 closed the last deposition-reproducibility gap. Manuscript ready for BMC Bioinformatics submission.

