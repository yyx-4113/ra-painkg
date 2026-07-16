filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add title page with author info before the abstract
title_block = """# Domain-Specific versus Dense Knowledge Graphs for Gene Perturbation Prediction: A Multi-Split Ablation Benchmark

**Yongxin Yang (杨永新)**<sup>1,*</sup>

<sup>1</sup> Department of Anesthesiology, The Second People's Hospital Affiliated to Fujian University of Traditional Chinese Medicine, Fuzhou 350000, Fujian, China

<sup>*</sup> Corresponding author: 960856791@qq.com

---

"""

# Insert after the "Target: JBI" line
old_header = """## Manuscript (JBI Submission) | Target: *Journal of Biomedical Informatics*

---

## Abstract"""

new_header = """## Manuscript | Target: *Journal of Biomedical Informatics*

---

""" + title_block + """## Abstract"""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("[OK] Title/author block added")
else:
    print("[MISS] Header not found")

# 2. Update Author Contributions
old_contrib = """## Author Contributions

[Author contributions to be finalized prior to submission. Conceptualization, Methodology, Software, Formal Analysis, Writing – Original Draft, Writing – Review & Editing, Supervision.]"""

new_contrib = """## Author Contributions

**Yongxin Yang:** Conceptualization, Methodology, Software, Formal Analysis, Investigation, Data Curation, Writing – Original Draft, Writing – Review & Editing, Visualization, Project Administration."""

if old_contrib in content:
    content = content.replace(old_contrib, new_contrib)
    print("[OK] Author Contributions updated")
else:
    print("[MISS] Author Contributions not found")

# 3. Add ORCID placeholder and update author info in acknowledgements
old_ack = """The authors thank the Norman lab and the Gene Ontology Consortium for making their data publicly available. This research was supported by institutional resources."""

new_ack = """The author thanks the Norman lab and the Gene Ontology Consortium for making their data publicly available. This research was supported by institutional resources from The Second People's Hospital Affiliated to Fujian University of Traditional Chinese Medicine."""

if old_ack in content:
    content = content.replace(old_ack, new_ack)
    print("[OK] Acknowledgements updated for single author")
else:
    print("[MISS] Acknowledgements not found")

# 4. Update Data Availability - correct GitHub URL
old_url = "https://github.com/ra-painkg/ra-painkg"
new_url = "https://github.com/yyx-4113/ra-painkg"
if old_url in content:
    content = content.replace(old_url, new_url)
    print("[OK] GitHub URL updated to yyx-4113 account")
else:
    print("[MISS] GitHub URL not found")

# 5. Fix corresponding author email in Abstract
if "960856791@qq.com" not in content:
    print("[WARN] Email not in abstract - already handled by title block")

# 6. Update Competing Interests for single author
old_competing = "The authors declare no competing interests."
new_competing = "The author declares no competing interests."
if old_competing in content:
    content = content.replace(old_competing, new_competing)
    print("[OK] Competing interests updated")
else:
    print("[MISS] Competing interests")

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("\nDone.")