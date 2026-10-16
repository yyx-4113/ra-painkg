# A3 — Provenance & Recomputation Audit (Round 2, Independent)

**Scope:** Re-verify every headline number in the REVISED manuscript (`manuscript_BMC.md`) directly from raw/deposited data, and scan for residual internal contradictions. No prior-round review files, `REVISION_NOTE.md`, `SUBMISSION_MANIFEST.md`, or `*_gen_*.py` were read. Judgement is from manuscript + deposited files only.

**Files used:** `manuscript_BMC.md`, `RA_PainKG_summary.json`, `graph_statistics.json`, `track_assignments.csv`, `full_benchmark_results.json`, `supplementary_table_S4.md`. Python: `C:/Python314/python.exe` (numpy/pandas available).

---

## 1. Composition / recovery (Tasks 1–2, 5)

### Recomputation
- `track_assignments.csv` → **165 rows** (matches "165 annotated genes", lines 15, 39, 43). ✅
- Track A (inflammation, True) = **106**; Track B (nociception, True) = **122**; both = **96**; neither = **33**. (Recomputed: 106+122−96 = 132; 165−132 = 33.) All match manuscript lines 15, 39, 69, 132 exactly. ✅
- 96/165 = 58.2% (line 69) — correct. ✅
- `seed_nodes.pain_gene_protein` = **190** (summary line 53) and `pain_gene_nodes` = **190** (graph_statistics line 44) → "190 seed gene/protein nodes" (line 39) verified. ✅
- 188/192 = 97.92% → 97.9%; 189/192 = 98.44% → 98.4% (lines 15, 39, 73, 89, 120). Percentages correctly rounded. ⚠️ Derivation NOT independently reproducible (see §Reproducibility Gap) but internally consistent with 190 seed nodes (188 exact-symbol present + 2 alias-resolved present = 190).

### 【Problem】 Line 39 "4 artifacts" contradicts Line 73 "recovered/present" (Task 5)
Line 39 states: *"Of the 192 curated genes, 72 were not retained …; 68 of these are present in the graph but were not assigned dual-track annotations, and 4 are identifier/construction artifacts."*
Line 73 states: *"NAPE-PLD and RANKL are present under the HGNC symbols NAPEPLD and TNFSF11 … ADRA2B is present but was not retained … the only residual items are (i) one construction artifact (ADRA2B) and (ii) identifier/alias notes (ACPA; NAPE-PLD→NAPEPLD; RANKL→TNFSF11)."*

The "4 artifacts" in line 39 must be {ACPA, NAPE-PLD, RANKL, ADRA2B}. But line 73 explicitly classifies **NAPE-PLD and RANKL as PRESENT (alias-resolved)** and ADRA2B as present-in-PrimeKG, and says the only true construction artifact is **ADRA2B (1)**, with ACPA/NAPE-PLD/RANKL being "identifier/alias notes." So:
- NAPE-PLD and RANKL are **present in the graph** → they belong in the "68 present-but-unannotated" group, not "artifacts."
- ADRA2B is **not in the final graph** → it cannot be "present in the graph but unannotated," yet it is lumped with the artifacts.

This is a genuine internal contradiction: line 39's "4 artifacts / 68 present" split double-counts items that line 73 treats as recovered.

### 【Evidence】
- Manuscript line 39 vs line 73 (quoted above).
- Logical reconstruction: 192−120 (curated core) = 72 not retained. Of the 4 "artifacts", only ACPA (non-gene) is genuinely absent; NAPE-PLD/RANKL are present (line 73); ADRA2B is present-in-PrimeKG but dropped. The only curated gene "genuinely absent" per line 73 is **none** (ACPA is not a gene).

### 【Why it matters】
The Recovery section's central claim — *"No curated gene is therefore genuinely absent from the underlying knowledge base"* (line 73) — is undermined by line 39 implying 4 "artifacts/gaps." A reader tallying "4 artifacts" as residual gaps conflicts with the stated genuine-absence = 0. This is exactly the kind of residual inconsistency a BMC reviewer will catch.

### 【Specific fix】
Recast line 39 so the two sections agree. Recommended wording:
> *"…and 4 require identifier/alias handling that kept them outside the curated-core annotated set: ACPA (a non-gene autoantibody marker), NAPE-PLD and RANKL (present under aliases NAPEPLD and TNFSF11), and ADRA2B (present in PrimeKG but excluded from the final graph). All four are represented in the underlying knowledge base, so genuine KB absence = 0, consistent with the Recovery section."*

And make the 72-split arithmetic consistent: redefine as **70 present-but-unannotated + 2 (ACPA non-gene, ADRA2B construction artifact) = 72**, OR keep "4" but explicitly state they are present-in-KB items outside the annotated core (so the count of genuine gaps stays 0). Either way, line 39 and line 73 must use the same vocabulary ("artifact" must not imply absence).

---

## 2. Graph statistics (Task 3) — ALL VERIFIED ✅

From `RA_PainKG_summary.json` and `graph_statistics.json` (both files agree; component sums equal the totals):
- Total nodes **18,069** (line 15, 43, 65): `sum(node_types)` = 18,069. ✅
- Total edges **127,226** (line 15, 43, 65): `sum(edge_relation_types)` = 127,226. ✅
- Node types **10** (line 67): both files list 10 keys. ⚠️ See Issue 3 (enumeration omits "exposure").
- Edge types **24** (line 43, 67): both files list 24 relation types. ✅
- `protein_protein` = **28,972** (line 43): matches. ✅
- non-PPI = 127,226 − 28,972 = **98,254** (line 43): correct. ✅
- `drug_protein` = **4,760** (lines 15, 43, 67, 89, 120): matches. ✅
- Top hubs by betweenness **EGR1, FOS, STAT3, AKT1, SRC** (lines 15, 67, 128): exactly equal `top_hubs_by_betweenness[:5]` in summary. ✅

---

## 3. Forbidden-fingerprint contradiction scan (Task 4)

| Fingerprint | Status | Location checked |
|---|---|---|
| (a) "2,400" in RESOURCE description | **ABSENT** ✅ | "2,400" appears only at lines 43, 49, 81 — all benchmark context. The resource description (lines 63–69, esp. line 65) lists only 18,069 nodes / 127,226 edges. No leak into resource section. |
| (b) "190+45=165" implication | **ABSENT** ✅ | 190 seed nodes (line 39) and 120+45=165 (line 39) are presented as separate quantities with no "190+45=165" arithmetic. No forbidden concatenation. |
| (c) "62.5%" reasserted as positive claim | **ABSENT** ✅ | Grep for "62.5" returns no match anywhere in the manuscript. |
| (d) NAPE-PLD / RANKL listed as NON-recoveries | **ABSENT** ✅ | Lines 47, 73, 95 reference them. Line 73 explicitly states they are **present** (alias-resolved). Line 95 calls them "identifier/symbol artifacts" but in the context "documents exactly which genes are present, which are identifier/symbol artifacts … and which were present in PrimeKG but not retained (ADRA2B)" — i.e., present, not non-recoveries. No forbidden fingerprint. |

**No forbidden fingerprints remain.** ✅

---

## 4. STRING r = 0.000 (Task 6)

### 【Problem】 "r = 0.000 on all subsets" is slightly overstated
Line 49: *"STRING PPI v12 … yielded zero predictive signal (r = 0.000 on all subsets)."*
Deposited `full_benchmark_results.json` → `STRING v12`: `pearson_r` = **0.0002656** (rounds to 0.000 ✅), but `pain_pearson_r` = **0.0007867** (rounds to **0.001**, not 0.000). The overall/seen signal is ≈0.000; the pain subset is ≈0.001.

### 【Evidence】
- Manuscript line 49 vs `full_benchmark_results.json["STRING v12"]`.

### 【Why it matters】
Trivial, but "0.000 on all subsets" is literally false for the pain subset; a reviewer checking the deposited JSON will see 0.0008.

### 【Specific fix】
Change to *"r ≈ 0.000 (|r| < 0.001; 0.0003 overall, 0.0008 on the pain subset)"* or *"effectively zero predictive signal."*

---

## 5. Additional residual inconsistencies found

### Issue 2 (COMT self-contradiction)
**【Problem】** `track_assignments.csv` contains `COMT,True,True` (row 26) — i.e. COMT IS in the current 165-gene annotated set (it must be one of the 45 expansion genes, since it is not in the 192 curated list). Yet line 112 (Limitations) states: *"The initial 192-gene set omits two canonically implicated pain/analgesia genes, DRD2 and COMT, which should be incorporated in a future release."* COMT is already incorporated; only DRD2 is genuinely absent (DRD2 ∉ CSV).
**【Evidence】** CSV row 26 vs manuscript line 112.
**【Why it matters】** Self-contradiction in the Limitations section; reduces trust in the curation accounting.
**【Specific fix】** Rewrite line 112 to state only DRD2 remains to be added, noting COMT was recovered via the 2-hop expansion and is already in the annotated set.

### Issue 3 (Entity-type enumeration incomplete)
**【Problem】** Line 67 says *"10 entity types"* but enumerates only 9: gene/protein, drug, disease, pathway, biological process, molecular function, cellular component, anatomy, phenotype — **"exposure" (83 nodes) is omitted**. The count 10 is correct (summary has 10 types incl. exposure); the enumerated list is not.
**【Evidence】** Line 67 vs `node_type_distribution` (10 keys, incl. `exposure`:83).
**【Why it matters】** Minor factual gap; a careful reviewer will flag the mismatch between stated count and listed items.
**【Specific fix】** Add "exposure" to the enumerated list in line 67 (and use a consistent label for `effect/phenotype`).

### Issue 5 (Deposited benchmark file is not "full")
**【Problem】** Manuscript describes **11 KG variants** (lines 49–50). Deposited `full_benchmark_results.json` contains only **5** keys: GO-BP, STRING v12, RA-PainKG PPI, Random (same density), Identity. Missing: the 5 random realizations, GO-painCentric, RA-PainKG-degPreserved. (`supplementary_table_S4.md` has some pairwise comparisons but not the per-variant r dumps.)
**【Evidence】** Benchmark JSON key count = 5 vs manuscript "11 variants."
**【Why it matters】** Reproducibility: the file named "full_benchmark_results" cannot reproduce the 11-variant claim.
**【Specific fix】** Deposit complete results for all 11 variants (or rename the file and note the subset).

---

## § Stands up (verified-correct numbers)

All of the following were recomputed from deposited files and match the manuscript exactly:
- 18,069 nodes / 127,226 edges (component sums reconcile). [L15,43,65]
- 10 node types, 24 edge types. [L43,67]
- `protein_protein` = 28,972; non-PPI = 98,254; `drug_protein` = 4,760. [L43]
- Top-5 hubs EGR1/FOS/STAT3/AKT1/SRC = `top_hubs_by_betweenness[:5]`. [L15,67,128]
- 165 annotated genes (CSV row count). [L15,39,43]
- Track A=106, Track B=122, both=96, neither=33 (CSV exact). [L15,39,69,132]
- 96/165 = 58.2%. [L69]
- 190 seed gene/protein nodes = `seed_nodes.pain_gene_protein` (190). [L39]
- 188/192=97.9%, 189/192=98.4% (rounding correct; derivation dependent on undeposited recovery map — see below).
- Internal arithmetic that IS checkable: 44/165 = 26.7% [L43,99]; 26/44 = 59.1% [L81,99]; 1,600/5,045 = 31.7% [L49]; 68.3% zero-edge [L81]; 673,899/2,400 = 280.8 ≈ 280-fold [L81]; GO-BP density 0.0265, GO-painCentric 0.0048, RA-PainKG 0.00009 [L49] — all reconcile against the stated edge counts.
- STRING overall r ≈ 0.000 (deposited 0.00027). [L49]
- Forbidden fingerprints (a)–(d) all ABSENT. [L43,49,81 ; none ; L47,73,95]

---

## § Reproducibility Gap (Task 7 — numbers NOT reproducible from deposited files)

The following headline numbers **cannot be independently recomputed** from the files provided, because the required source artifacts are not in the deposited set:

| Number | Manuscript | Missing source file |
|---|---|---|
| 188/192 present; 189/192 exact-symbol match | L15,39,73,89,120 | Final-graph node symbol set + 192-gene list + recovery map (S3) |
| 120 curated + 45 expansion split; "72 not retained"; "68 present-but-unannotated" | L39 | 192-gene list with curated/expansion flag (S1) |
| 44/165 Norman overlap (26.7%) | L43,99 | S6 (Norman vocabulary overlap) |
| 2,400-edge PPI benchmark variant | L43,49,81 | PPI-variant adjacency matrix |
| 1,600/5,045 (31.7%) with ≥1 edge | L49 | Edge-incidence over Norman genes |
| 50% (Track B) / 20% (Track A) zero PPI edges | L75 | PPI subgraph + track membership |
| 190 seed derivation (188+2 alias) | L39 | Final-graph node symbol set (to confirm NAPEPLD/TNFSF11 present) |

What IS verifiable: 190 seed (summary field), and 165/106/122/96/33 (CSV). The 188/189 and composition splits rest on files not deposited here. **Recommend depositing S1, S3, S6, and the final-graph node symbol list / PPI variant matrix** so the recovery accounting is fully auditable.

---

## § Residual risk

- **Primary risk:** The recovery accounting (line 39 vs line 73) is internally contradictory and, because the recovery map (S3) and 192-gene list are not deposited, the true "68/4" vs "70/2" split cannot be confirmed by an independent auditor. If the recovery map were deposited, the count could shift to **70 present-but-unannotated + 2 genuine (ACPA, ADRA2B)**. Until deposited, the manuscript's gap documentation is not fully auditable.
- **Secondary risk:** COMT contradiction (Issue 2) and the incomplete benchmark JSON (Issue 5) suggest the "revised" manuscript still carries round-1 artifacts not fully cleaned.
- None of the issues above alter the headline scientific conclusions (graph size, track structure, hub genes, transparent benchmark null result).

---

## Verdict: **MINOR**

No fabricated numbers, no forbidden fingerprints (2,400-in-resource, 190+45=165, 62.5%, NAPE-PLD/RANKL-as-non-recoveries) were found. Every directly verifiable graph and track statistic matches the raw data **exactly**. The defects are: (1) one genuine internal contradiction — line 39 "4 artifacts" vs line 73 "recovered/present" (Task 5); (2) COMT limitation self-contradiction; (3) minor enumeration (exposure), STRING-r precision, and an incomplete "full" benchmark file. All are fixable with small text edits + depositing S1/S3/S6. **Recommend Minor revision; do not reject.**
