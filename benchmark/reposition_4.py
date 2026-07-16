filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Position-based replacement of Section 4.2
idx_start = content.find("### 4.2 Clinical Implications")
idx_next = content.find("### 4.3", idx_start)
if idx_next < 0:
    idx_next = content.find("### 4.4", idx_start)

old_section = content[idx_start:idx_next]

new_section = """### 4.2 Methodological Implications

Our results carry three implications for KG benchmarking methodology.

**Single-split artifacts are prevalent and consequential.** In our data, RA-PainKG appeared to outperform GO on pain genes under a single split (r = 0.558 vs 0.481, seed 42; a relative swing of +0.116 favoring the domain KG). Multi-split averaging reversed this result (0.503 vs 0.542). This single-split false positive demonstrates that KG benchmarking studies reporting results from a single train/test split risk drawing conclusions that are artifacts of the split rather than properties of the KG. We recommend a minimum of 10 splits with paired statistical tests and Bonferroni correction for primary comparisons.

**Ablation design is essential for causal inference.** The observation that Random > GO > RA-PainKG is correlational; the demonstration that degree-preserving randomization leaves performance indistinguishable (p = 0.41\u20130.83) is causal. The pain-gene-centric reduction of GO (GO-painCentric, retaining only edges incident to pain genes) also produces performance indistinguishable from full GO (p = 0.22), indicating that the vast majority of GO\u2019s predictive value concentrates in edges involving pain-relevant genes. Future KG benchmarking efforts should include topology-randomization and domain-reduction controls to separate density effects from semantic effects.

**Test system relevance bounds conclusions.** K562 cells express pain genes at levels comparable to the genomic background (mean 0.117 vs 0.107), with 59.1% of measurable pain genes below the expression threshold. Only 26.7% of RA-PainKG pain genes are present in the Norman dataset. Consequently, this benchmark provides strong evidence about density effects in linear models (established on over 5,000 non-pain genes across 10 splits) but cannot resolve whether domain-specific KGs would improve prediction in disease-relevant cell types. This question remains open and requires sensory neuron or DRG models.

**Note on extrapolation:** A preliminary two-point log-linear fit between RA-PainKG (~2,400 PPI edges) and GO-painCentric (~121,500 PPI edges) yields an extrapolated target of approximately 60,000 pain-relevant PPI edges for domain KG predictive parity. This estimate rests on only two data points and an unvalidated functional form; it should be treated as an order-of-magnitude guide rather than a quantitative prediction.

"""

content = content[:idx_start] + new_section + content[idx_next:]
print(f"[OK] Section 4.2 replaced ({len(old_section)} -> {len(new_section)} chars)")

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("Done.")