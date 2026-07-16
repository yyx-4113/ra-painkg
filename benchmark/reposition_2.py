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

# 2a. Introduction: Remove "clinical question" paragraph
old_clin = "For disease-focused applications\u2014such as identifying analgesic targets in rheumatoid arthritis (RA), where inflammatory pain affects approximately 0.5\u20131.0% of adults in Western populations (global age-standardized prevalence: 0.24%, 95% UI 0.23\u20130.25%) [3]\u2014a domain-specific knowledge graph might provide more relevant prior information. The clinical question is straightforward: given a list of candidate drug targets for RA pain, should a researcher prioritize them using GO (a dense, general-purpose graph) or RA-PainKG (a sparse, disease-specific graph)?"
new_clin = "RA serves as a motivating example: despite effective anti-inflammatory therapies, a substantial proportion of patients continue to experience clinically significant pain, suggesting that analgesic targets may be distinct from inflammatory targets and that domain-specific prior knowledge could, in principle, aid their identification [3]. However, whether computational benchmarks can reliably detect such advantages\u2014or whether standard evaluation practices produce artifacts that obscure real differences\u2014remains an open methodological question that motivates our controlled ablation design."
if old_clin in content:
    content = content.replace(old_clin, new_clin)
    changes.append("  [OK] 2a: Introduction clinical question removed")
else:
    changes.append("  [MISS] 2a")

# 2b. RA-PainKG description: add explicit overlap caveat
old_ra = "RA-PainKG is a tissue-specific KG constructed in three stages [4]: (1) 192 core pain genes were manually curated from nine literature-defined pain signaling pathways (opioid, TRP channel, sodium channel, neurotrophin, MAPK, JAK-STAT, NF-kappaB, Src kinase, complement cascades); (2) 120 of 192 seed genes matched PrimeKG v1.0 by exact symbol, and 2-hop neighborhood expansion identified 45 additional pain-relevant genes, yielding 165 annotated genes; (3) all PrimeKG edges involving these genes were retained, producing 18,069 nodes (10 entity types) and 127,226 directed edges (24 relation types), of which 2,400 are PPI edges and 124,826 are non-PPI (pathway, bioprocess, drug-target, disease-association). GTEx v8 tissue expression data provided tissue-context filtering. The 165 genes are organized into a dual-track framework: Track A (immune-inflammation, 106 genes), Track B (nociception-pain transduction, 122 genes), with 96 genes spanning both tracks. Hub nodes include EGR1, FOS, STAT3, JUN, and AKT1. A coverage-gap analysis identified 72 core pain genes (37.5%) absent from PrimeKG, primarily in complement cascade and GABA receptor families."
new_ra = "We selected RA-PainKG as a worked example of a domain-specific KG [4]. It was constructed in three stages: (1) 192 core pain genes were manually curated from nine literature-defined pain signaling pathways; (2) 120 matched PrimeKG v1.0 by exact symbol and 2-hop expansion identified 45 additional genes, yielding 165 annotated genes organized into Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes, 96 overlapping); (3) all PrimeKG edges involving these genes were retained, producing 18,069 nodes and 127,226 edges (2,400 PPI, 124,826 non-PPI). A coverage-gap analysis identified 72 core pain genes (37.5%) absent from PrimeKG. Critically, only 44 of the 165 pain genes (26.7%) overlap with the Norman K562 Perturb-seq gene vocabulary, constraining the pain-specific conclusions that can be drawn from this benchmark."
if old_ra in content:
    content = content.replace(old_ra, new_ra)
    changes.append("  [OK] 2b: RA-PainKG with overlap caveat")
else:
    changes.append("  [MISS] 2b")

# 3. Methods 2.5: Remove "conservative test"
old_m25 = "We frame low expression as a conservative test: if density effects dominate in a cell type with minimal pain gene expression, the observed performance gap between dense and sparse KGs represents a lower bound on the true gap in disease-relevant cell types."
new_m25 = "Given that 59.1% of measurable pain genes fall below the expression threshold and mean pain-gene expression (0.117) is comparable to the genome-wide mean (0.107), we treat the pain-gene subset results as exploratory and interpret density-driven conclusions primarily through the non-pain gene subset (n = 5,001), where the benchmark is adequately powered."
if old_m25 in content:
    content = content.replace(old_m25, new_m25)
    changes.append("  [OK] 3: Methods 2.5 'conservative test' removed")
else:
    changes.append("  [MISS] 3: Methods 2.5")

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print(f"\nDone. {sum(1 for c in changes if '[OK]' in c)}/{len(changes)} applied.")