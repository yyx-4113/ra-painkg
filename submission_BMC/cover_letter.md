# Cover Letter — RA-PainKG → BMC Bioinformatics

**Date:** 2026-10-16

**To:** The Editorial Board, *BMC Bioinformatics* (Springer Nature / BMC)
**Manuscript type:** Research article
**Submission system:** Editorial Manager / Snapp (https://bmcbioinformatics.biomedcentral.com)

Dear Editors,

Please find enclosed our research article entitled:

**"RA-PainKG: a tissue-contextualized knowledge graph for rheumatoid arthritis pain signaling with benchmark validation"**

by Yongxin Yang (Department of Anesthesiology, The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, China).

## Summary of significance

Rheumatoid arthritis (RA) pain often persists despite adequate inflammation control, yet existing biological network resources treat RA as a single disease entity without separating pain-specific signaling from general inflammatory pathways or providing tissue context for nociception-relevant compartments. We present **RA-PainKG**, a directed, tissue-contextualized knowledge graph that integrates PrimeKG v1.0, GTEx v8 tissue expression across 54 human tissues, and manual curation of 192 pain-relevant genes organized into 20 functional categories spanning nine core pain signaling pathways. The graph contains 18,069 nodes and 127,226 directed edges, with 4,760 drug–target edges enabling direct pharmacological queries; 188/192 (97.9%) of curated pain genes are recovered, and all nine pathways map at 57–100% coverage. We further provide transparent benchmark validation across 11 knowledge-graph variants, establishing honest boundary conditions for downstream use.

The resource is released in GraphML, CSV, and Python pickle formats with complete analysis source code, supporting both hypothesis generation in pain biology and structured prior knowledge for machine learning.

## Declarations (per BMC requirements)

- **Ethics approval and consent to participate:** Not applicable — the study uses exclusively publicly available data; no new data involving human subjects or animals were collected.
- **Consent for publication:** Not applicable.
- **Availability of data and materials:** All code, graph files, and benchmark results are at https://github.com/yyx-4113/ra-painkg (MIT license). Source datasets: Norman et al. Perturb-seq (Harvard Dataverse DOI 10.7910/DVN/R9JDLS), PrimeKG v1.0 (DOI 10.7910/DVN/IXA7BM), GTEx v8, Gene Ontology.
- **Competing interests:** The author declares no competing interests.
- **Funding:** No specific funding; institutional resources supported the research.
- **Authors' contributions:** Yongxin Yang — conceptualization, methodology, software, formal analysis, investigation, data curation, writing, visualization, project administration.
- **AI-use disclosure:** During manuscript preparation the author used AI-assisted tools (OpenAI Codex CLI, GitHub Copilot, Claude via API) for code development, literature search, and language editing; all content was reviewed and verified by the author, who takes full responsibility for scientific accuracy.

This manuscript is original, has not been published elsewhere, and is not under consideration by any other journal. We confirm compliance with BMC's editorial policies.

Thank you for your consideration.

Yongxin Yang, on behalf of the author
Corresponding author: 960856791@qq.com · ORCID 0009-0004-9698-6552
