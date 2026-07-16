filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    paper = f.read()

print("="*60)
print("FINAL ZERO-TOLERANCE SCAN")
print("="*60)

# Should be GONE
gone = [
    "diagnostic value", "diagnostic overlay", "diagnostic function",
    "clinical translation", "clinical decision", "Clinical Implications",
    "research prioritization", "practical decision", "conservative test",
    "decision framework", "Scenario:", "10 variants", "10 KG variants",
    "0.008", "0.80", "0.85", "38.6%", "0.032",
    "[-0.085, +0.007]", "[+0.043, +0.112]", "[+0.081, +0.152]",
    "Intel i7", "[username]", "[To be completed]",
    "collapse KG distinctions",
]

# Should be PRESENT
present = [
    "11 KG variants", "11 variants",
    "0.010", "0.64", "0.65", "59.1%", "0.117",
    "[-0.078, +0.000]", "[+0.059, +0.096]", "[+0.083, +0.150]",
    "i9-13900K", "yyx-4113", "960856791@qq.com", "杨永新",
    "attenuated KG distinctions",
    "methodological contributions",
    "single-split artifact",
    "worked example",
    "sensory neuron",
    "26.7%",
    "Note on extrapolation",
    "benchmark methodology",
    "multi-split validation",
]

issues = []
for w in gone:
    if w in paper:
        issues.append(f"  [RESIDUAL] '{w}'")

for w in present:
    if w not in paper:
        issues.append(f"  [MISSING] '{w}'")

# Extra check: all numerical CIs in Table 3
table_vals = {
    "[+0.083, +0.150]": "Random_R1 vs RA-PainKG r_pain CI",
    "[+0.059, +0.096]": "Random_R1 vs GO r_pain CI (Table says all-genes?)",
    "[-0.047, +0.010]": "GO-painCentric vs GO r_pain CI",
    "[-0.078, +0.000]": "RA-PainKG vs GO CI",
}
for val, desc in table_vals.items():
    if val not in paper:
        issues.append(f"  [TABLE CI MISSING] {desc}: {val}")

# Count sections
for section in ["## 1.", "## 2.", "## 3.", "## 4.", "4.1", "4.2", "4.3", "4.4", "4.5", "4.6"]:
    if section not in paper:
        issues.append(f"  [SECTION MISSING] {section}")

# Refs check
for ref in [f"[{i}]" for i in range(1,14)]:
    if ref not in paper:
        issues.append(f"  [REF MISSING] {ref}")

if not issues:
    print("  [ALL CLEAN] Zero issues found.")
else:
    for i in issues:
        print(i)

print(f"\nFile: {len(paper)} chars, {len(paper.split(chr(10)))} lines")