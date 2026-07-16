filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

print("="*60)
print("POST-REPOSITIONING VERIFICATION")
print("="*60)

checks = [
    # Should be GONE
    ("clinical translation", "clinical translation" not in content, "GONE"),
    ("research prioritization", "research prioritization" not in content, "GONE"),
    ("diagnostic overlay", "diagnostic overlay" not in content, "GONE"),
    ("decision framework", "decision framework" not in content, "GONE"),
    ("conservative test", "conservative test" not in content, "GONE"),
    ("practical decision", "practical decision" not in content, "GONE"),
    ("Clinical Implications", "Clinical Implications" not in content, "GONE"),
    ("Scenario:", "Scenario:" not in content, "GONE"),
    ("clinical informatics", "clinical informatics" not in content, "GONE"),
    
    # Should be PRESENT
    ("Methodological Implications", "Methodological Implications" in content, "PRESENT"),
    ("single-split artifact", "single-split artifact" in content, "PRESENT"),
    ("worked example", "worked example" in content, "PRESENT"),
    ("open-source multi-split ablation", "open-source multi-split ablation" in content, "PRESENT"),
    ("causal evidence", "causal evidence" in content, "PRESENT"),
    ("sensory neuron", "sensory neuron" in content, "PRESENT"),
    ("benchmark methodology", "benchmark methodology" in content, "PRESENT"),
    ("methodological contributions", "methodological contributions" in content, "PRESENT"),
    ("59.1%", "59.1%" in content, "PRESENT"),
    ("26.7%", "26.7%" in content, "PRESENT"),
]

pass_count = 0
for name, result, expected in checks:
    status = "PASS" if result else "FAIL"
    if result: pass_count += 1
    print(f"  [{status}] [{expected}] {name}")

print(f"\nTOTAL: {pass_count}/{len(checks)} PASS")
print(f"File size: {len(content)} chars")