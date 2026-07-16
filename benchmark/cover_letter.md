# Cover Letter

**Date:** July 16, 2026

**To:** Editor-in-Chief
*Journal of Biomedical Informatics*

**From:** Yongxin Yang (杨永新)
Department of Anesthesiology
The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine
Fuzhou 350000, Fujian, China
Email: 960856791@qq.com

---

Dear Editor,

I am pleased to submit our manuscript entitled **"Domain-Specific versus Dense Knowledge Graphs for Gene Perturbation Prediction: A Multi-Split Ablation Benchmark"** for consideration for publication in the *Journal of Biomedical Informatics*.

**Summary of Contribution**

This study addresses a methodological gap in biomedical informatics: how to rigorously benchmark knowledge graph (KG) contributions to machine learning models for gene perturbation prediction. Using GEARS-style spectral decomposition with ridge regression, we evaluated 11 KG variants across 10 independent train/test splits, with paired statistical tests and two causal ablation designs.

The key methodological findings are:

1. **Single-split evaluation produces artifacts.** We document a case where RA-PainKG (a disease-specific KG for rheumatoid arthritis pain signaling) appeared to outperform Gene Ontology under one split (pain r = 0.558 vs 0.481) but the effect reversed under multi-split averaging (0.503 vs 0.542). This demonstrates that split-level statistics are essential for reliable KG benchmarking.

2. **Causal evidence via ablation.** Degree-preserving randomization of RA-PainKG produces statistically indistinguishable performance (p = 0.41–0.83), establishing that graph connectivity—not edge semantics—drives prediction in linear spectral embedding models.

3. **Open-source benchmark framework.** We provide a complete multi-split ablation benchmark with paired t-tests, Kendall's W ranking consistency, and sensitivity analyses, along with all code and data at https://github.com/yyx-4113/ra-painkg.

We believe this manuscript aligns with JBI's scope in biomedical informatics methodology, specifically addressing evaluation standards for knowledge graph integration in machine learning pipelines.

**Declarations**

- This manuscript has not been published previously and is not under consideration elsewhere.
- The author declares no competing interests.
- This study uses exclusively publicly available data (Norman et al., 2019; DOI: 10.7910/DVN/R9JDLS). No new data involving human subjects were collected.
- All code, processed data, and benchmark results are publicly available under the MIT license at https://github.com/yyx-4113/ra-painkg.

**Suggested Reviewers** (optional)

1. A researcher with expertise in knowledge graph benchmarking and biomedical network analysis
2. A researcher with expertise in single-cell perturbation prediction and GEARS methodology
3. A researcher with expertise in biomedical informatics evaluation standards

Thank you for considering this manuscript. I look forward to your response.

Sincerely,

**Yongxin Yang (杨永新)**

---

## Submission Package Checklist

| Item | File | Status |
|------|------|--------|
| Manuscript | `benchmark/methods_paper.md` | ✅ Ready |
| Cover Letter | `benchmark/cover_letter.md` | ✅ This file |
| Supplementary Table S1 | `benchmark/results/supplementary_table_S1.md` | ✅ |
| Supplementary Table S2 | `benchmark/results/supplementary_table_S2.md` | ✅ |
| Supplementary Table S3 | `benchmark/results/supplementary_table_S3.md` | ✅ |
| Supplementary Table S4 | `benchmark/results/supplementary_table_S4.md` | ✅ |
| Supplementary Table S5 | `benchmark/results/supplementary_table_S5.md` | ✅ |
| Code & Data Repository | https://github.com/yyx-4113/ra-painkg | ✅ Public |
| Figures | `output/fig1-6.pdf` | ✅ Ready |
| Ethics Statement | Included in manuscript | ✅ |
| Competing Interests | Included in manuscript | ✅ |
| Author Contributions | Included in manuscript | ✅ |

**JBI Submission URL:** https://www.editorialmanager.com/jbi/