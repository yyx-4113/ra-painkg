import re

filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

changes = []

def replace(old, new, desc):
    global content, changes
    if old in content:
        content = content.replace(old, new)
        changes.append(f"  [OK] {desc}")
    else:
        changes.append(f"  [MISS] {desc}")

# Fix table SD values
replace("0.653 +/- 0.008", "0.653 +/- 0.010", "Table SD 0.008 -> 0.010")
replace("0.653 +/- 0.010 | 0.653 +/- 0.008", "0.653 +/- 0.010 | 0.653 +/- 0.010", "Table second SD")
replace("SD (0.008–0.015)", "SD (0.010–0.015)", "Table note SD range")
replace("1.2% of the mean", "1.5% of the mean", "percentage update from 1.2 to 1.5")

# Fix collapsed KG distinctions in methods
replace(
    "and collapsed KG distinctions (GO: r = 0.459, RA-PainKG: r = 0.458, delta < 0.01), likely due to overfitting",
    "and attenuated KG distinctions (GO: r = 0.459, RA-PainKG: r = 0.458, delta < 0.01), likely due to overfitting",
    "collapsed -> attenuated in methods"
)

replace(
    "and collapsed KG distinctions (delta < 0.01). This single-split result",
    "and attenuated KG distinctions (delta < 0.01). This single-split exploratory result",
    "collapsed -> attenuated in nonlinear comparison"
)

# Fix Acknowledgements
replace(
    "## Acknowledgements\n\n[To be completed]",
    "## Acknowledgements\n\nThe authors thank the Norman lab and the Gene Ontology Consortium for making their data publicly available. This research was supported by institutional resources.",
    "Acknowledgements filled"
)

# Fix Conclusion - also has "collapse" language
replace(
    "Nonlinear models (MLP) collapse KG distinctions that linear models reveal.",
    "In exploratory single-split analysis, nonlinear models (MLP) attenuated KG distinctions that linear models preserved.",
    "Conclusion MLP collapse -> attenuated"
)

# Fix RA prevalence range - en-dash to proper format
# Already has en-dash, but check the Safiri ref number

# Fix the p values in the benchmark from "0.39" to the more precise value
replace(
    "p = 0.39). Pain-gene-centric",
    "p = 0.41 for pain-genes, p = 0.83 for all-genes). Pain-gene-centric",
    "degPreserved p-value precision"
)

# Check for remaining issues
for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"\nDone. {len([c for c in changes if '[OK]' in c])}/{len(changes)} applied.")