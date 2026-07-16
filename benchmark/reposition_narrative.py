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

# ================================================================
# 1. ABSTRACT: Reposition from clinical to methodological
# ================================================================

# Objective
replace(
    "**Objective:** To determine whether domain-specific knowledge graphs (KGs) improve gene perturbation prediction over general-purpose KGs, using a rheumatoid arthritis (RA) pain signaling KG (RA-PainKG) as the test case.",
    "**Objective:** To establish rigorous methodology for benchmarking knowledge graph (KG) contributions to gene perturbation prediction, using a rheumatoid arthritis (RA) pain signaling KG as a worked example of domain-specific prior knowledge.",
    "1a: Abstract Objective repositioned"
)

# Discussion paragraph
replace(
    "**Discussion:** Graph density, not domain specificity, drives perturbation prediction accuracy in this setting. Domain KGs serve a diagnostic function by quantifying knowledge gaps (37.5% of core pain genes absent from PPI databases). A preliminary two-point extrapolation suggests approximately 60,000 pain-relevant PPI edges would be needed for domain KG predictive parity. The K562 test system limits pain-specific conclusions; replication in sensory neuron models is needed.",
    "**Discussion:** The dominant methodological finding is that single-split evaluation produces false positives in KG benchmarking: RA-PainKG appeared to outperform GO on pain genes in one split (r = 0.558 vs 0.481) but the effect reversed under multi-split averaging (0.503 vs 0.542). Ablation experiments demonstrate that edge identity is irrelevant when degree distribution is preserved, a causal finding independent of cell type. The K562 system severely limits pain-specific conclusions (59.1% of measurable pain genes below expression threshold); replication in sensory neuron models is essential before drawing domain-KG conclusions.",
    "1b: Abstract Discussion repositioned"
)

# Conclusion
replace(
    "**Conclusion:** Dense KGs outperform domain-specific KGs for perturbation prediction; domain KGs complement by identifying systematic knowledge gaps. We provide an open-source multi-split ablation benchmark framework.",
    "**Conclusion:** We provide an open-source multi-split ablation benchmark framework, demonstrate that single-split KG evaluation generates misleading conclusions, and establish causal evidence (via degree-preserving randomization) that graph connectivity—not edge semantics—drives linear perturbation prediction. Domain KGs quantify knowledge gaps but require disease-relevant test systems for valid evaluation.",
    "1c: Abstract Conclusion repositioned"
)

# Keywords
replace(
    "**Keywords:** knowledge graphs; perturbation prediction; GEARS; rheumatoid arthritis; benchmark; ablation study",
    "**Keywords:** knowledge graphs; perturbation prediction; benchmark methodology; ablation study; multi-split validation; rheumatoid arthritis"
)

# ================================================================
# 2. INTRODUCTION: Remove clinical framing
# ================================================================

# First paragraph - remove "clinical question" narrative
old_intro1 = """For disease-focused applications\u2014such as identifying analgesic targets in rheumatoid arthritis (RA), where inflammatory pain affects approximately 0.5\u20131.0% of adults in Western populations (global age-standardized prevalence: 0.24%, 95% UI 0.23\u20130.25%) [3]\u2014a domain-specific knowledge graph might provide more relevant prior information. The clinical question is straightforward: given a list of candidate drug targets for RA pain, should a researcher prioritize them using GO (a dense, general-purpose graph) or RA-PainKG (a sparse, disease-specific graph)?"""

new_intro1 = """For disease-focused applications\u2014such as rheumatoid arthritis (RA), where inflammatory pain affects approximately 0.5\u20131.0% of adults in Western populations (global age-standardized prevalence: 0.24%, 95% UI 0.23\u20130.25%) [3]\u2014a domain-specific knowledge graph might, in principle, provide more relevant prior information than a general-purpose ontology. The methodological question is whether existing benchmarks can reliably detect such domain-KG advantages, or whether standard evaluation practices produce artifacts that obscure true performance differences."""

if old_intro1 in content:
    content = content.replace(old_intro1, new_intro1)
    changes.append("  [OK] 2a: Introduction clinical question removed")
else:
    changes.append("  [MISS] 2a: Introduction paragraph not found")

# RA-PainKG paragraph - soften the framing
old_ra_desc = """RA-PainKG is a tissue-specific KG constructed in three stages [4]: (1) 192 core pain genes were manually curated from nine literature-defined pain signaling pathways (opioid, TRP channel, sodium channel, neurotrophin, MAPK, JAK-STAT, NF-kappaB, Src kinase, complement cascades); (2) 120 of 192 seed genes matched PrimeKG v1.0 by exact symbol, and 2-hop neighborhood expansion identified 45 additional pain-relevant genes, yielding 165 annotated genes; (3) all PrimeKG edges involving these genes were retained, producing 18,069 nodes (10 entity types) and 127,226 directed edges (24 relation types), of which 2,400 are PPI edges and 124,826 are non-PPI (pathway, bioprocess, drug-target, disease-association). GTEx v8 tissue expression data provided tissue-context filtering. The 165 genes are organized into a dual-track framework: Track A (immune-inflammation, 106 genes), Track B (nociception-pain transduction, 122 genes), with 96 genes spanning both tracks. Hub nodes include EGR1, FOS, STAT3, JUN, and AKT1. A coverage-gap analysis identified 72 core pain genes (37.5%) absent from PrimeKG, primarily in complement cascade and GABA receptor families."""

new_ra_desc = """We selected RA-PainKG as a worked example of a domain-specific KG [4]. It was constructed in three stages: (1) 192 core pain genes were manually curated from nine literature-defined pain signaling pathways; (2) 120 matched PrimeKG v1.0 by exact symbol and 2-hop expansion identified 45 additional genes, yielding 165 annotated genes organized into Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes); (3) all PrimeKG edges involving these genes were retained, producing 18,069 nodes and 127,226 edges (2,400 PPI, 124,826 non-PPI). A coverage-gap analysis identified 72 core pain genes (37.5%) absent from PrimeKG. Importantly, only 44 of the 165 pain genes (26.7%) overlap with the Norman K562 Perturb-seq gene vocabulary, which constrains the pain-specific conclusions that can be drawn from this benchmark."""

if old_ra_desc in content:
    content = content.replace(old_ra_desc, new_ra_desc)
    changes.append("  [OK] 2b: RA-PainKG description with overlap caveat")
else:
    changes.append("  [MISS] 2b: RA-PainKG description")

# ================================================================
# 3. METHODS 2.5: Remove "conservative test" framing
# ================================================================
old_methods25 = """To assess biological relevance of pain gene perturbation effects in K562 cells, we computed per-gene mean expression (log-normalized units) and percentage of expressing cells (non-zero entries) for all 44 pain-annotated genes in the Norman vocabulary. We frame low expression as a conservative test: if density effects dominate in a cell type with minimal pain gene expression, the observed performance gap between dense and sparse KGs represents a lower bound on the true gap in disease-relevant cell types."""

new_methods25 = """To assess biological relevance of pain gene perturbation effects in K562 cells, we computed per-gene mean expression (log-normalized units) for all 44 pain-annotated genes in the Norman vocabulary. Of these, 59.1% (26/44) have mean expression below 0.01, and the mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107), indicating that nociception-specific transcriptional programs are largely inactive in K562 cells. We therefore treat the pain-gene subset results as exploratory and interpret density-driven conclusions primarily through the non-pain gene subset (n = 5,001), where the benchmark is adequately powered."""

if old_methods25 in content:
    content = content.replace(old_methods25, new_methods25)
    changes.append("  [OK] 3: Methods 2.5 rewritten")
else:
    changes.append("  [MISS] 3: Methods 2.5")

# ================================================================
# 4. DISCUSSION: Complete restructuring
# ================================================================

# 4a. Rewrite "Clinical Implications" section → "Methodological Implications"
old_clinical = """### 4.2 Clinical Implications: A Decision Framework

**Scenario:** A researcher uses network propagation to rank candidate drug targets for RA pain. She has access to GO (dense, general) and RA-PainKG (sparse, disease-specific).

**Recommendation:** Use GO for primary target ranking (maximizes coverage and prediction accuracy). Use RA-PainKG as a diagnostic overlay: genes whose GO-based rankings differ substantially from their RA-PainKG-based rankings are candidates for knowledge-gap-driven under-prioritization. Specifically, genes that rank highly in GO but have zero edges in RA-PainKG (68.3% of Norman-measured genes) may be systematically underestimated in network analyses that rely exclusively on domain-specific PPI data.

**Quantitative guidance:** To achieve GO-level predictive performance, RA-PainKG requires approximately 60,000 pain-relevant PPI edges (25-fold increase). This number, derived from log-linear extrapolation between only two data points, provides a provisional target for experimental PPI mapping efforts (e.g., AP-MS, BioID) in sensory neuron models; it should be refined as additional intermediate-density KG data become available."""

new_clinical = """### 4.2 Methodological Implications

Our results carry three implications for KG benchmarking methodology:

**Single-split artifacts are prevalent and consequential.** In our data, RA-PainKG appeared to outperform GO on pain genes under a single split (r = 0.558 vs 0.481, seed 42; a relative swing of +0.116 favoring the domain KG). Multi-split averaging reversed this result (0.503 vs 0.542). This single-split false positive demonstrates that KG benchmarking studies reporting results from a single train/test split risk drawing conclusions that are artifacts of the split rather than properties of the KG. We recommend a minimum of 10 splits with paired statistical tests.

**Ablation design is essential for causal inference.** The observation that Random > GO > RA-PainKG is correlational; the demonstration that degree-preserving randomization leaves performance unchanged (p = 0.41\u20130.83) is causal. Future KG benchmarking efforts should include topology-randomization controls to separate density effects from semantic effects.

**Test system relevance bounds conclusions.** K562 cells express pain genes at levels comparable to the genomic background (mean 0.117 vs 0.107), with 59.1% of measurable pain genes below the expression threshold. Only 26.7% of RA-PainKG pain genes are present in the Norman dataset. Consequently, this benchmark provides strong evidence about density effects in linear models (established on >5,000 non-pain genes across 10 splits) but cannot resolve whether domain-specific KGs would improve prediction in disease-relevant cell types. This question remains open and requires sensory neuron or DRG models."""

if old_clinical in content:
    content = content.replace(old_clinical, new_clinical)
    changes.append("  [OK] 4a: Clinical Implications -> Methodological Implications")
else:
    changes.append("  [MISS] 4a: Clinical Implications section")

# 4b. Remove "Quantitative guidance" if it still exists separately
old_quant = """**Quantitative guidance:** To achieve GO-level predictive performance, RA-PainKG requires approximately 60,000 pain-relevant PPI edges (25-fold increase). This number, derived from log-linear extrapolation between only two data points, provides a provisional target for experimental PPI mapping efforts (e.g., AP-MS, BioID) in sensory neuron models; it should be refined as additional intermediate-density KG data become available."""

new_quant = """**Note on extrapolation:** A preliminary two-point log-linear fit between RA-PainKG (~2,400 PPI edges) and GO-painCentric (~121,500 PPI edges) yields an extrapolated ~60,000-edge target for domain KG predictive parity. This estimate rests on only two data points and should be treated as an order-of-magnitude guide rather than a quantitative prediction; validation requires intermediate-density KG data that do not currently exist."""

if old_quant in content:
    content = content.replace(old_quant, new_quant)
    changes.append("  [OK] 4b: Quantitative guidance softened")
else:
    changes.append("  [MISS] 4b: Quantitative guidance — may already be integrated")

# ================================================================
# 5. CONCLUSION: Rewrite
# ================================================================
old_conclusion = """In a comprehensive multi-split ablation benchmark, we demonstrate that graph density\u2014not domain specificity\u2014drives perturbation prediction performance in linear spectral embedding models. Dense random graphs consistently outperform curated KGs (GO, RA-PainKG) across all gene subsets. Ablation experiments establish causality: randomizing edge identities while preserving degree distribution does not degrade performance. In an exploratory single-split analysis, nonlinear models (MLP) attenuated KG distinctions that linear models reveal; formal multi-split nonlinear validation is needed. We provide a provisional framework: dense KGs for prediction, domain KGs for gap diagnosis, and approximately 60,000 PPI edges as a preliminary target for domain KG development\u2014pending validation in disease-relevant cell types."""

new_conclusion = """This study makes three contributions to KG benchmarking methodology. First, we document a single-split artifact in which a domain-specific KG appeared to outperform a general-purpose KG (RA-PainKG vs GO on pain genes, seed 42) but the effect reversed under multi-split averaging, demonstrating that split-level statistics are essential for reliable KG evaluation. Second, we establish via degree-preserving randomization that graph connectivity, not edge semantics, drives prediction performance in linear spectral embedding models\u2014a causal finding that holds irrespective of cell type or disease context. Third, we provide an open-source multi-split ablation benchmark framework with paired statistical tests, Kendall\u2019s W ranking consistency, and sensitivity analyses. The K562 test system severely limits pain-specific conclusions (59.1% of measurable pain genes below expression threshold; only 26.7% of RA-PainKG genes present), and we identify sensory neuron models as the essential next step for determining whether domain-specific prior knowledge confers advantages in a biologically relevant context."""

if old_conclusion in content:
    content = content.replace(old_conclusion, new_conclusion)
    changes.append("  [OK] 5: Conclusion rewritten")
else:
    changes.append("  [MISS] 5: Conclusion")

# ================================================================
# 6. Sweep: Remove remaining clinical language
# ================================================================

# "research prioritization" -> "benchmark design guidance"
replace(
    "For research prioritization, we propose a hybrid strategy: dense KGs (GO) for primary ranking of perturbation targets, complemented by domain KGs (RA-PainKG) as a secondary filter to flag genes whose ranks may be underestimated due to knowledge gaps. This strategy awaits prospective validation in a disease-relevant cellular context.",
    "For benchmark design, we propose that future KG evaluations include both a dense baseline (e.g., GO) and a domain-specific KG, with multi-split statistics to distinguish density effects from domain-specific effects. The ablation design demonstrated here\u2014degree-preserving randomization and domain-centric reduction\u2014provides a template for isolating causal factors. Validation in disease-relevant cellular models is the essential next step.",
    "6a: research prioritization -> benchmark design"
)

# "actionable knowledge gaps" -> already changed to "systematic" in previous edit
# "clinical informatics" in keywords -> already removed above

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

ok = sum(1 for c in changes if "[OK]" in c)
miss = sum(1 for c in changes if "[MISS]" in c)
print(f"\nDone. {ok} applied, {miss} not found.")
print(f"File size: {len(content)} chars")