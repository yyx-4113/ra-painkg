filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Update Reference [4] from "In preparation" to actual repository location
old_ref4 = "[4] RA-PainKG: A tissue-specific knowledge graph for rheumatoid arthritis pain signaling. Companion Data Descriptor. [In preparation]."
new_ref4 = "[4] Yang Y. RA-PainKG: A tissue-specific knowledge graph for rheumatoid arthritis pain signaling — construction protocol, network analysis, and coverage-gap documentation. Zenodo/GitHub. 2026. Available at: https://github.com/yyx-4113/ra-painkg."

if old_ref4 in content:
    content = content.replace(old_ref4, new_ref4)
    print("[OK] Reference [4] updated")
else:
    print("[MISS] Reference [4] not found with exact string")

# Also update the Data Availability section to reference supplementary tables
old_data = "Benchmark result tables are provided as Supplementary Tables S1-S5."
new_data = "Benchmark result tables are provided as Supplementary Tables S1-S5 (included in this repository at benchmark/results/supplementary_table_S*.md)."
if old_data in content:
    content = content.replace(old_data, new_data)
    print("[OK] Data Availability updated")

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("Done.")