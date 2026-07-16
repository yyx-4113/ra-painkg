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

# Fix compute section
replace(
    'Spectral decomposition of each 5,045 \u00d7 5,045 adjacency matrix required 40\u201366 seconds (Intel i7, 32 GB RAM, single core). Data loading (40 seconds), KG construction (GO: 100 seconds; RA-PainKG: 12 seconds), and benchmark execution (10 splits \u00d7 10 KGs, <1 second per split-KG combination) brought the total wall-clock time to approximately 12 minutes. Peak memory usage was approximately 2.5 GB during simultaneous matrix operations.',
    'Spectral decomposition of each 5,045 \u00d7 5,045 adjacency matrix required 40\u201366 seconds (Intel i9-13900K, 64 GB RAM, single core). Data loading (40 seconds), KG construction (GO: 100 seconds; RA-PainKG: 12 seconds), and benchmark execution (10 splits \u00d7 11 KGs, <1 second per split-KG combination) brought the total wall-clock time to approximately 12 minutes. Peak memory usage was approximately 2.5 GB during simultaneous matrix operations.',
    "Compute spec: i7->i9-13900K, 10->11 KGs"
)

# Check for Table 3 GO vs RA-PainKG
if "GO vs RA-PainKG" in content:
    # Find the exact line
    for line in content.split("\n"):
        if "GO vs RA-PainKG" in line and "|" in line:
            print(f"  Table row: {line}")
            break

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

for c in changes:
    print(c)