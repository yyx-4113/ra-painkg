import os
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("submission/supplementary_tables.md", "r", encoding="utf-8") as f:
    content = f.read()

# Fix STRING edge count: 0 -> 15,403
content = content.replace("| STRING | 0 | 0.000 +/- 0.000 | 0.000 +/- 0.000", "| STRING | 15,403 | 0.000 +/- 0.000 | 0.000 +/- 0.000")

with open("submission/supplementary_tables.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("[OK] STRING edge count fixed in S1")