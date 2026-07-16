import os
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("submission/supplementary_tables.md", "r", encoding="utf-8") as f:
    suppl = f.read()

# Find insertion point (before the first existing table, or at the beginning after the header)
# Insert Table S6 as the first table (structural characteristics)
s6 = """
# Supplementary Table S6: KG Variant Structural Characteristics

| KG Variant | Edges | Density | Mean Degree | Coverage (%) |
|-----------|-------|---------|-------------|-------------|
| GO-BP | 673,899 | 0.02648 | 267.1 | 100 |
| Random (5 graphs; range) | 673,899 | 0.02648 | 267.1 | 100 |
| GO-painCentric | 121,543 | 0.00478 | 48.2 | 100 |
| RA-PainKG | 2,400 | 0.00009 | 1.0 | 31.7 |
| RA-PainKG-degPreserved | 2,400 | 0.00009 | 1.0 | 31.7 |
| STRING (gene-symbol filtered) | 15,403 | 0.00061 | 6.1 | 100 |
| Identity | 0 | 0 | 0 | 0 |

RA-PainKG is 280-fold sparser than GO (2,400 vs 673,899 edges), with 68.3% of genes having zero edges.

---

"""

# Insert after the initial header
# Find first --- separator after the title
first_sep = suppl.index("---")
insert_pos = suppl.index("\n", suppl.index("\n", first_sep + 3) + 1)
suppl = suppl[:insert_pos] + s6 + suppl[insert_pos:]

with open("submission/supplementary_tables.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(suppl)
print("[OK] Supplementary Table S6 added")