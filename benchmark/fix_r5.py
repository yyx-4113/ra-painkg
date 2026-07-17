import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    c = f.read()

# FIX 1+2: Replace Methods 2.5-2.8 with compact version + fix 每 encoding
# Use regex to match from "### 2.5 Gene" to "### 2.8 Implementation" inclusive
pattern = r'### 2\.5 Gene Embedding.*?(?=\n## 3\. Results)'
match = re.search(pattern, c, re.DOTALL)

new_block = """### 2.5 Benchmark Validation Methods

For validation, 128-dimensional gene embeddings were computed via spectral decomposition of the normalized graph Laplacian (k = 128) for each KG [22]. Perturbation effects were predicted via ridge regression (lambda = 0.1) across 10 independent train/test splits (80%/20%). This linear architecture isolates KG contribution from model capacity. Paired t-tests with Bonferroni correction (alpha = 0.01, m = 5) and Kendall's W ranking consistency were used for statistical comparison. Sensitivity analyses for regularization (alpha = 0.001--100.0) and embedding dimension (k = 32--512) confirmed robustness. K562 pain gene expression was quantified per-gene for all 44 pain-annotated genes (mean expression, percent expressing cells). Complete methods, including spectral decomposition details, nonlinear model comparison (MLP vs ridge), GEARS architecture comparison [21], evaluation protocol, and power analysis, are provided in Supplementary Methods.

### 2.6 Implementation

Python 3.10+, ScanPy 1.12, NetworkX 3.6, NumPy, SciPy, scikit-learn. Total compute time: approximately 12 minutes (Intel i9-13900K, 64 GB RAM). Full pipeline and processed data at https://github.com/yyx-4113/ra-painkg.

"""

if match:
    c = c[:match.start()] + new_block + c[match.end():]
    print("[1+2] Methods 2.5-2.8 compressed (38 lines -> 8 lines) + 每 encoding fixed")
else:
    print("[FAIL] Could not find Methods 2.5-2.8 block")

# FIX 3: Remove duplicate "phenotype" 
c = c.replace("anatomy, phenotype, phenotype)", "anatomy, phenotype)")
print("[3] Duplicate phenotype removed")

# FIX 4: Remove double blank line before 4.5
c = c.replace("\n\n\n### 4.5 Updates", "\n\n### 4.5 Updates")
print("[4] Extra blank line removed")

# Also fix any remaining 每 characters using regex
c = re.sub(r'每', '-', c)
print("[Extra] Any remaining 每 -> -")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(c)
print("\n[DONE] All 4 fixes applied")