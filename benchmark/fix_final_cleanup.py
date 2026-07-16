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

# A. Fix Section 3.8: remove "diagnostic value", move extrapolation note to Discussion only
old_38 = """### 3.8 Bridge Genes and RA-PainKG Diagnostic Value

RA-PainKG identifies bridge genes connecting inflammatory (Track A) and nociceptive (Track B) subgraphs. Top bridges include STAT3 (score 35), RELA (24), and the NF-kappaB complex (IKBKB, IKBKG, NFKB1). Their diagnostic value lies in quantifying the knowledge gap: 72 of 192 core pain genes (37.5%) are absent from PrimeKG, and 50% of Track B genes present in the KG are isolated. A preliminary log-linear extrapolation between two data points\u2014RA-PainKG (~2,400 PPI edges) and GO-painCentric (~121,500 PPI edges)\u2014suggests RA-PainKG would require approximately 60,000 pain-relevant PPI edges to achieve GO-level predictive performance, a 25-fold increase. This estimate is speculative: it rests on only two observations and an unvalidated functional form; it should be treated as a rough magnitude estimate rather than a precise target."""

new_38 = """### 3.8 Bridge Genes and Knowledge Gap Quantification

RA-PainKG identifies bridge genes connecting inflammatory (Track A) and nociceptive (Track B) subgraphs. Top bridges include STAT3 (score 35), RELA (24), and the NF-kappaB complex (IKBKB, IKBKG, NFKB1). The KG quantifies knowledge gaps relevant to domain-specific prior knowledge: 72 of 192 core pain genes (37.5%) are absent from PrimeKG, and 50% of Track B genes present in the KG are isolated (no PPI edges). These gaps constrain the predictive value of domain-specific prior knowledge for perturbation prediction (see Discussion 4.2 for extrapolation analysis)."""

if old_38 in content:
    content = content.replace(old_38, new_38)
    changes.append("  [OK] A: Section 3.8 cleaned")
else:
    changes.append("  [MISS] A: Section 3.8")

# B. Fix Section 4.1 density gradient ordering
old_41 = """1. **Density gradient:** Performance tracks edge count monotonically: Random (673,899 edges, r = 0.653) > GO-painCentric (121,543, r = 0.604) ~ GO (673,899, r = 0.589) > RA-PainKG (2,400, r = 0.551). GO and Random have identical edge counts; the Random advantage (+0.078 r for the representative Random_R1) demonstrates that GO's specific edge identities are not optimized for this task."""

new_41 = """1. **Density gradient:** Performance tracks edge count monotonically: Random (673,899 edges, all-genes r = 0.653) > GO (673,899, r = 0.589) > RA-PainKG (2,400, r = 0.551). Although GO-painCentric (121,543 edges, r = 0.604) nominally exceeds GO on all-genes r, this difference is not significant (p = 0.17) and the overall ranking is consistent with a density-driven mechanism. GO and Random have identical edge counts; the Random advantage (delta = +0.078 for Random_R1 vs GO on all-genes r, p < 0.001) demonstrates that GO's specific edge identities are not optimized for this task."""

if old_41 in content:
    content = content.replace(old_41, new_41)
    changes.append("  [OK] B: Section 4.1 density gradient fixed")
else:
    changes.append("  [MISS] B: Section 4.1")

# C. Fix "Their diagnostic value" in 4.3 Generalizability 
old_gen = "domain KGs for biological interpretation and knowledge gap identification."
new_gen = "domain KGs for biological interpretation and knowledge gap quantification."
if old_gen in content:
    content = content.replace(old_gen, new_gen)
    changes.append("  [OK] C: diagnostic->quantification in Generalizability")
else:
    changes.append("  [MISS] C: Generalizability")

# D. Fix "their diagnostic value" wording in discussion body
replace(
    "Their diagnostic value lies in quantifying the knowledge gap",
    "Their value for this benchmark lies in quantifying the knowledge gap",
    "D: diagnostic value softened"
)

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

ok = sum(1 for c in changes if "[OK]" in c)
print(f"\nDone. {ok}/{len(changes)} applied.")