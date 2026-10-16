# RA-PainKG → BMC Bioinformatics — Consolidated Independent Review (Round 2)

**Date:** 2026-10-16 | **Editor:** Yongxin Yang (acting editor) | **Panel:** A1 domain, A2 design/statistics, A3 provenance/recompute, A4 venue/reporting
**Manuscript:** `submission_BMC/manuscript_BMC.md` (+ `.docx`), target *BMC Bioinformatics* (SCIE, JIF 2025 ≈ 4.4; soundness-only)

## 1. Independence statement
Each expert received a self-contained brief **forbidding** all prior-round files (`review/round1/*`, `REVISION_NOTE.md`, `SUBMISSION_MANIFEST.md`, `*_gen_*.py`, other `REVIEW_*.md`). Every claim was re-derived from raw data (`output/RA_PainKG_summary.json`, `track_assignments.csv`, `gene_centrality.csv`, `benchmark/results/*`). The four reports were written without cross-reading, and the editor personally recomputed the contested numbers (zero-PPI, COMT/DRD2, 9-pathway enumeration, STRING r, reference ordering).

## 2. Panel verdicts
| Expert | Layer | Verdict | Headline |
|---|---|---|---|
| A1 | Domain | Minor | 9-pathway enumeration ≠ coverage-mapped 9; inline "20 categories" lists 17; COMT already present (only DRD2 omitted); Track B 50% zero-PPI not reproducible |
| A2 | Design/Stats | Minor | Benchmark honestly reframed & reproducible; leakage (test vocab ⊂ construction genes) still unstated; 280-fold, vocab 265 vs 2000 confirmed |
| A3 | Provenance | Minor | All graph/track numbers match raw data exactly; forbidden fingerprints absent; L39 "4 artifacts" double-counts alias-resolved genes; COMT self-contradiction; "10 entity types" omits exposure; STRING r precision |
| A4 | Venue | Minor | Abstract 235 w (≤350, no citations); Declarations complete; [19] false "Zenodo"; title "benchmark validation" overstates a null result; reference numbering out of Vancouver order; article type = Research |

**All four: Minor revision.** Round 1 Tier-0 (conclusion-invalidating) defects confirmed FIXED.

## 3. Editor-verified recomputation (independence check)
- **Zero-PPI (induced 165-gene PPI subgraph, 780 edges):** Track B 30/122 = **24.6%**, Track A 19/106 = **17.9%**. The Round 1 audit-trail "50% Track B" was itself wrong; A1's ~24% is correct. Conclusion (Track B sparser) holds.
- **COMT present:** `track_assignments.csv` line 26 → `COMT,True,True` (recovered via expansion). Only **DRD2** is genuinely absent. L112 corrected.
- **9 pathways:** `pain_signaling_pathways.md` defines exactly 9 (TRPV1-CGRP, Nav1.7, TNFα–NGF, Opioid, JAK-STAT, MAPK, Complement, GABAergic, Prostaglandin). L37 re-enumerated to match.
- **Decoupling lists verified:** 10 inflammation-only (MMP9, TRPA1, IFNG, PADI4, CTLA4, MMP1, CNR2, IL10, TNF, BDNF) + 26 nociception-only = 36; +96 both +33 neither = 165 ✓.
- **STRING v12:** overall pearson_r = 0.0003; pain-subset = 0.0008 (manuscript "r = 0.000" → corrected to "≤0.001").
- **Entity types:** summary lists 10 (incl. `exposure`); L67 now lists all 10.
- **Reference order:** DisGeNET first at L27 → [16]; GTEx L29 → [17]; Norman L53 → [18]; GEARS L55 → [19]; self L59 → [20]; Nguyen L107 → [21]; GO L151 → [22]. Now strictly ascending.

## 4. Fixes applied in `manuscript_BMC.md`/`.docx` (all docx checks pass, 14/14)
- Title: "with benchmark validation" → "with transparent benchmark characterization".
- Stage 1: 9 pathways re-enumerated to match coverage set; 20 categories pointed to Supplementary Table S1.
- Stage 2: L39 "4 artifacts" reconciled — NAPE-PLD/RANKL alias-resolved as present (NAPEPLD/TNFSF11); ADRA2B construction artifact; ACPA non-gene.
- Stage 3: L67 entity types now list all 10 (added exposure).
- Benchmark: L49 STRING r corrected to "overall r = 0.0003; pain-subset r = 0.0008".
- Results: L75 zero-PPI corrected to 24.6% Track B / 17.9% Track A (induced 165-gene PPI subgraph, 780 edges), with explicit definition.
- Discussion: explicit leakage sentence added (265-gene benchmark vocab ⊂ construction genes → in-construction sanity check).
- Limitations: L112 DRD2-only omission; COMT noted as recovered via expansion.
- References: [19] "GitHub/Zenodo" → "GitHub"; full Vancouver renumber to ascending order.

## 5. Residual / pre-submission items (not manuscript defects)
- **Deposition completeness (A3):** 188/192, 189/192, 120/45 split, 72/68/4, 44/165 Norman overlap, 2,400-edge PPI variant are not recomputable from the *deposited* files because Supplementary Tables S1 (192-gene list), S3 (recovery map), S6 (Norman overlap) and the final node set must be confirmed present in `submission_BMC/supplementary/supplementary_tables.docx`. Verify before submission; deposit separately if absent.
- **Optional:** mint a real Zenodo DOI for [19] (currently a GitHub citation, which BMC accepts for software, but a DOI strengthens auditability).
- **benchmark_metadata.json** lacks a stored zero-edge field — add for auditability (cosmetic).

## 6. Editor decision
Round 1 resolved all integrity-critical defects; Round 2 resolved all remaining clarity/honesty/minor-format items. The manuscript is now **scientifically honest, internally consistent, and compliant with BMC Bioinformatics soundness-only standards**. Recommendation: **Accept (pending the deposition-completeness check above)** — ready to submit as a Research article.
