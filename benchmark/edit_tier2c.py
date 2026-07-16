filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Find and replace the table with a properly formatted one
# Let me find the table section
old_table_header = "| Knowledge Graph | Edges | Density |"
new_table_header = "**Table 1. Knowledge graph variants and predictive performance (mean +/- SD across 10 splits).**\n\n| Knowledge Graph | PPI Edges | Density | All-Genes r | Pain-Genes r | Non-Pain r |"

# Actually, let me just verify the table looks ok. Let me instead fix p=0.39 in the KG Variants section
old_p039_var = "matches RA-PainKG performance (p = 0.39), demonstrating"
new_p039_var = "matches RA-PainKG performance (p = 0.41–0.83 across subsets), demonstrating"
if old_p039_var in content:
    content = content.replace(old_p039_var, new_p039_var)
    print("[OK] p=0.39 fixed in KG variants section")
else:
    print("[MISS] p=0.39 in KG variants section")

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("Done.")