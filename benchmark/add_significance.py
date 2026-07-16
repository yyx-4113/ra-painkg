import os
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    content = f.read()

# JBI Significance Statement (149 words, 4-part structure)
significance = """

**Significance Statement**

*Problem:* Knowledge graph (KG) evaluation in gene perturbation prediction relies predominantly on single train/test splits, with no established methodology for separating the effects of graph density from domain-specific edge semantics.

*What is Known:* General-purpose KGs such as Gene Ontology improve perturbation prediction, but whether domain-specific KGs confer additional advantages remains unresolved.

*What this Paper Adds:* We provide causal evidence, via a multi-split ablation benchmark of 11 KG variants, that graph connectivity—not edge identity—drives linear perturbation prediction. We document a single-split artifact where a domain KG appeared superior but the effect reversed under multi-split averaging, demonstrating that prevailing evaluation practices produce misleading conclusions. The open-source framework includes paired statistics, Kendall's W ranking consistency, and sensitivity analyses.

*Who Benefits:* Biomedical informaticians integrating prior knowledge into machine learning pipelines, KG curators evaluating domain-specific resources, and perturbation prediction method developers seeking rigorous benchmarking standards.

"""

# Insert before "## 2. Materials and Methods" (right after Introduction)
old = "\n---\n\n## 2. Materials and Methods"
new = significance + "\n---\n\n## 2. Materials and Methods"

if old in content:
    content = content.replace(old, new)
    print("[OK] Significance Statement inserted at end of Introduction")
else:
    print("[WARN] Pattern not found")

# Save
with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

# Word count verification
wc = len(significance.split())
print(f"Significance Statement word count: {wc} (must be <= 150)")