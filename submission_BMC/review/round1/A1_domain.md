# Reviewer A1 — Domain Expert (computational biology / pain & RA knowledge-graph science)
## Independent review of BMC Bioinformatics submission: "RA-PainKG: a tissue-contextualized knowledge graph for rheumatoid arthritis pain signaling with benchmark validation"

**Independence statement:** This review was written without access to any other reviewer reports, the authors' responses, the revision note, the submission manifest, or any simulation (`*_gen_*.py`) script. Conclusions are based solely on `manuscript_BMC.md`, `src/ra_painkg/config.py` (`CORE_PAIN_GENES`), and the gene lists in `benchmark/results/supplementary_table_S1.md` and `submission_BMC/supplementary/supplementary_tables.docx`.

---

## ITEM 1 — Two canonical pain genes (DRD2, COMT) are absent from the curated 192-gene core

【Problem】 The curated 192-gene set omits DRD2 and COMT, two of the most replicated, experimentally established pain-modulation genes in the human literature.

【Evidence】 `config.py` CORE_PAIN_GENES (20 categories) contains neither `DRD2` nor `COMT` in any category. The supplementary gene list (`supplementary_tables.docx`, "Annotated Pain Gene List (165 genes)") confirms `DRD2` is absent from the entire resource (token `DRD2` not present in the document), while `COMT` appears only as `expansion-discovered` (provenance label), not as a curated core gene. By contrast, the prompt's canonical panel is otherwise well covered in `config.py`: SCN9A, SCN10A, SCN11A, TRPV1, TRPA1, TRPM8, P2RX3, CALCA, NGF, NTRK1, OPRM1, PTGER2, PTGER4, TNF, IL6, IL1B are all present.

【Why it matters】 DRD2 (dopaminergic descending analgesia) and COMT (the val158met haplotype and experimentally demonstrated pain sensitivity; Diatchenko et al., Pain 2006) are foundational to the pain field. Their omission directly contradicts the manuscript's claim of a comprehensive, literature-curated pain-gene set (manuscript lines 13, 29, 37) and weakens the nociception/descending-modulation biology that the dual-track framework is supposed to capture. A curation that misses COMT/DRD2 invites the inference that inclusion was not systematically grounded in the pain-genetics literature.

【Specific fix】 Add both genes to the curated core (e.g., a "descending modulation" or existing neuropeptide/opioid-adjacent category) and cite the primary literature. Paste-ready replacement for the Stage 1 inclusion sentence (manuscript line 37):
> "Inclusion required (1) published experimental evidence for a role in pain signaling, nociception, or RA inflammation in at least two independent studies (PubMed: 'gene_symbol AND (pain OR nociception OR rheumatoid arthritis)'), or (2) designation as a known analgesic or RA drug target in the IUPHAR/BPS Guide to Pharmacology [14] or DrugBank. Canonical pain-modulation genes with replicated genetic or pharmacological evidence (e.g., SCN9A/Nav1.7, TRPV1, DRD2, COMT, OPRM1) were prioritized to ensure coverage of the descending, opioid, and inflammatory-sensitization axes; the full list with functional assignments and PMIDs is in Supplementary Table S1."

---

## ITEM 2 — The "nine pain signaling pathways" are never enumerated; 20 categories ≠ 9 pathways is undefined

【Problem】 The manuscript repeatedly asserts "nine core pain signaling pathways" and that "all nine pathways mapped at 57–100% coverage," but the nine pathways are never listed, and the relationship between the enumerated 20 functional categories and the claimed nine pathways is never defined.

【Evidence】 `manuscript_BMC.md` references "nine" pathways at lines 15 (Abstract), 29 (Background), 39 (Methods), 65, 69, 94, 124 (Results/Discussion/Conclusions), and the Figure 6 caption ("Pathway subnetwork visualizations for all nine curated pain signaling pathways"). However, only **four** of the nine are ever named — in the coverage sentence (line 69): complement cascade (57%), TRP channels (100%), voltage-gated sodium channels (100%), neurotrophin signaling (100%). The Methods Stage 1 list (line 37) enumerates **20** functional categories, several of which are not "pathways" at all (RA-specific genes, anesthetic targets, transcription factors, kinase signaling, inflammatory cytokines vs cytokine receptors counted separately). No mapping table from the 20 categories to the 9 pathways exists anywhere in the text.

【Why it matters】 The central, repeatedly stated claim — "all nine pathways mapped at 57–100% coverage" — is unverifiable and irreproducible. A reader cannot tell whether a pathway is a biological signaling cascade or a curation bucket, nor whether the 20 categories are a superset, subset, or orthogonal to the 9 pathways. This is a coherence defect that blocks domain validation of the resource's central organizing principle.

【Specific fix】 Add an explicit table (e.g., in Results or as Supplementary Table) titled "The nine curated pain signaling pathways," listing each pathway, its constituent 20-category members, the curated genes assigned to it, and the pathway's recovery/coverage denominator and numerator. Paste-ready sentence for line 29:
> "manual curation of 192 pain-relevant genes organized into 20 functional categories that instantiate nine core pain signaling pathways — (1) TRP channel transduction, (2) voltage-gated sodium channel transduction, (3) voltage-gated calcium channel transduction, (4) neuropeptide signaling, (5) neurotrophin signaling, (6) opioid system, (7) inflammatory cytokine/receptor signaling, (8) eicosanoid/prostaglandin signaling, and (9) complement cascade — with additional categories (MAPK, JAK–STAT, NF-κB, GABA/glycine and serotonin receptors, endocannabinoid, kinase, transcription factor, RA-specific, and anesthetic-target groupings) providing mechanistic context (Table X)."

---

## ITEM 3 — The "pathway coverage %" metric is undefined and contradicts the 97.9% recovery claim

【Problem】 "57–100% gene coverage" is never operationally defined, and a 57% floor is irreconcilable with the stated 188/192 (97.9%) presence of curated genes in the graph.

【Evidence】 Line 69: "All nine curated pathways mapped onto RA-PainKG at 57% (complement cascade) to 100% (TRP channels, voltage-gated sodium channels, neurotrophin signaling) gene coverage." Lines 73–78 state 188/192 genes are present in the final graph and that "No curated gene is genuinely absent." The `config.py` complement category contains 11 genes (C1QA, C1QB, C1QC, C2, C3, C5, C5AR1, C6, C7, C8A, C9); if 97.9% of curated genes are in the graph, a pathway "coverage" of 57% cannot mean "genes present in the graph." The numerator/denominator of "coverage" (node-based? edge-based subnetwork membership?) is unspecified, and the supplementary gene list shows only `C5` carrying complement track annotations, implying the metric measures something other than graph presence that is never defined.

【Why it matters】 The headline "all nine pathways mapped at 57–100%" can be (and likely will be) misread as incomplete capture of complement biology, directly undercutting the recovery claim two paragraphs later. Undefined metrics make the benchmark and the pathway results impossible to audit.

【Specific fix】 Define coverage explicitly and report it per pathway in a table. Paste-ready sentence for line 69:
> "All nine curated pathways are represented in RA-PainKG. Pathway coverage is defined as the fraction of curated genes assigned to pathway X that possess at least one edge within the X-specific subnetwork (n_nodes, n_with_edges / n_assigned): TRP channels 13/13 (100%), voltage-gated sodium 7/7 (100%), neurotrophin 7/7 (100%), … complement cascade 6/11 (57%); the lower complement coverage reflects sparser curated edges rather than gene absence, consistent with 188/192 (97.9%) overall recovery (Table Y)."

---

## ITEM 4 — Dual-track cardinalities are internally inconsistent and contradict the benchmark supplement

【Problem】 The Track A / Track B / overlap numbers do not reconcile, and the benchmark supplementary table reports a different, internally impossible set of track sizes.

【Evidence】 Manuscript lines 39 and 69: annotated set = 165 genes; Track A = 106; Track B = 122; overlap = 96. By inclusion–exclusion, |A ∪ B| = 106 + 122 − 96 = **132**, not 165 — 33 genes are unaccounted for by the two tracks. Line 80 then introduces a third, inconsistent total: "Within the 120 core genes that received dual-track annotations." Separately, `benchmark/results/supplementary_table_S1.md` carries the note: "Track A: n=3 genes (immune-inflammation). Track B: n=5 genes (nociception-pain transduction). Track Dual: n=96 genes spanning both tracks." This contradicts 106/122 and is itself impossible because 96 > the 44 Norman pain genes that the benchmark restricts to.

【Why it matters】 The dual-track framework is the paper's conceptual contribution and the basis for the Track A r / Track B r / Track Dual r benchmark columns (S1). Mutually contradictory cardinalities — 165 vs 132 vs 120 in the manuscript, and 3/5/96 in the supplement — destroy confidence in every track-stratified result and in the framework itself.

【Specific fix】 Recompute and publish a single consistent Venn: |A|, |B|, |A∩B|, and |neither|, and make the benchmark S1 note use those exact numbers. Paste-ready sentence for line 69:
> "The 165 annotated genes were assigned to Track A (immune-inflammation, n=106), Track B (nociception–pain transduction, n=122), or both (n=96), with n=33 genes carrying neither track label; |A ∪ B| = 132, and the 33 unlabeled genes are listed in Supplementary Table S2."

---

## ITEM 5 — The 58% overlap means the tracks are barely disjoint; the exclusive sets that justify the framework are tiny and unenumerated

【Problem】 With overlap 96 of 122 Track-B genes, the two tracks are overwhelmingly coincident, yet the manuscript presents the split as if it identifies separable intervention points without reporting the size or content of the exclusive sets.

【Evidence】 Recomputed from lines 39/69: 96/122 = **78.7%** of nociception genes are also inflammatory; 96/106 = **90.6%** of inflammatory genes are also nociceptive. The exclusive sets are therefore |A only| = 106 − 96 = **10** and |B only| = 122 − 96 = **26** — only ~22% of the annotated genes are track-exclusive. The manuscript acknowledges the overlap as "biologically expected" (lines 69–70) but never states these exclusive-set sizes nor enumerates the exclusive genes.

【Why it matters】 The utility claim — "genes exclusive to one track may mark intervention points where anti-inflammatory and analgesic effects partially decouple" (line 69–70) — rests on at most 36 genes that are never listed or validated. Without the exclusive sets, a reviewer cannot judge whether the dual-track lens adds anything beyond a relabeling of PrimeKG, and the large overlap suggests the split is largely overlapping rather than a meaningful biological partition.

【Specific fix】 Report the exclusive sets explicitly and state their evidentiary basis. Paste-ready sentence for lines 69–70:
> "The substantial overlap (96/165, 58.2%; 78.7% of Track B and 90.6% of Track A are shared) is biologically expected, as transcription factors (FOS, JUN, STAT3) and prostaglandins bridge inflammation and nociception. The 10 inflammation-only and 26 nociception-only genes are enumerated in Supplementary Table S2; of these, [X] have experimental evidence for inflammation–analgesia decoupling, and the remainder are flagged as candidate decoupling nodes pending validation."

---

## ITEM 6 — "Tissue-contextualized" overstates the resource; tissue data are descriptive metadata only

【Problem】 The title and stated contribution characterize the graph as "tissue-contextualized," but GTEx expression is stored only as node attributes and was explicitly not used to constrain any edge or node.

【Evidence】 Line 41: "These annotations are node attributes in the GraphML and CSV formats but were not used to filter edges in the current release, because removing edges on bulk tissue expression risks discarding valid low-expression interactions." Title (line 1) and Contributions (lines 13, 78, 94, 124) repeatedly emphasize "tissue-contextualized." The Limitations section (lines 112–113) itself notes GTEx lacks DRG and synovium and is bulk, not cell-type resolved.

【Why it matters】 A knowledge graph is not "tissue-contextualized" when tissue expression does not filter edges, nodes, or subnetworks — it is "tissue-annotated." The branding overstates biological novelty and may mislead users into believing tissue context shapes the network structure. The genuine (and modest) contribution is the transparent recovery/gap documentation, not tissue contextualization.

【Specific fix】 Either implement a tissue-based filtering step (even a simple median-TPM≥1 retention of edges between co-expressed nodes) or relabel. Paste-ready replacement for the title/subtitle claim (line 1) and Contribution (line 13):
> "RA-PainKG: a knowledge graph for rheumatoid arthritis pain signaling with tissue-expression annotation and benchmark validation" / "…integrates curated pain gene annotations with multimodal biomedical network data, provides GTEx v8 tissue-expression annotations for every pain gene, and transparently documents gene recovery and residual gaps."

---

## ITEM 7 — Missing must-cite primary literature for the pain-genetics and RA-pain basis of the curation

【Problem】 Several canonical primary references that justify the curation and the RA-pain dissociation are absent from the reference list, weakening the scholarly grounding of a gene set that (per Item 1) already omits COMT and DRD2.

【Evidence】 Reference list [1]–[22] includes RA burden/clinical-pain (Lee 2011 [3], McWilliams 2017 [4]), Basbaum 2009 [5], Julius 2013 [6], Ji 2018 [7], and the HP-GDB resource (Meloto 2018 [15]), but lacks: (i) the SCN9A/Nav1.7 channelopathy literature establishing sodium channels in human pain (e.g., Cox et al., Nature 2006; Dib-Hajj et al.); (ii) the COMT pain-sensitivity haplotype (Diatchenko et al., Pain 2006) — directly relevant to the omitted COMT; (iii) NGF/nerve-growth-factor in rheumatic/arthritis pain (e.g., Seidel et al., Nat Rev Rheumatol 2013; and the tanezumab clinical program); (iv) central sensitization as a unifying concept (Woolf, Pain 2011); and (v) large-scale human pain genetics beyond the HP-GDB entry (e.g., the International Pain Genetics Consortium / pain GWAS efforts).

【Why it matters】 For a resource whose central asset is a curated gene list, the curation must be demonstrably anchored in the primary pain/RA genetics literature. The absence of these citations — combined with the omission of their target genes (COMT, and the descending-modulation axis behind DRD2) — suggests the inclusion criteria were not systematically executed against the field's canonical evidence.

【Specific fix】 Add the following (or equivalent primary) citations and reference them at the relevant curation points:
- Cox JJ, et al. An SCN9A channelopathy causes congenital inability to experience pain. Nature. 2006;444(7121):894–898.
- Diatchenko L, et al. Catechol-O-methyltransferase gene polymorphisms are associated with multiple pain-evoking stimuli. Pain. 2006;119(1–3):86–95.
- Seidel MF, et al. Nerve growth factor in rheumatic diseases. Nat Rev Rheumatol. 2013;9(7):416–422.
- Woolf CJ. Central sensitization: implications for the diagnosis and treatment of pain. Pain. 2011;152(3 Suppl):S2–S15.
- Fields HL, Heinricher MM, Mason P. Neurotransmitters in nociceptive modulatory circuits. Annu Rev Neurosci. 1991;14:219–245. (justifies DRD2/descending dopamine in analgesia)

---

## ITEM 8 — Supplementary Table S1 as described does not match the delivered files; provenance is conflated with function

【Problem】 The manuscript's description of Supplementary Table S1 cannot be located in the delivered supplementary material, and the gene-list table conflates data provenance with biological function.

【Evidence】 Line 37: "The full list with functional assignments and PMIDs is in Supplementary Table S1." Yet (a) `submission_BMC/supplementary/supplementary_tables.docx` ("Supplementary Table S1: Annotated Pain Gene List (165 genes)") has columns Gene / Track A / Track B / Functional category / Recovered in PrimeKG — there is **no PMID column** (token `PMID` absent from the document) and it lists 165 genes (120 curated + 45 expansion), not the 192 curated set; (b) `benchmark/results/supplementary_table_S1.md` is a benchmark-results table, not a gene list, so the "S1" label is duplicated/ambiguated across two different files; (c) the docx uses the literal string `expansion-discovered` as a "Functional category" for 46 genes, treating data provenance as if it were biology; (d) the docx contains `CALCAN` (a typo for the HGNC symbol `CALCA`).

【Why it matters】 Reviewers and users cannot find the promised 192-gene curated table with PMIDs, and the provenance/function conflation (46 genes labeled "expansion-discovered" rather than, e.g., complement/cytokine/chemokine) reduces the reproducibility and biological interpretability of the curation.

【Specific fix】 Deliver the true 192-gene curated table with one PMID (or PMID set) per gene as Supplementary Table S1, exactly as promised; relabel the current 165-gene table as Supplementary Table S2; correct `CALCAN`→`CALCA`; and replace the `expansion-discovered` label with the actual biological category for each of the 45 expansion genes (e.g., CCR6→chemokine/receptor, COMT→catecholamine metabolism, IFNG→cytokine).

---

## § Stands up (things I suspected but found correct)

1. **Nociceptor transduction-channel coverage is genuinely strong.** Verified against `config.py`: SCN9A, SCN10A, SCN11A, TRPV1, TRPA1, TRPM8, P2RX3, ASIC1–ASIC4, PIEZO1/PIEZO2 are all present — a correct and comprehensive capture of the canonical peripheral nociceptor channelome (Basbaum 2009 [5]; Julius 2013 [6]).
2. **The immune-inflammation axis is well represented.** TNF, IL1B, IL6, IL1A, IL17A, IL23A, the cytokine receptors (TNFRSF1A/B, IL1R1, IL6R, IL6ST, IL17RA, IL23R), NF-κB (NFKB1/2, RELA, RELB, IKBKB/KG, CHUK), JAK–STAT, and MAPK are all present in `config.py`, supporting a biologically coherent Track A.
3. **The recovery/gap documentation is honest and correct.** The manuscript's classification of ACPA (not a gene symbol), NAPE-PLD→NAPEPLD, RANKL→TNFSF11 (alias resolution), and ADRA2B (construction artifact) matches `config.py` and is a real, well-executed piece of transparency — the strongest substantive claim in the paper.
4. **The prostaglandin/eicosanoid axis is appropriately detailed.** PTGS1/2, PTGES/2, PTGER1–4, ALOX5/12/15, LTA4H are present, supporting the RA pain eicosanoid biology that legitimately bridges immune activation and nociceptor sensitization.
5. **Benchmark self-honesty about K562 is a strength.** Lines 86 and 104 correctly flag that K562 cells are biologically mismatched to RA pain and that the K562 benchmark should not be read as a validity measure — this is appropriate scientific restraint.

---

## § Questions for the authors (do not guess — I need your answers)

1. What is the explicit, ordered list of the **nine** pathways, and which of the 20 categories (or genes) map to each? (Required to validate the "all nine pathways mapped" claim.)
2. How exactly is **pathway coverage %** computed — node presence, or edges within a pathway subnetwork? What are the denominator and numerator for each of the nine?
3. Why were **DRD2 and COMT** excluded from the curated 192 despite being canonical, replicated pain genes? Will you add them (and IFNG/CCR6, currently only "expansion-discovered") to the core?
4. What are the exact **|A only|** and **|B only|** gene sets (recomputed to resolve the 165/132/120 inconsistency), and are any of those exclusive genes experimentally validated inflammation–analgesia decoupling points?
5. Is "tissue-contextualized" intended to remain descriptive only, or will a future version use GTEx TPM to filter edges/nodes? If the latter, what threshold and what co-expression rule?
6. The benchmark S1 note reports Track A n=3, Track B n=5, Track Dual n=96 — which numbers are correct, and how were the benchmark track subsets derived from the 44 Norman pain genes (since 96 > 44)?

---

## § What I actually checked

- Read `submission_BMC/manuscript_BMC.md` in full (214 lines).
- Read `src/ra_painkg/config.py`; verified `CORE_PAIN_GENES` contains 20 categories and confirmed **absence** of DRD2, COMT, IFNG, CCR6 from the curated set; confirmed **presence** of SCN9A, SCN10A, SCN11A, TRPV1, TRPA1, TRPM8, P2RX3, CALCA, NGF, NTRK1, OPRM1, PTGER2, PTGER4, TNF, IL6, IL1B, and the complement (11 genes), prostaglandin, cytokine, NF-κB, JAK–STAT, MAPK categories.
- Extracted and parsed `submission_BMC/supplementary/supplementary_tables.docx`: confirmed it is the **165-gene** list (120 curated + 45 expansion), confirmed **no PMID column** (token `PMID` absent), confirmed **DRD2 absent** from the whole document, confirmed **COMT/CCR6/IFNG present only as `expansion-discovered`** (46 occurrences of that label), and confirmed the `CALCAN` typo for `CALCA`.
- Read `benchmark/results/supplementary_table_S1.md` (benchmark results table) and noted its note: "Track A: n=3 … Track B: n=5 … Track Dual: n=96," contradicting the manuscript's 106/122 and exceeding the 44 Norman pain genes.
- Recomputed dual-track arithmetic: 106 + 122 − 96 = **132 ≠ 165**; overlap fractions 96/122 = 78.7%, 96/106 = 90.6%; exclusive sets |A only| = 10, |B only| = 26.
- Sample-checked ≥10 canonical genes for PubMed-evidence plausibility against the already-cited pain/RA literature (Basbaum 2009; Julius 2013; Ji 2018) plus the must-cite primaries listed in Item 7: TRPV1, TRPA1, SCN9A, CALCA/CGRP, NGF, OPRM1, TNF, IL1B, IL6, PTGS2, P2RX3 — all biologically established; DRD2 and COMT are equally established yet absent (Item 1).

**Bottom line for the panel:** The nociceptor-channel and inflammatory-axis curation is sound, and the recovery/gap transparency is a genuine (if modest) contribution. However, the paper's two headline organizing claims — "nine pathways" and a "tissue-contextualized dual-track" framework — are currently unverifiable due to (a) the nine pathways never being enumerated, (b) an undefined coverage metric that contradicts the 97.9% recovery, (c) mutually inconsistent track cardinalities, and (d) tissue data that does not contextualize the graph. Combined with the omission of canonical genes (DRD2, COMT) and missing primary citations, these are major revisions, not minor edits.
