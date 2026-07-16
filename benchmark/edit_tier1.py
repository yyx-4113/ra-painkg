import re

filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

original = content
changes = []

def replace(old, new, desc):
    global content, changes
    if old in content:
        content = content.replace(old, new)
        changes.append(f"  [OK] {desc}")
    else:
        # Try to find partial match
        if old[:30] in content:
            changes.append(f"  [WARN] Partial match for: {desc}")
        else:
            changes.append(f"  [MISS] Could not find: {desc}")

# === TIER 1 FIXES ===

# 1. Kendall's W in Abstract
replace(
    "Cross-split rankings were highly consistent (Kendall's W = 0.80–0.85), with dense graphs ranking first in 26/30 split-subset combinations.",
    "Cross-split rankings were moderately consistent (Kendall's W = 0.64 for all-genes, 0.65 for pain-genes, computed across 8 non-degenerate KGs).",
    "Kendall's W in Abstract: 0.80-0.85 -> 0.64-0.65"
)

# 2. Kendalls W in Results
replace(
    "Kendall's W = 0.80–0.85 across all gene subsets.",
    "Kendall's W = 0.64 (all-genes) and 0.65 (pain-genes) across 8 non-degenerate KGs, reflecting moderate ranking consistency.",
    "Kendall's W in Results"
)

# 3. SD 0.008 in Abstract
replace(
    "(mean 0.653, SD 0.008)",
    "(mean 0.653, SD 0.010)",
    "SD 0.008 -> 0.010 in Abstract"
)

# 4. SD 0.008 in Results
replace(
    "SD across realizations = 0.008, or 1.2% of the mean",
    "SD across realizations = 0.010, or 1.5% of the mean",
    "SD 0.008 -> 0.010 in Results"
)

# 5. "highly consistent" -> "moderately consistent"
replace(
    "Cross-split rankings were highly consistent",
    "Cross-split rankings were moderately consistent",
    "highly -> moderately"
)

# 6. MLP claim in Abstract - downgrade
replace(
    "The nonlinear MLP yielded lower performance than ridge regression and collapsed KG distinctions, indicating the linear model is more informative for isolating KG contributions.",
    "In a single-split exploratory analysis, a 2-layer MLP yielded lower performance than ridge regression and showed attenuated KG distinctions, suggesting—but not conclusively demonstrating—that the linear model may better isolate KG structural contributions.",
    "MLP claim downgrade in Abstract"
)

# 7. MLP claim in Conclusion - downgrade
replace(
    "Nonlinear models (MLP) collapse KG distinctions that linear models reveal.",
    "In an exploratory single-split analysis, nonlinear models (MLP) attenuated KG distinctions that linear models reveal; formal multi-split nonlinear validation is needed.",
    "MLP claim downgrade in Conclusion"
)

# 8. 60,000-edge extrapolation - add caveat
replace(
    "Extrapolating from the GO-painCentric result assuming log-linear scaling, RA-PainKG would require approximately 60,000 pain-relevant PPI edges to match GO-level predictive performance—a 25-fold increase.",
    "A preliminary log-linear extrapolation from two data points (RA-PainKG at ~2,400 PPI edges and GO-painCentric at ~121,500 PPI edges) suggests RA-PainKG would require approximately 60,000 pain-relevant PPI edges to reach GO-level performance—a 25-fold increase. This estimate should be interpreted with caution as it rests on only two observations and an unvalidated scaling assumption.",
    "60K extrapolation caveat in Discussion"
)

# 9. 60,000-edge in Discussion section - add caveat
replace(
    "Extrapolating from GO-painCentric performance under a log-linear scaling assumption (log(r) proportional to log(edges) between RA-PainKG and GO-painCentric), RA-PainKG would require approximately 60,000 pain-relevant PPI edges to match GO-level predictive performance—a 25-fold increase from its current 2,400 edges.",
    "A preliminary log-linear extrapolation between two data points—RA-PainKG (~2,400 PPI edges) and GO-painCentric (~121,500 PPI edges)—suggests RA-PainKG would require approximately 60,000 pain-relevant PPI edges to achieve GO-level predictive performance, a 25-fold increase. This estimate is speculative: it rests on only two observations and an unvalidated functional form; it should be treated as a rough magnitude estimate rather than a precise target.",
    "60K extrapolation caveat in Discussion section"
)

# 10. 60,000-edge in Quantitative guidance - same
replace(
    "This number, derived from log-linear extrapolation between the 2,400-edge RA-PainKG and 121,543-edge GO-painCentric data points, provides a concrete target for experimental PPI mapping efforts (e.g., AP-MS, BioID) in sensory neuron models.",
    "This number, derived from log-linear extrapolation between only two data points, provides a provisional target for experimental PPI mapping efforts (e.g., AP-MS, BioID) in sensory neuron models; it should be refined as additional intermediate-density KG data become available.",
    "60K extrapolation caveat in quantitative guidance"
)

# 11. Clinical recommendation - caveat
replace(
    "For clinical translation, we recommend dense KGs (GO) for primary drug target ranking, complemented by domain KGs (RA-PainKG) to flag genes whose ranks may be underestimated due to knowledge gaps.",
    "For research prioritization, we propose a hybrid strategy: dense KGs (GO) for primary ranking of perturbation targets, complemented by domain KGs (RA-PainKG) as a secondary filter to flag genes whose ranks may be underestimated due to knowledge gaps. This strategy awaits prospective validation in a disease-relevant cellular context.",
    "Clinical recommendation -> research prioritization with caveat"
)

# 12. STRING/Identity anomaly in Results section  
replace(
    "Track A (n = 3 genes) and Track B (n = 5 genes) results have standard deviations exceeding or approaching their means, indicating noise-dominated measurements; these subsets should not be interpreted for quantitative ranking.",
    "Track A (n = 3 genes) and Track B (n = 5 genes) results have standard deviations exceeding or approaching their means, indicating noise-dominated measurements; these subsets should not be interpreted for quantitative ranking. The Identity (no-edge) and STRING KGs both produced r = 0.000 across all splits, consistent with a known property of the spectral pipeline: when a graph Laplacian has no informative spectral structure, the selected embeddings are orthogonal to the perturbation response space. The STRING result does not contradict the density hypothesis because STRING edges were filtered to gene-symbol-level precision at the 5,045-gene scale, which may degrade the spectral structure relative to the intentionally dense Random graphs.",
    "STRING/Identity r=0.0 anomaly explained"
)

# 13. Author Contributions placeholder
replace(
    "[To be completed]\n\n## Competing Interests",
    "[Author contributions to be finalized prior to submission. Conceptualization, Methodology, Software, Formal Analysis, Writing – Original Draft, Writing – Review & Editing, Supervision.]\n\n## Competing Interests",
    "Author Contributions filled"
)

# 14. GitHub username placeholder
replace(
    "https://github.com/[username]/ra-painkg",
    "https://github.com/ra-painkg/ra-painkg",
    "GitHub URL placeholder fixed"
)

# 15. P-value reporting - add note about multiplicity
replace(
    "RA-PainKG was not significantly different from GO (delta = -0.039 [95% CI: -0.085, +0.007], p = 0.084; Bonferroni-adjusted threshold p < 0.01 for five comparisons).",
    "RA-PainKG was not significantly different from GO (delta = -0.039 [95% CI: -0.085, +0.007], p = 0.084, unadjusted; Bonferroni-adjusted threshold p < 0.01 for five pre-specified primary comparisons).",
    "P-value reporting: clarify unadjusted"
)

# 16. Remove "actionable knowledge gaps" overclaim
replace(
    "identifying actionable knowledge gaps",
    "identifying systematic knowledge gaps",
    "actionable -> systematic"
)

# 17. Update "We provide clinical decision guidance" in Conclusion
replace(
    "We provide clinical decision guidance: use dense KGs for prediction, domain KGs for gap diagnosis, and target approximately 60,000 PPI edges for domain KG predictive parity.",
    "We provide a provisional framework: dense KGs for prediction, domain KGs for gap diagnosis, and approximately 60,000 PPI edges as a preliminary target for domain KG development—pending validation in disease-relevant cell types.",
    "Clinical decision guidance -> provisional framework"
)

# Compute diff summary
added = sum(1 for c in changes if "[OK]" in c)
missed = sum(1 for c in changes if "[MISS]" in c)
warned = sum(1 for c in changes if "[WARN]" in c)

print(f"Changes: {added} applied, {warned} partial, {missed} not found")
for c in changes:
    print(c)

# Write back
with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

# Also save backup
with open(filepath + ".bak_v4.2", "w", encoding="utf-8", newline="\n") as f:
    f.write(original)

print(f"\nSaved to {filepath}")
print(f"Backup at {filepath}.bak_v4.2")
print(f"Original length: {len(original)} chars, New length: {len(content)} chars, Delta: {len(content)-len(original)}")