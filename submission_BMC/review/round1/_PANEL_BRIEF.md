# RA-PainKG → BMC Bioinformatics — Independent Review Panel Brief (Round 1)

**Manuscript:** `D:/麻醉科共病/ra-painkg/submission_BMC/manuscript_BMC.md` (companion DOCX `manuscript_BMC.docx`).
**Target:** *BMC Bioinformatics* (Springer Nature; SCIE, JIF 2025 = 4.4; soundness-only editorial policy; Research article).
**Study claim in one line:** RA-PainKG is a tissue-contextualized, dual-track knowledge graph for rheumatoid-arthritis (RA) pain, built on PrimeKG v1.0 + GTEx v8 + manual curation of 192 pain genes / 20 categories / 9 pathways; validated by a benchmark over 11 knowledge-graph variants on the Norman K562 Perturb-seq dataset.

## Independence discipline (mandatory)
You are reviewing this **as if you have never seen it**. Forbidden to read:
- Any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md` in this or any sibling directory.
- `SUBMISSION_MANIFEST.md`, `REVISION_NOTE.md`, `cover_letter.md`, `declarations.md` in `submission_BMC/`.
- Any other reviewer's output file under `submission_BMC/review/`.
- `author_verification_statement.md`, any `GITHUB_DEPOSIT_SOP.md`, `*_gen_*.py` simulation scripts (do NOT treat them as real peer review).
Treat the manuscript as a first submission. Every judgement must come from text or raw source data you read yourself.
**Any claim in the manuscript that you CAN verify, you MUST verify** (recompute from source, not from the manuscript's own summary).

## Output contract (every item needs all four)
- 【Problem】 one sentence.
- 【Evidence】 pinned to file:line, or section/table + exact numbers; numbers you cite MUST be ones you recomputed yourself.
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance.
- 【Specific fix】 paste-ready English replacement sentence, or an explicit spec for a new analysis (variables, strata, output columns).
"Consider strengthening the discussion" is banned.

## Also required
- § Stands up (≥3, with evidence) — things you suspected but found correct.
- § Questions for the authors — what you need to know; do not guess answers.
- § What I actually checked — files read, commands run, values recomputed vs the manuscript's, with the discrepancy stated.

## Source-of-truth paths (read these, do not trust the manuscript's arithmetic)
- Code: `D:/麻醉科共病/ra-painkg/src/ra_painkg/*.py` (esp. `config.py`, `network_analysis.py`, `kg_builder.py`, `seed_nodes.py`, `track_assigner.py`, `gtex_filter.py`)
- Graph stats: `D:/麻醉科共病/ra-painkg/output/RA_PainKG_summary.json`, `output/graph_statistics.json`, `output/track_assignments.csv`, `output/seed_nodes.csv`, `output/RA_PainKG_nodes.csv`, `output/RA_PainKG_edges.csv`
- Benchmark: `D:/麻醉科共病/ra-painkg/benchmark/results/` (`benchmark_results.json`, `supplementary_table_S1.md`…`S5.md`, `benchmark_jbi.csv`, `benchmark_multisplit*.json`, `split_info.json`, `predictions_*.npy`)
- Manuscript numbers to recompute and cross-check (do NOT accept at face value): 188/192 (97.9%), 189/192 (98.4%), top-5 hubs = EGR1/FOS/STAT3/AKT1/SRC, 165 annotated genes, Track A 106 / Track B 122 / 96 overlap, 18,069 nodes / 10 types, 127,226 edges / 24 types, 4,760 drug–target edges, 2,400 PPI + 124,826 non-PPI, 44/165 (26.7%) overlap Norman vocab, 1,600/5,045 (31.7%) have ≥1 RA-PainKG edge, benchmark densities (GO-BP 0.0265; GO-painCentric 0.0048; RA-PainKG 0.00009), multi-split r values (RA-PainKG 0.503 vs GO 0.542; seed-42 0.558 vs 0.481), K562 stats (91,205 cells, 5,045 genes, 284 conditions, 59.1% pain genes <0.01 expr, mean pain-gene expr 0.117 vs background 0.107, 280-fold sparsity), STRING v12 r = 0.000, the 4 stated "non-recovered" genes (ACPA, NAPE-PLD, RANKL, ADRA2B).

## Environment traps
- `python` may not be on PATH; use `C:/Python314/python.exe` (has NetworkX? verify by importing; if missing, install into a venv or use the managed venv `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/bin/python`). For `.npy`/`json`/`csv` use stdlib + `numpy`/`pandas` if available, else report what you could not run.
- A `.docx` is a zip; to verify text use the `zipfile` stdlib (read `word/document.xml`, strip tags) if python-docx is unavailable.
- The repo `.gitignore` excludes `output/*.graphml/*.pkl/*_edges.csv`; the graph is distributed as GitHub Release v1.0.0 assets, not in the git tree. Verify graph stats from `output/RA_PainKG_summary.json` / `graph_statistics.json` / the CSVs which ARE tracked.

## Forbidden
Do NOT mention what tools you use. Write review comments only. Do NOT edit any source or manuscript files — review output ONLY.
