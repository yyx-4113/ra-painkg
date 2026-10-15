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

188/192 (97.9%); 189/192 (98.4%); 192 genes; 20 functional categories; 9 pathways; 45 added genes → 165 annotated; Track A 106 / Track B 122 / overlap 96 (58.2%); 18,069 nodes (10 types); 127,226 edges (24 types); 2,400 PPI + 124,826 non-PPI edges; 4,760 drug–target edges; top hubs EGR1, FOS, STAT3, AKT1, SRC; pathway coverage 57–100%; 11 KG variants benchmark; Norman K562 91,205 cells / 5,045 genes / 284 conditions; k=128 embeddings; ridge λ=0.1; 10 splits; Bonferroni α=0.01 (m=5); Kendall's W 0.64–0.65; 280-fold sparser than GO; 68.3% zero-edge; 44/165 (26.7%) in Norman; 59.1% (26/44) K562 expr <0.01; mean pain-gene expr 0.117 vs background 0.107; seed-42 split r=0.558 vs 0.481, multi-split 0.503 vs 0.542.
