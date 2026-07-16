filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

print("="*60)
print("FINAL VERIFICATION CHECKLIST")
print("="*60)

checks = [
    # Tier 1
    ("Kendall W 0.80-0.85 removed", "0.80" not in content and "0.85" not in content),
    ("Kendall W 0.64-0.65 present", "0.64" in content and "0.65" in content),
    ("SD 0.008 removed", "0.008" not in content),
    ("SD 0.010 present", "0.010" in content),
    ("STRING/Identity anomaly explained", "orthogonal to the perturbation response" in content),
    ("60K caveat present", "only two observations" in content),
    ("MLP downgraded (attenuated)", "attenuated KG distinctions" in content),
    ("Author Contributions filled", "[To be completed]" not in content),
    ("GitHub URL fixed", "[username]" not in content),
    ("P-value unadjusted noted", "unadjusted" in content),
    ("Acknowledgements filled", "institutional resources" in content),
    
    # Tier 2
    ("RA-PainKG construction summary", "192 core pain genes were manually curated" in content),
    ("K562 limitations honest", "fundamentally mismatched" in content),
    ("RA prevalence corrected", "0.24%" in content),
    
    # Tier 3
    ("Literature expanded", "scGPT" in content and "Geneformer" in content),
    ("Hardware specified", "Intel i9-13900K" in content),
    ("New references [11]-[13]", "[11]" in content and "[13]" in content),
]

all_pass = True
for name, result in checks:
    status = "PASS" if result else "FAIL"
    if not result:
        all_pass = False
    print(f"  [{status}] {name}")

print(f"\nOverall: {'ALL PASS' if all_pass else 'SOME FAILURES'}")

# Word count for abstract
lines = content.split("\n")
in_abstract = False
abstract_lines = []
for line in lines:
    if line.startswith("## Abstract"):
        in_abstract = True
        continue
    if in_abstract:
        if line.startswith("## "):
            break
        abstract_lines.append(line)
abstract_text = " ".join(abstract_lines)
abstract_words = len(abstract_text.split())
print(f"\nAbstract word count: {abstract_words}")

# Count sections
sections = [l for l in lines if l.startswith("## ")]
print(f"Main sections: {len(sections)}")
for s in sections:
    print(f"  {s}")

print(f"\nTotal file length: {len(content)} chars, ~{len(lines)} lines")