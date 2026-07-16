filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

changes = []
def replace(old, new, desc):
    global content
    if old in content:
        content = content.replace(old, new)
        changes.append(f"  [OK] {desc}")
        return True
    else:
        changes.append(f"  [MISS] {desc}")
        return False

# === CRITICAL FIXES ===

# F1a: Fix 38.6% to 59.1% in Abstract
replace(
    "K562 cells express pain genes at low levels (38.6% below mean expression 0.01, vs genome-wide mean 0.107), representing a conservative test scenario.",
    "Among 44 pain genes overlapping the Norman dataset, 59.1% (26/44) have mean expression below 0.01, compared to the genome-wide distribution (mean 0.107); mean pain-gene expression is 0.117. The low overlap and limited expression of nociception-specific genes in K562 cells represent a fundamental limitation for pain-specific conclusions.",
    "F1a: 38.6% -> 59.1% in Abstract"
)

# F1b: Fix same in Limitations section
replace(
    "1. **Cell-type mismatch:** K562 chronic myeloid leukemia cells are fundamentally mismatched to RA pain biology. Pain-relevant genes show low expression (mean expression 0.032 vs genome-wide mean 0.107, units of log-normalized counts; 38.6% of pain genes below 0.01 expression threshold), indicating that key nociceptive transcriptional programs are largely inactive in this cell line. Consequently, the null result for domain KG advantage should not be interpreted as evidence that domain-specific prior knowledge lacks value for pain biology\u2014only that no advantage was detectable in a system where pain genes are minimally expressed. Whether domain KGs improve prediction in disease-relevant models (e.g., iPSC-derived sensory neurons, DRG organoids) remains an open question.",
    "1. **Cell-type mismatch:** K562 chronic myeloid leukemia cells are fundamentally mismatched to RA pain biology. Among 44 pain genes present in the Norman K562 dataset, 59.1% (26/44) exhibit mean expression below 0.01 (log-normalized counts), and the mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107), indicating that nociception-specific transcriptional programs are largely inactive or indistinguishable from background in this cell line. Only 44 of 165 RA-PainKG pain genes (26.7%) are measurable in the Norman dataset. Consequently, the null result for domain KG advantage should not be interpreted as evidence that domain-specific prior knowledge lacks value for pain biology\u2014only that no advantage was detectable in a system where most pain genes are either absent or minimally expressed. Whether domain KGs improve prediction in disease-relevant models (e.g., iPSC-derived sensory neurons, DRG organoids) remains an open question.",
    "F1b: Limitations section pain expression corrected"
)

# F2: Fix CI [-0.085, +0.007] -> [-0.078, +0.000] in Abstract
replace(
    "delta = -0.039, 95% CI [-0.085, +0.007], p = 0.084, unadjusted",
    "delta = -0.039, 95% CI [-0.078, +0.000], p = 0.084, unadjusted",
    "F2: CI corrected in Abstract"
)

# Also fix in Results section
replace(
    "GO vs RA-PainKG showed no significant difference (Pearson r delta = -0.020, 95% CI [-0.058, +0.018], p = 0.084, paired t-test, Bonferroni threshold",
    "GO vs RA-PainKG showed no significant difference (Pearson r delta = -0.039, 95% CI [-0.078, +0.000], p = 0.084, paired t-test, Bonferroni threshold",
    "F2b: CI in Results section"
)

# F3: Fix "10 KG variants" -> "11 KG variants"
replace(
    "We evaluated 10 KG variants",
    "We evaluated 11 KG variants",
    "F3a: 10->11 in Methods (old eval)"
)
replace(
    "We benchmarked 10 KG variants",
    "We benchmarked 11 KG variants",
    "F3b: 10->11 in Abstract"
)

# F4: Fix delta +0.077 -> +0.078
replace(
    "delta = +0.077, 95% CI [+0.059, +0.096]",
    "delta = +0.078, 95% CI [+0.059, +0.096]",
    "F4: delta rounded correctly"
)

# M1: Add 44-gene overlap clarification to Abstract
replace(
    "significantly outperforming GO (r = 0.589 and 0.542; delta = +0.078, 95% CI [+0.059, +0.096], p < 0.001) and RA-PainKG (pain r = 0.503; delta = +0.117, 95% CI [+0.083, +0.150], p < 0.001).",
    "significantly outperforming GO (r = 0.589 and 0.542; delta = +0.078, 95% CI [+0.059, +0.096], p < 0.001) and RA-PainKG (pain r = 0.503, computed over 44 pain genes overlapping the Norman dataset; delta = +0.117, 95% CI [+0.083, +0.150], p < 0.001).",
    "M1: 44 pain gene overlap noted in Abstract"
)

# M2: Fix k range 32-256 -> 32-512 in Abstract  
replace(
    "sensitivity analyses for regularization (alpha = 0.001\u2013100.0) and embedding dimension (k = 32\u2013256)",
    "sensitivity analyses for regularization (alpha = 0.001\u2013100.0) and embedding dimension (k = 32\u2013512)",
    "M2: k range corrected"
)

# Also in Methods if there
replace(
    "embedding dimension sensitivity (k = 32\u2013256)",
    "embedding dimension sensitivity (k = 32\u2013512)",
    "M2b: k range in Methods"
)

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

ok = sum(1 for c in changes if "[OK]" in c)
print(f"\nDone. {ok}/{len(changes)} applied.")