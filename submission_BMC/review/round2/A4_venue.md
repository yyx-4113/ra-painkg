# A4 — Venue & Reporting-Compliance Review (Round 2)
**Target journal:** BMC Bioinformatics (Springer Nature; SCIE; 2025 JIF ≈ 4.4; soundness-only policy)
**Article types in scope:** Research, Database
**Reviewer role:** Independent venue & reporting-compliance check — judged solely from the manuscript + BMC standards (prior-round files not consulted).
**Manuscript reviewed:** `manuscript_BMC.md` (full read, 210 lines). Numbers cross-checked against `supplementary_table_S4.md` where relevant.

---

## 1. Structured-abstract word count & citations (Task 1)

**【Problem】** None — compliance confirmed, with one minor editorial note.

**【Evidence】**
- Abstract is properly structured with `Background` (L13), `Results` (L15), `Conclusions` (L17) headings; `Keywords` present (L19).
- Word count (Background + Results + Conclusions, whitespace tokens, parentheticals counted as tokens):
  - Background: 61 words
  - Results: 133 words
  - Conclusions: 41 words
  - **Total = 235 words** (well within BMC's ≤350 limit; ~67% headroom).
- No bracketed/numeric citations appear anywhere in the abstract (L11–L19). Confirmed clean.

**【Why it matters】** BMC enforces a ≤350-word structured abstract and forbids in-abstract citations; both rules are satisfied.

**【Specific fix】** None required. (Optional: trim the Results sub-section if a stricter house word budget is later imposed — not needed now.)

**Verdict on Task 1:** PASS.

---

## 2. Declarations block completeness (Task 2)

**【Problem】** None — all BMC-mandatory subsections present.

**【Evidence】** Declarations block (L142–L163) contains, verbatim:
- `Ethics approval and consent to participate` (L144) — "Not applicable." ✓
- `Consent for publication` (L147) — "Not applicable." ✓
- `Availability of data and materials` (L150) ✓
- `Competing interests` (L153) ✓
- `Funding` (L156) ✓
- `Authors' contributions` (L159) ✓
- `Acknowledgements` (L162) ✓

All seven BMC-required headings are present and individually headed. "Not applicable." is acceptable for the ethics/consent items for a computational, no-human-subjects study.

**【Why it matters】** BMC rejects manuscripts missing any mandatory Declarations heading; none are missing here.

**【Specific fix】** None. (Optional, non-blocking: consider adding an `Authors' information` paragraph — BMC permits but does not require it.)

**Verdict on Task 2:** PASS.

---

## 3. Self-citation [19] — software/code citation without a real DOI (Task 3)

**【Problem】** Reference [19] is a self-citation that names "GitHub/Zenodo" but supplies **no Zenodo (or any) DOI** — it is a bare GitHub URL. The label is misleading.

**【Evidence】**
- L203: `[19] Yang Y. RA-PainKG: … GitHub/Zenodo. 2026. Available at: https://github.com/yyx-4113/ra-painkg.`
- The "Availability of data and materials" statement (L151) points to a GitHub Release v1.0.0 with SHA-256 checksums but likewise cites **no persistent archive DOI** (Zenodo/Software Heritage).
- BMC's policy expects software/code/data to be archived in a recognized repository with a persistent identifier (DOI); a moving GitHub URL is not a durable citation and is not, by itself, a citable "Zenodo" artifact.

**【Why it matters】** (a) Reproducibility/soundness: a versioned DOI snapshot is the durable object a reviewer/reader should cite; a GitHub branch can change. (b) Honesty: labeling the item "Zenodo" while providing only a GitHub URL is inaccurate. (c) Self-citation placed at [19] is acceptable, but it must resolve to a real, archived, citable object.

**【Specific fix】**
- Mint a Zenodo DOI for the v1.0.0 release (or a Software Heritage archive) and cite that DOI in [19] (e.g., `Yang Y. RA-PainKG (v1.0.0). Zenodo. 2026. https://doi.org/10.xxxx/zenodo.XXXXXXX`).
- Correct the repository URL in the Availability statement to point at the same archived DOI (keep the GitHub URL as the development home, separate from the archival citation).
- If a DOI cannot be minted before submission, at minimum change "GitHub/Zenodo. 2026." to "GitHub. 2026." and remove the false "Zenodo" attribution; still add the release tag/SHA-256 (already present) so the exact version is recoverable.

**Verdict on Task 3:** MINOR (must fix before acceptance — DOI/label correction).

---

## 4. Title overclaim — "with benchmark validation" (Task 4)

**【Problem】** The title foregrounds "benchmark validation," which connotes a positive performance confirmation, whereas the benchmark reports a **NULL result**: random and degree-preserving null graphs match or exceed RA-PainKG (L101; S4: random vs RA-PainKG Δr = +0.115, p < 0.001; degree-preserved Δr = +0.005, p = 0.83).

**【Evidence】**
- Title (L1): `… with benchmark validation`.
- L101: RA-PainKG "confers no predictive advantage over a structureless or degree-matched null on this task; we report this transparently as a boundary condition, not as evidence of resource quality."
- L99–L103: K562 is "fundamentally mismatched to RA pain biology"; performance "should not be interpreted as a measure of RA-PainKG's biological validity."

**【Why it matters】** For a soundness-only journal, a title implying validation success misrepresents the actual (null) finding and invites an overclaim rejection. The body text is already honest; the title must match.

**【Specific fix】** Soften the title subtitle, e.g.:
- `RA-PainKG: a tissue-contextualized knowledge graph for rheumatoid arthritis pain signaling with transparent benchmark characterization`
- or `… with benchmark characterization and boundary analysis`.
Keep "validation" only if it is explicitly framed as *null/boundary* validation in the title (less clean). Preferred: "transparent benchmark characterization."

**Verdict on Task 4:** MINOR (recommend softening; journal could flag as overclaim).

---

## 5. Reference format: Vancouver, spot-checks, ordering (Task 5)

**【Problem】** Vancouver style is used, and spot-checks [13] and [16] are correct, but **two citation-number ordering violations** (and a cascade) exist vs. first-appearance-in-text order.

**【Evidence】**
- Style: numbered, sequential, author–title–journal–year–volume–pages — consistent Vancouver. ✓
- Spot-check [13] (L191): `Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine. Sci Data. 2023;10:67.` — **correct** (PrimeKG, Scientific Data 2023, 10:67). ✓
- Spot-check [16] (L197): `GTEx Consortium. … Science. 2020;369(6509):1318–1330.` — **correct** (GTEx, Science 2020, 369:1318–1330). ✓
- No duplicate entries among [1]–[22]. ✓
- **Ordering error A — [16]↔[17] swapped:** DisGeNET `[17]` is first cited at L27 ("DisGeNET [17]"), but GTEx `[16]` is first cited later at L29 ("GTEx v8 … [16]"). Vancouver requires numbering by first appearance, so DisGeNET should be [16] and GTEx [17]; they are reversed.
- **Ordering error B — [19]↔[20] swapped:** Norman `[20]` is first cited at L53 ("Norman et al. … [20]"), but the self-citation `[19]` (Yang) is first cited at L59 ("[19]"). Norman should be [19] and Yang [20]; reversed.
- **Cascade:** because of the swaps, `[18]` (Nguyen DRG, first cited L107), `[21]` (GEARS, L55), and `[22]` (GO, L151) also fall out of strict first-appearance sequence. A clean renumber is needed, not just two local swaps.

**【Why it matters】** BMC mandates Vancouver sequential numbering by first textual appearance; mis-numbering is a formal compliance defect editors routinely return for correction, and cross-references in the text ([16], [17], [19], [20]) currently point to the wrong semantic entries if a reader re-sorts by order.

**【Specific fix】** Renumber the entire reference list to match first-appearance order. Correct sequence should be: [1]–[15] unchanged; then **[16] = Piñero/DisGeNET (currently [17])**, **[17] = GTEx (currently [16])**, **[18] = Norman (currently [20])**, **[19] = Roohani/GEARS (currently [21])**, **[20] = Yang self-cite (currently [19])**, **[21] = Nguyen DRG (currently [18])**, **[22] = Ashburner/GO (unchanged)**. Re-run an automated reference checker after renumbering.

**Verdict on Task 5:** MINOR (ordering must be corrected; spot-checks otherwise correct).

---

## 6. Overclaim / absolute-language scan (Task 6)

**【Problem】** No absolute self-claims of novelty/superiority remain; the one flagged phrase at L95 is hedged and defensible, but can be marginally softened.

**【Evidence】**
- No self-use of `novel`, `first`, `unique`, `state-of-the-art`, `superior`, or `unprecedented` was found (grep). The only `novel` is in reference [21] (GEARS paper title); `outperform` at L83 is used *honestly* to describe the seed-42 artifact that later reverses ("the effect reversed under multi-split averaging") — not a claimed win.
- L73 honestly states the gene set is "an already well-covered gene set," consistent with the non-novel framing — good internal consistency, no contradiction with any "first/unique" claim.
- L95: "A knowledge graph that explicitly documents what it does and does not contain is, to our knowledge, rarely implemented; … systematic per-gene recovery documentation with categorized absence reasons has few precedents." This is qualified ("to our knowledge", "few precedents") and therefore **defensible**, not an absolute overclaim. It is the only claim bordering on a distinctiveness assertion.
- Benchmark is reported as a null/boundary result throughout (L81, L99–L103, L120) — appropriately humble.

**【Why it matters】** Soundness-only BMC tolerates hedged distinctiveness claims; absolute "first/unique" claims would breach honesty. The manuscript is largely clean; only L95 needs a light touch.

**【Specific fix】** (Optional, low priority) At L95, keep the "to our knowledge" hedge (already present) and consider "uncommon" instead of "rarely implemented" if the author wants to avoid any challenge — but current wording is acceptable. No change is mandatory.

**Verdict on Task 6:** PASS (one optional softening; no blocking overclaim).

---

## 7. Article-type recommendation (Task 7)

**【Recommendation】** Submit as a **Research article**, not a **Database** article.

**【Evidence / reasoning】**
- BMC "Database" articles describe a curated, freely available **database with a stable web/query interface** (typically a live resource). RA-PainKG is released as static files (GraphML/CSV/pickle) on GitHub with a versioned release + SHA-256 (L65, L151) — it has **no hosted queryable database front-end**, so it does not fit BMC's "Database" definition and could be desk-rejected or re-typed by the editor.
- The manuscript is fundamentally a **research study**: it constructs a resource, applies a recovery/gap methodology, and reports a benchmarking experiment with explicit null/boundary findings (L77–L103). This maps cleanly to BMC Bioinformatics "Research article."
- Under soundness-only policy, the honest, null-result benchmark framing is a strength for a Research article (it demonstrates rigorous self-assessment) and avoids the "validation success" expectation a Database article title might invite.
- If the author later stands up a web-accessible query interface, a follow-up "Database" article would then be appropriate.

**【Specific fix】** Set article type = "Research" in the submission system. Do not select "Database."

**Verdict on Task 7:** Research (reasoned).

---

## § Stands up (compliant items)
- Structured abstract within word limit (235/350) and free of citations (Task 1).
- All 7 mandatory Declarations subsections present and individually headed (Task 2).
- Vancouver style correctly applied; [13] PrimeKG and [16] GTEx spot-checks accurate; no duplicate references (Task 5 partial).
- No `novel`/`first`/`unique` self-claims; honest null-result benchmark framing; internally consistent with the "already well-covered gene set" admission (Task 6).
- Benchmark numbers in the text match Supplementary Table S4 exactly (random vs RA-PainKG Δr = +0.115 p<0.001; degree-preserved Δr = +0.005 p=0.83).

## § Residual risk
- **Blocking-for-compliance (pre-acceptance):** (a) [19] lacks a real DOI / mislabels "Zenodo" (Task 3); (b) reference-list numbering violates Vancouver first-appearance order ([16]/[17] and [19]/[20] swapped, with cascade) (Task 5).
- **Editorial/overclaim risk:** title "with benchmark validation" implies positive validation against a null result (Task 4) — soften to avoid an overclaim flag.
- **Low priority:** optional softening of L95 "rarely implemented" (already hedged).
- **Strategic:** selecting "Database" article type risks desk rejection; use "Research" (Task 7).

## Verdict
**MINOR** — The manuscript is scientifically honest and structurally sound for BMC Bioinformatics, but requires three minor pre-acceptance fixes: (1) provide/correct a DOI for self-citation [19] and stop labeling it "Zenodo" without one; (2) renumber the reference list to Vancouver first-appearance order; (3) soften the title's "benchmark validation" to "benchmark characterization." None are substantive soundness defects; all are format/honesty-polish items resolvable in a single revision. Recommend **accept after minor revision**.
