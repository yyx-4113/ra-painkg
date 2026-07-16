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

# 1a. Abstract Objective
replace(
    "**Objective:** To determine whether domain-specific knowledge graphs (KGs) improve gene perturbation prediction over general-purpose KGs, using a rheumatoid arthritis (RA) pain signaling KG (RA-PainKG) as the test case.",
    "**Objective:** To establish rigorous methodology for benchmarking knowledge graph (KG) contributions to gene perturbation prediction, using a rheumatoid arthritis (RA) pain signaling KG as a worked example of domain-specific prior knowledge.",
    "1a: Abstract Objective repositioned"
)

# 1b. Abstract Discussion
replace(
    "**Discussion:** Graph density, not domain specificity, drives perturbation prediction accuracy in this setting. Domain KGs serve a diagnostic function by quantifying knowledge gaps (37.5% of core pain genes absent from PPI databases). A preliminary two-point extrapolation suggests approximately 60,000 pain-relevant PPI edges would be needed for domain KG predictive parity. The K562 test system limits pain-specific conclusions; replication in sensory neuron models is needed.",
    "**Discussion:** The dominant methodological finding is that single-split evaluation produces artifacts in KG benchmarking: RA-PainKG appeared to outperform GO in one split (pain r = 0.558 vs 0.481) but reversed under multi-split averaging (0.503 vs 0.542). Ablation experiments provide causal evidence that edge identity is irrelevant when degree distribution is preserved. The K562 system severely limits pain-specific conclusions (59.1% of measurable pain genes below expression threshold; only 26.7% of RA-PainKG genes present in the dataset); replication in sensory neuron models is essential.",
    "1b: Abstract Discussion repositioned"
)

# 1c. Abstract Conclusion
replace(
    "**Conclusion:** Dense KGs outperform domain-specific KGs for perturbation prediction; domain KGs complement by identifying systematic knowledge gaps. We provide an open-source multi-split ablation benchmark framework.",
    "**Conclusion:** We provide an open-source multi-split ablation benchmark framework and demonstrate that single-split KG evaluation generates misleading conclusions. Causal evidence from degree-preserving randomization shows that graph connectivity, not edge semantics, drives linear perturbation prediction. Domain KGs quantify knowledge gaps but require disease-relevant test systems for valid evaluation.",
    "1c: Abstract Conclusion repositioned"
)

# 1d. Keywords
replace(
    "**Keywords:** knowledge graphs; perturbation prediction; GEARS; rheumatoid arthritis; benchmark; ablation study",
    "**Keywords:** knowledge graphs; perturbation prediction; benchmark methodology; ablation study; multi-split validation; rheumatoid arthritis",
    "1d: Keywords updated"
)

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print(f"Abstract done. {sum(1 for c in changes if '[OK]' in c)}/{len(changes)} applied.")