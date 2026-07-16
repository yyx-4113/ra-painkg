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

# Fix Table 3 CI values based on verified data
# 1. Random_R1 vs GO CI
replace(
    "| Random_R1 vs GO | +0.078 | [+0.043, +0.112] | <0.001 | *** | *** |",
    "| Random_R1 vs GO | +0.078 | [+0.059, +0.096] | <0.001 | *** | *** |",
    "Table 3: Random_R1 vs GO CI fixed"
)

# 2. RA-PainKG vs GO CI
replace(
    "| RA-PainKG vs GO | -0.039 | [-0.085, +0.007] | 0.084 | ns | ns |",
    "| RA-PainKG vs GO | -0.039 | [-0.078, +0.000] | 0.084 | ns | ns |",
    "Table 3: RA-PainKG vs GO CI fixed"
)

# 3. GO-painCentric vs GO CI
replace(
    "| GO-painCentric vs GO | -0.019 | [-0.052, +0.014] | 0.22 | ns | ns |",
    "| GO-painCentric vs GO | -0.019 | [-0.047, +0.010] | 0.22 | ns | ns |",
    "Table 3: GO-painCentric vs GO CI fixed"
)

# 4. Random_R1 vs RA-PainKG CI
replace(
    "| Random_R1 vs RA-PainKG | +0.117 | [+0.081, +0.152] | <0.001 | *** | *** |",
    "| Random_R1 vs RA-PainKG | +0.117 | [+0.083, +0.150] | <0.001 | *** | *** |",
    "Table 3: Random_R1 vs RA-PainKG CI fixed"
)

# 5. Discussion section "density ablation": fix delta
replace(
    "GO-painCentric (121,543 edges, 18% of GO edges) achieves performance statistically indistinguishable from full GO (delta = -0.019, p = 0.22)",
    "GO-painCentric (121,543 edges, 18% of GO edges) achieves performance statistically indistinguishable from full GO (delta = -0.019, p = 0.22 for pain-genes; delta = +0.014, p = 0.17 for all-genes)",
    "Discussion: GO-painCentric values clarified"
)

# 6. Fix Abstract to use verified CI
replace(
    "delta = +0.078, 95% CI [+0.059, +0.096], p < 0.001) and RA-PainKG",
    "delta = +0.078, 95% CI [+0.059, +0.096], p < 0.001) and RA-PainKG",
    "Abstract Random_R1 vs GO CI — already correct"
)

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

ok = sum(1 for c in changes if "[OK]" in c)
print(f"\nDone. {ok}/{len(changes)} applied.")