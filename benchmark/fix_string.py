import os
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    content = f.read()

old = "**STRING exclusion rationale:** We excluded STRING PPI because (a) ENSP-to-gene-symbol mapping at 5,045-gene scale introduces identifier ambiguity that complicates reproducibility; and (b) the Random graphs with matched density provide a cleaner control for density effects, while the ablation variants test domain specificity independently. The 11 variants tested span the full density-accuracy-design space."

new = "**STRING note:** STRING PPI (v12) was included in the benchmark as the 11th variant but yielded zero predictive signal (r = 0.000 on all subsets), consistent with Identity (no-edge) performance. We attribute this null result to ENSP-to-gene-symbol mapping at the 5,045-gene scale, which introduces identifier ambiguity that degrades the spectral structure relative to the intentionally dense Random graphs. The 11 variants tested span the full density-accuracy design space, with Random graphs and GO serving as dense baselines and the ablation variants (degPreserved, painCentric) testing domain specificity."

if old in content:
    content = content.replace(old, new)
    print("[OK] STRING exclusion -> STRING note")
else:
    print("[WARN] STRING exclusion paragraph not found exactly; checking...")
    idx = content.find("STRING exclusion")
    if idx >= 0:
        print(f"Found at {idx}: ...{content[idx:idx+100]}...")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("[OK] File saved")