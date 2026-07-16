# JBI Comprehensive Dual-Expert Review — RA-PainKG Benchmark (v4.2)
## Journal: *Journal of Biomedical Informatics*
## Reviewers: Reviewer #1 (Statistical ML / Bioinformatics) & Reviewer #2 (Clinical Informatics / KG Methodology)
## Review Philosophy: Rejection-targeted, comprehensive, actionable

---

## REVIEWER #1 — Statistical Machine Learning & Bioinformatics Expert

### OVERALL ASSESSMENT: **REJECT** (Major Concerns, Potentially Resolvable)

This manuscript reports a benchmark comparing domain-specific knowledge graphs (RA-PainKG) against general-purpose KGs (GO) and random graphs for gene perturbation prediction. The core finding is null: domain-specific KGs do not improve prediction over dense random graphs. While negative results have scientific value, the manuscript suffers from **critical data-reporting inaccuracies, insufficient statistical rigor, and overinterpretation of null findings** that preclude publication in JBI in its current form.

---

### MAJOR CONCERNS

#### M1. **CRITICAL: Kendall's W values are grossly inflated in the manuscript**

The Abstract/Results claim "Kendall's W = 0.80-0.85" for cross-split ranking consistency. **Independent verification of the benchmark_jbi_extended.csv data yields W = 0.647 (all-genes) and W = 0.639 (pain-genes).** This is not a rounding discrepancy — the reported values are inflated by approximately 30%. If the authors computed W differently (e.g., on a different subset of KGs or metrics), this must be explicitly stated. Otherwise, this constitutes a serious reporting error that undermines reader trust in all numerical claims.

**Required action:** Recompute Kendall's W explicitly using only the 8 non-degenerate KGs (GO, RA-PainKG, GO-painCentric, 5× Random_R), report the correct values (0.64-0.65), and explain any methodological differences from the original calculation. All conclusions about "highly consistent" rankings must be tempered.

#### M2. **Multiple reporting discrepancies between claims and data**

| Claim in manuscript | Verified from CSV | Discrepancy |
|---|---|---|
| Random all-genes SD = 0.008 | SD = 0.010 | +25% error |
| Random_R1 vs GO r_all delta = +0.078 | delta = +0.077 | Minor |
| Kendall's W = 0.80-0.85 | W = 0.64-0.65 | CRITICAL |
| Delta CIs use ±1.96×SE (paired) | Verified CIs are narrower | Method mismatch |

**Required action:** Every numerical claim in the Results section must be verified against the raw CSV data and corrected.

#### M3. **Bonferroni correction is inconsistently applied**

The Abstract mentions "Bonferroni-adjusted threshold p < 0.01 for five comparisons." However: (a) the paper makes far more than 5 comparisons (at minimum: 10 KG pairs × 2 metrics × 5 gene subsets = potentially 100+ comparisons); (b) the Bonferroni adjustment is applied only to a cherry-picked subset; (c) for the core null finding (RA-PainKG vs GO), the unadjusted p=0.084 is reported without noting that it becomes even more non-significant under any reasonable multiplicity correction. This selective application of correction is a form of p-hacking.

**Required action:** Apply consistent multiple comparison correction across all reported comparisons, or explicitly state which comparisons were pre-registered as primary and which are exploratory. Report both raw and adjusted p-values.

#### M4. **The single-split MLP comparison is methodologically inadequate**

The paper makes a strong claim: "nonlinear models collapse KG distinctions." This claim rests on a **single train/test split** with a single architecture (2-layer MLP, 128 hidden units). This is insufficient to support the generalization. The authors acknowledge this limitation but then proceed to make sweeping statements in the Abstract and Conclusion. Either:

(a) Run 10-split MLP benchmarks matching the linear model protocol, OR
(b) Downgrade the MLP claim to "exploratory/qualitative" throughout the manuscript (Abstract, Results, Discussion, Conclusion) and remove it from the Abstract entirely.

#### M5. **60,000-edge extrapolation is unsupported black-box modeling**

The Discussion claims that RA-PainKG "would require approximately 60,000 pain-relevant PPI edges to match GO-level predictive performance — a 25-fold increase." This extrapolation rests on an unvalidated "log-linear scaling" assumption with **two data points** (GO-painCentric and RA-PainKG). With n=2, any curve can be fit perfectly — this is curve-fitting, not prediction. The extrapolation from ~2,400 edges to 60,000 edges (25×) is wildly out of sample. This claim should be removed or presented as speculation with explicit caveats about the n=2 limitation.

#### M6. **Identity/STRING baseline produces r=0.0 across all splits — unexplained anomaly**

The Identity KG (no edges) and STRING KG both produce r=0.000 exactly across all 10 splits and all gene subsets. This is statistically implausible. An unregularized regression with no KG features should produce some non-zero correlation by chance alone in a high-dimensional setting. This suggests either: (a) a coding bug where the Identity baseline is hardcoded to zero, (b) the Laplacian eigenvector selection fails for the zero-edge case in a way that produces degenerate embeddings, or (c) the ridge regression degenerates. The authors must explain this result technically and demonstrate that the Identity baseline is correctly implemented.

#### M7. **Overinterpretation of null/negative results as positive contributions**

The paper frames its null findings as a "benchmark framework" contribution. While this is valid, the Discussion overreaches: "Domain KGs serve a complementary diagnostic function by identifying actionable knowledge gaps." This clinical recommendation is not supported by any clinical validation. The paper shows that RA-PainKG underperforms dense graphs on K562 leukemia cells — it does not demonstrate that it "identifies actionable knowledge gaps" in any meaningful clinical sense.

---

### MINOR CONCERNS

#### m1. **Abstract is excessively long and dense**

At ~350 words, the Abstract far exceeds JBI's typical 250-word structured abstract format. The Abstract reads more like a mini-paper than a summary. It should be restructured with clear Objective/Methods/Results/Conclusion headings and tightened.

#### m2. **"10 KG variants" counting is confusing**

The Abstract says "10 KG variants" but the actual breakdown includes: GO-BP, RA-PainKG, 5× random, 2× ablation, Identity, STRING = 11 entities. The counting methodology should be clarified.

#### m3. **No main-text Figures or Tables**

The manuscript references Supplementary Tables S1-S5 and Figures but includes no main-text tables or figures. JBI requires at least one graphical abstract or key figure. The current version is a wall of text.

#### m4. **Reference [4] is a self-citation to an unpublished companion paper**

Citing an "In preparation" companion Data Descriptor creates a circular dependency. Either publish the Data Descriptor first or describe RA-PainKG construction sufficiently in this manuscript.

#### m5. **Pain gene expression statistics need verification**

The claim "38.6% below mean expression 0.01" uses a threshold of 0.01 without justification. Is this TPM? log-normalized counts? The units and normalization method are unclear.

---

## REVIEWER #2 — Clinical Informatics & Knowledge Graph Methodology Expert

### OVERALL ASSESSMENT: **REJECT** (Major Conceptual and Translational Gaps)

This manuscript tackles an important question — whether domain-specific KGs improve over general KGs for perturbation prediction — but fails to deliver a compelling answer due to **fundamental design limitations, clinical irrelevance of the test system, and inadequate framing of null results**. The benchmark is technically competent but scientifically incomplete.

---

### MAJOR CONCERNS

#### M1. **K562 leukemia cells are fundamentally unsuitable for RA pain research**

The authors benchmark RA-PainKG — a graph built for rheumatoid arthritis pain signaling in nociceptive tissues — using K562 chronic myeloid leukemia cells. The authors acknowledge this mismatch (38.6% of pain genes below 0.01 expression) but frame it as a "conservative test." This framing is incorrect: a test system that does not express the biology of interest cannot serve as a valid negative control. If pain genes are not expressed in K562 cells, no KG — domain-specific or general — can meaningfully predict their perturbation responses because the relevant transcriptional programs are absent. This is analogous to testing a cardiac drug target predictor on kidney cells and concluding the drug targets are not predictive.

**Required action:** Either (a) replicate on a DRG/sensory neuron dataset (e.g., Sharma et al. 2020, Ray et al. 2018), (b) restrict claims to the expressed gene subset and acknowledge the test system may be fundamentally invalid for pain-specific conclusions, or (c) reframe the entire paper as a methodological benchmark without clinical claims.

#### M2. **The clinical translation narrative is unsupported**

The Discussion recommends: "use dense KGs (GO) for primary drug target ranking, complemented by domain KGs (RA-PainKG) to flag genes whose ranks may be underestimated." This recommendation has never been tested. It is purely speculative. The paper demonstrates that domain KGs underperform dense KGs, not that using both together improves clinical decision-making. The "clinical decision guidance" in the Conclusion should be removed or clearly labeled as speculation requiring prospective validation.

#### M3. **RA-PainKG construction methodology is not described**

The paper repeatedly references RA-PainKG as a domain-specific KG but does not describe its construction. The reader is directed to a companion Data Descriptor that is "In preparation" ([4]). For the benchmark to be reproducible and interpretable, the essential construction details (seed nodes, edge sources, filtering criteria, final edge count by type) must appear in this manuscript, not in an inaccessible companion paper.

#### M4. **The dual-track framework (Track A/B) is mentioned but not leveraged**

RA-PainKG organizes genes into Track A (immune-inflammation) and Track B (nociception-pain transduction). However, the benchmark reports Track A/B performance only in passing and does not use track membership for any stratified analysis beyond reporting r_trackA and r_trackB values. This is a missed opportunity: if Track B genes are the ones most mismatched to K562 biology, the null result could be partially explained by track-level analysis. A track-stratified analysis could reveal whether domain KG advantages exist within the expressed Track A subset.

#### M5. **The term "noise-dominated subsets" is undefined and potentially misleading**

The Results mention "noise-dominated subsets" without defining what constitutes a "noise-dominated" gene set. Is this based on expression variance? Perturbation effect size? If the D3 gene pool or other subsets show low signal, this should be quantified (e.g., intra-class correlation, heritability) rather than dismissed as "noise-dominated."

#### M6. **STRING KG yields r=0.0 — suggests implementation problem**

The STRING PPI network has 673,899 edges — more than GO-BP. If graph density drives prediction, STRING should outperform GO. Instead, STRING produces r=0.000, identical to the Identity (no-edge) baseline. This contradicts the paper's central thesis that density drives performance and strongly suggests an implementation issue with STRING edge filtering or Laplacian computation. This must be investigated and explained.

---

### MINOR CONCERNS

#### m1. **RA prevalence figure format is ambiguous**

The Abstract/Introduction mentions "0.5-1.0%" RA prevalence. The en-dash is technically correct but the range is imprecise. The Safiri 2019 reference reports 0.24% (95% UI 0.23-0.25%) global age-standardized prevalence — much lower than 0.5-1.0%. Verify the source or specify that 0.5-1.0% refers to adult prevalence in Western populations.

#### m2. **"Compute time approximately 12 minutes" — missing hardware context**

The Abstract notes "Total compute time was approximately 12 minutes." Without specifying CPU/GPU/RAM, this metric is meaningless. Was this on a laptop? A cluster node? An HPC environment?

#### m3. **Missing Author Contributions and incomplete metadata**

The Author Contributions section is empty ("[To be completed]"), and the GitHub URL contains a placeholder username ("[username]"). JBI requires complete author metadata at submission.

#### m4. **Section numbering is inconsistent**

The paper jumps from "4.5 Limitations" to "4.6 Conclusion." Sections 1-4 are numbered but the Abstract lacks a section number. The internal consistency of numbering should be verified.

#### m5. **Literature review omits key related work**

The Introduction does not cite:
- Recent GEARS alternatives (e.g., scGPT, GenePT, scFoundation models)
- Other KG-in-ML benchmarks beyond GEARS
- Prior work on spectral decomposition sensitivity to graph structure
- Work on K562 as a perturbation testbed and its limitations

---

## SYNTHESIS: CONVERGENT CRITICISMS

Both reviewers independently identify:

1. **Kendall's W inflation** — a factual data-reporting error (R1-M1)
2. **K562 cell-type mismatch** — fundamental to validity of pain-specific conclusions (R1, R2-M1)
3. **STRING/Identity r=0.0 anomaly** — suggests implementation issue (R1-M6, R2-M6)
4. **Overinterpretation of null results** — clinical recommendations unsupported (R1-M7, R2-M2)
5. **Unpublished companion paper** — undermines reproducibility (R1-m4, R2-M3)
6. **Missing author metadata** — incomplete submission (R2-m3)

---

## REQUIRED REVISIONS (Priority-Ordered)

### TIER 1 — Must Fix (Blocking)
1. Recompute and correct Kendall's W from CSV data (W ≈ 0.64-0.65, not 0.80-0.85)
2. Fix Random all-genes SD (0.010, not 0.008)
3. Investigate and explain STRING/Identity r=0.0 anomaly
4. Remove or heavily caveat the 60,000-edge extrapolation (n=2)
5. Downgrade MLP claims to exploratory throughout
6. Complete Author Contributions and fix GitHub URL
7. Report both raw and adjusted p-values consistently

### TIER 2 — Should Fix (Major Improvement)
8. Add RA-PainKG construction summary (seed nodes, edge counts by type)
9. Add track-stratified analysis (Track A vs B performance)
10. Restructure Abstract to ≤250 words
11. Add at least one main-text Figure or Table
12. Address K562 cell-type limitations more honestly

### TIER 3 — Would Improve
13. Clarify pain gene expression units and threshold justification
14. Specify hardware for compute time claims
15. Expand literature review with recent related work
16. Verify RA prevalence figure against cited source

---

**EDITORIAL SUMMARY:** This manuscript is not ready for publication in JBI. The core finding (domain KGs do not improve prediction) is scientifically interesting but is undermined by data-reporting errors, an inappropriate test system for pain biology, unsupported clinical extrapolations, and methodological anomalies that remain unexplained. A major revision addressing all Tier 1 and Tier 2 items would be required before re-review.