filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old = "RA-PainKG is a tissue-specific KG integrating PrimeKG, GTEx v8, and literature-curated pain signaling pathways [4]. It contains 18,069 nodes and 127,226 edges, with 165 unique pain genes organized into a dual-track framework: Track A (immune-inflammation, 106 genes), Track B (nociception-pain transduction, 122 genes), with 96 genes spanning both tracks."

new = """RA-PainKG is a tissue-specific KG constructed in three stages [4]: (1) 192 core pain genes were manually curated from nine literature-defined pain signaling pathways (opioid, TRP channel, sodium channel, neurotrophin, MAPK, JAK-STAT, NF-kappaB, Src kinase, complement cascades); (2) 120 of 192 seed genes matched PrimeKG v1.0 by exact symbol, and 2-hop neighborhood expansion identified 45 additional pain-relevant genes, yielding 165 annotated genes; (3) all PrimeKG edges involving these genes were retained, producing 18,069 nodes (10 entity types) and 127,226 directed edges (24 relation types), of which 2,400 are PPI edges and 124,826 are non-PPI (pathway, bioprocess, drug-target, disease-association). GTEx v8 tissue expression data provided tissue-context filtering. The 165 genes are organized into a dual-track framework: Track A (immune-inflammation, 106 genes), Track B (nociception-pain transduction, 122 genes), with 96 genes spanning both tracks. Hub nodes include EGR1, FOS, STAT3, JUN, and AKT1. A coverage-gap analysis identified 72 core pain genes (37.5%) absent from PrimeKG, primarily in complement cascade and GABA receptor families."""

if old in content:
    content = content.replace(old, new)
    print("[OK] RA-PainKG construction summary added to Introduction")
else:
    print("[MISS] RA-PainKG description not found")

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("Done.")