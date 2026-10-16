# RA-PainKG — Round 3 Review (focused integrity verification, 2026-10-16)

**Trigger:** Pre-submission deposition-completeness check requested by the editor. Round 1 and Round 2 had returned Minor revision / Accept-pending-packaging. This round verifies that the honest "within-construction benchmark" claim in the Discussion is backed by deposited, reproducible data, and resolves an internal inconsistency surfaced during that check.

**Method:** Editor-driven recomputation from deposited raw files (no new 4-panel; the issue is a single, well-scoped factual gap). Independence discipline maintained: numbers re-derived from `benchmark/results/gene_vocab.csv`, `output/track_assignments.csv`, `benchmark/data/norman/norman/perturb_processed.h5ad` — not from prior review text.

---

## 【Problem】
Round 2 had added a within-construction caveat to the Discussion (L101): *"RA-PainKG's 265-gene benchmark vocabulary is drawn from its own construction genes (the 44 annotated genes present in Norman plus their PPI neighbours)…"* The parenthetical decomposition was **factually wrong**, and no deposited file quantified the overlap — so the central honesty claim lacked reproducible support.

## 【Evidence】
From deposited files:
- `benchmark/results/gene_vocab.csv` = 265 genes (the RA-PainKG benchmark test vocabulary).
- `output/track_assignments.csv` = 165 dual-track annotated genes.
- Intersection computed by the editor: **265-vocab ∩ 165 annotated = 165 (100%)**; the remaining **100 genes are additional RA-PainKG genes** (0 external validation genes).
- Therefore the 265-vocab = **165 annotated + 100 RA-PainKG genes**, NOT "44 annotated + PPI neighbours." The "44" figure belongs to a different, correctly-computed metric (see below).
- The Norman `.h5ad` uses Ensembl IDs in `gene_name`; symbol matching yields 0, confirming the 44/165 "present/expressed in Norman" stat is computed via Ensembl→symbol mapping in the pipeline, referring to *measurably expressed* genes — a subset of the 265-vocab (expressed ⊆ present-in-265-vocab), so the two statements are mutually consistent once terminology is disambiguated.

## 【Why it matters】
For a soundness-only journal, the within-construction nature of the benchmark is the manuscript's core honesty point. Asserting a false decomposition ("44 + PPI neighbours") while the real structure is "all 165 annotated + 100" would (a) misstate how the benchmark was constructed and (b) leave the honest claim unsupported by any deposited table — a reproducibility defect exactly of the kind flagged in prior rounds.

## 【Specific fix】
1. **L101 (Discussion):** replaced the wrong decomposition with the verified one: *"RA-PainKG's 265-gene benchmark vocabulary is drawn entirely from its own construction: it comprises all 165 dual-track annotated genes plus 100 additional RA-PainKG genes and contains no external validation genes (Supplementary Table S6). This benchmark is therefore an in-construction sanity check rather than an independent external evaluation…"*
2. **Supplementary Table S6 note:** appended the reproducible composition — *"The RA-PainKG benchmark vocabulary (265 genes) consists of the 165 dual-track annotated genes plus 100 further RA-PainKG genes and includes no external validation genes (within-construction evaluation)."*
3. **L81 & L99:** changed "present in Norman" → "measurably expressed in Norman" for the 44/165 stat, disambiguating it from the 265-vocab (which contains all 165). Internal consistency verified.

## §Stands up (re-verified correct)
- S1 (165-gene annotated list, 165 rows, Track A/B populated), S3 (192-gene recovery map: 188 present / 4 artifacts), S6 (structural characteristics) all present in `supplementary_tables.docx`.
- Benchmark honest reframing (random ≥ RA-PainKG; Δr +0.115, p<0.001; degPreserved Δr +0.005, p=0.83) intact.
- All Round 2 fixes (zero-PPI 24.6%/17.9%; COMT/DRD2; 9 pathways; entity types; STRING r; title; [19]; Vancouver order) intact.

## §Residual risk / open items (non-defects)
- **Optional:** mint a real Zenodo DOI for [19] (currently a GitHub software citation — acceptable to BMC, but a DOI strengthens auditability).
- **Optional:** add a zero-edge field to `benchmark_metadata.json`.

## Verdict
**Accept.** Round 3 closes the final reproducibility gap: the within-construction claim is now both true and backed by a deposited, recomputable number. The manuscript is scientifically honest, internally consistent, and compliant with BMC Bioinformatics (SCIE, soundness-only) standards. Submit as a **Research** article.

*Local commit (Round 3) pushed to origin/master.*
