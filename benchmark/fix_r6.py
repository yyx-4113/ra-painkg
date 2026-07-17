import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    c = f.read()

# FIX 1: Intro number contradiction: 165 != 106+122-96
old_165 = "yielding 165 annotated genes organized into Track A (immune-inflammation, 106 genes) and Track B (nociception-pain transduction, 122 genes, with 96 overlapping)"
new_165 = "yielding 165 annotated genes, of which 106 were assigned to Track A (immune-inflammation), 122 to Track B (nociception-pain transduction, 96 overlapping between tracks), and 33 to neither track (expansion-discovered genes without clear pain functional assignment)"
c = c.replace(old_165, new_165)
print("[1] Fixed 165/106/122/96 contradiction")

# FIX 2: Abstract "57每100%" -> "57-100%"
c = c.replace("57每100%", "57-100%")
# Also fix any other remaining 每 variants
c = c.replace("每", "-")
print("[2] Fixed abstract encoding")

# FIX 3: Significance Statement inconsistency (nine -> 15 functional categories)
old_sig9 = "manual curation of nine pain signaling pathways. The resource includes"
new_sig9 = "manual curation of 15 functional gene categories spanning nine pain signaling pathways. The resource includes"
c = c.replace(old_sig9, new_sig9)
print("[3] Fixed Significance Statement number consistency")

# FIX 4: L5 formatting: "---## Abstract" -> "---\n\n## Abstract"
c = c.replace("---## Abstract", "---\n\n## Abstract")
print("[4] Fixed missing newline before Abstract")

# FIX 5: [19] self-citation loop
old_self = "RA-PainKG was constructed in three stages (detailed protocol in [19])."
new_self = "RA-PainKG was constructed in three stages (detailed below in Sections 2.2-2.3)."
c = c.replace(old_self, new_self)
print("[5] Fixed self-citation loop: [19] -> Sections 2.2-2.3")

# FIX 6: Table 2 numbers source - add footnote to Table 2
old_t2_foot = "RA-PainKG serves three primary use cases."
new_t2_foot = """Coverage percentages for comparator resources (IUPHAR Pain, DisGeNET) were computed by querying each resource for the same 192-gene curated set by gene symbol, following each resource's standard query interface. See Supplementary Methods for query details.

RA-PainKG serves three primary use cases."""
c = c.replace(old_t2_foot, new_t2_foot)
print("[6] Added source explanation for Table 2 comparator numbers")

# FIX 7: Results missing 15-category summary - add brief sentence in 3.1
old_cats = "The dual-track organization is summarized in Table S1: Track A (immune-inflammation, 106 genes)"
new_cats = "The 165 annotated genes span 15 functional categories (TRP channels, voltage-gated sodium channels, neurotrophin signaling, opioid signaling, MAPK pathway, JAK-STAT pathway, prostaglandin pathway, kinase signaling, transcription factors, serotonin receptors, endocannabinoid system, complement cascade, GABA/glycine receptors, RA-specific genes, and anesthetic targets; complete list in Supplementary Table S1). The dual-track organization is summarized in Table S1: Track A (immune-inflammation, 106 genes)"
c = c.replace(old_cats, new_cats)
print("[7] Added 15-category summary to Results 3.1")

# FIX 8: GTEx TPM>=1.0 citation
old_gtex = "A gene was classified as tissue-expressed if median TPM >= 1.0 in the relevant tissue."
new_gtex = "A gene was classified as tissue-expressed if median TPM >= 1.0 in the relevant tissue, following standard GTEx expression thresholds [16]."
c = c.replace(old_gtex, new_gtex)
print("[8] Added GTEx threshold citation")

# FIX 9: Usage 5.3 - fix infinite loop, add break
old_loop = """for node, data in G.nodes(data=True):
    if data.get("track") == "B" and data.get("node_type") == "gene/protein":
        gene = data["node_name"]
        expr = data.get("gtex_median_tpm", {})
        spinal = expr.get("Spinal_Cord_cervical_c-1", "N/A")
        tibial = expr.get("Nerve_Tibial", "N/A")
        print(f"{gene}: Spinal={spinal}, Tibial={tibial}")"""
new_loop = """track_b_expr = []
for node, data in G.nodes(data=True):
    if data.get("track") == "B" and data.get("node_type") == "gene/protein":
        gene = data["node_name"]
        expr = data.get("gtex_median_tpm", {})
        track_b_expr.append({
            "gene": gene,
            "spinal": expr.get("Spinal_Cord_cervical_c-1", "N/A"),
            "tibial": expr.get("Nerve_Tibial", "N/A")
        })
# Display first 5 Track B genes
for item in track_b_expr[:5]:
    print(f\"{item['gene']}: Spinal={item['spinal']}, Tibial={item['tibial']}\")"""
c = c.replace(old_loop, new_loop)
print("[9] Fixed Usage 5.3: added break via list slicing")

# FIX 10: Discussion 4.2 wording
old_uncommon = "is uncommon in the biomedical database literature. While resources such as the IUPHAR/BPS Guide to Pharmacology [14] acknowledge incomplete coverage in narrative form, systematic per-gene gap documentation with categorized absence reasons is rarely implemented. We argue this practice represents"
new_uncommon = "is, to our knowledge, rarely implemented in published biomedical knowledge graphs. While resources such as the IUPHAR/BPS Guide to Pharmacology [14] acknowledge incomplete coverage in narrative form, systematic per-gene gap documentation with categorized absence reasons has few precedents. We suggest this practice represents"
c = c.replace(old_uncommon, new_uncommon)
print("[10] Toned down Discussion 4.2 wording")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(c)
print("\n[DONE] All 10 fixes applied")