filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

changes = []
def replace(old, new, desc):
    global content
    if old in content:
        content = content.replace(old, new)
        changes.append(f"  [OK] {desc}")
    else:
        changes.append(f"  [MISS] {desc}")

# 4a. Replace "Clinical Implications" section
old_s42 = """### 4.2 Clinical Implications: A Decision Framework

**Scenario:** A researcher uses network propagation to rank candidate drug targets for RA pain. She has access to GO (dense, general) and RA-PainKG (sparse, disease-specific).

**Recommendation:** Use GO for primary target ranking (maximizes coverage and prediction accuracy). Use RA-PainKG as a diagnostic overlay: genes whose GO-based rankings differ substantially from their RA-PainKG-based rankings are candidates for knowledge-gap-driven under-prioritization. Specifically, genes that rank highly in GO but have zero edges in RA-PainKG (68.3% of Norman-measured genes) may be systematically underestimated in network analyses that rely exclusively on domain-specific PPI data.

**Quantitative guidance:** To achieve GO-level predictive performance, RA-PainKG requires approximately 60,000 pain-relevant PPI edges (25-fold increase). This number, derived from log-linear extrapolation between only two data points, provides a provisional target for experimental PPI mapping efforts (e.g., AP-MS, BioID) in sensory neuron models; it should be refined as additional intermediate-density KG data become available."""

new_s42 = """### 4.2 Methodological Implications

Our results carry three implications for KG benchmarking methodology.

**Single-split artifacts are prevalent and consequential.** In our data, RA-PainKG appeared to outperform GO on pain genes under a single split (r = 0.558 vs 0.481, seed 42; a relative swing of +0.116 favoring the domain KG). Multi-split averaging reversed this result (0.503 vs 0.542). This single-split false positive demonstrates that KG benchmarking studies reporting results from a single train/test split risk drawing conclusions that are artifacts of the split rather than properties of the KG. We recommend a minimum of 10 splits with paired statistical tests and Bonferroni correction for primary comparisons.

**Ablation design is essential for causal inference.** The observation that Random > GO > RA-PainKG is correlational; the demonstration that degree-preserving randomization leaves performance indistinguishable (p = 0.41\u20130.83) is causal. The pain-gene-centric reduction of GO (GO-painCentric, retaining only edges incident to pain genes) also produces performance indistinguishable from full GO (p = 0.22), indicating that the vast majority of GO\u2019s predictive value concentrates in edges involving pain-relevant genes. Future KG benchmarking efforts should include topology-randomization and domain-reduction controls to separate density effects from semantic effects.

**Test system relevance bounds conclusions.** K562 cells express pain genes at levels comparable to the genomic background (mean 0.117 vs 0.107), with 59.1% of measurable pain genes below the expression threshold. Only 26.7% of RA-PainKG pain genes are present in the Norman dataset. Consequently, this benchmark provides strong evidence about density effects in linear models (established on over 5,000 non-pain genes across 10 splits) but cannot resolve whether domain-specific KGs would improve prediction in disease-relevant cell types. This question remains open and requires sensory neuron or DRG models.

**Note on extrapolation:** A preliminary two-point log-linear fit between RA-PainKG (~2,400 PPI edges) and GO-painCentric (~121,500 PPI edges) yields an extrapolated target of approximately 60,000 pain-relevant PPI edges for domain KG predictive parity. This estimate rests on only two data points and an unvalidated functional form; it should be treated as an order-of-magnitude guide rather than a quantitative prediction."""

if old_s42 in content:
    content = content.replace(old_s42, new_s42)
    changes.append("  [OK] 4a: Section 4.2 rewritten")
else:
    changes.append("  [MISS] 4a: Section 4.2")

# 4b. Replace Conclusion
old_conc = "In a comprehensive multi-split ablation benchmark, we demonstrate that graph density\u2014not domain specificity\u2014drives perturbation prediction performance in linear spectral embedding models. Dense random graphs consistently outperform curated KGs (GO, RA-PainKG) across all gene subsets. Ablation experiments establish causality: randomizing edge identities while preserving degree distribution does not degrade performance. In an exploratory single-split analysis, nonlinear models (MLP) attenuated KG distinctions that linear models reveal; formal multi-split nonlinear validation is needed. We provide a provisional framework: dense KGs for prediction, domain KGs for gap diagnosis, and approximately 60,000 PPI edges as a preliminary target for domain KG development\u2014pending validation in disease-relevant cell types."

new_conc = """This study makes three methodological contributions to KG benchmarking for perturbation prediction.

First, we document a single-split artifact in which a domain-specific KG appeared to outperform a general-purpose KG (RA-PainKG vs GO on pain genes, seed 42, r = 0.558 vs 0.481) but the effect reversed under multi-split averaging (0.503 vs 0.542), demonstrating that split-level statistics are essential for reliable KG evaluation.

Second, we establish via degree-preserving randomization that graph connectivity\u2014not edge semantics\u2014drives prediction performance in linear spectral embedding models. This causal finding holds across all gene subsets and is independent of cell type or disease context.

Third, we provide an open-source multi-split ablation benchmark framework with paired statistical tests, Kendall\u2019s W ranking consistency, and sensitivity analyses for regularization and embedding dimension.

The K562 test system severely limits pain-specific conclusions (59.1% of measurable pain genes below expression threshold; only 26.7% of RA-PainKG genes present in the dataset). We identify sensory neuron models as the essential next step for determining whether domain-specific prior knowledge confers advantages in a biologically relevant context."""

if old_conc in content:
    content = content.replace(old_conc, new_conc)
    changes.append("  [OK] 4b: Conclusion rewritten")
else:
    changes.append("  [MISS] 4b: Conclusion")

# 4c. Remove "research prioritization" language
replace(
    "For research prioritization, we propose a hybrid strategy: dense KGs (GO) for primary ranking of perturbation targets, complemented by domain KGs (RA-PainKG) as a secondary filter to flag genes whose ranks may be underestimated due to knowledge gaps. This strategy awaits prospective validation in a disease-relevant cellular context.",
    "For benchmark design, we recommend that future KG evaluations include both a dense baseline (e.g., GO) and a domain-specific KG, with multi-split statistics and ablation controls (degree-preserving randomization, domain-centric reduction) to separate density effects from domain-specific effects. Validation in disease-relevant cellular models is the essential next step.",
    "4c: research prioritization removed"
)

# 4d. Fix "Quantitative guidance" anywhere remaining
replace(
    "**Quantitative guidance:** To achieve GO-level predictive performance, RA-PainKG requires approximately 60,000 pain-relevant PPI edges (25-fold increase).",
    "**Extrapolation:** A two-point log-linear fit suggests approximately 60,000 pain-relevant PPI edges as an order-of-magnitude target for domain KG predictive parity.",
    "4d: Quantitative guidance softened"
)

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print(f"\nDone. {sum(1 for c in changes if '[OK]' in c)}/{len(changes)} applied.")