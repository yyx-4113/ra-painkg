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

# 1. Fix "10 variants" in STRING exclusion
replace(
    "The 10 variants tested span the full density-accuracy-design space.",
    "The 11 variants tested span the full density-accuracy-design space.",
    "#1: 10->11 in STRING exclusion"
)

# 2. Fix k range in Methods 2.3
replace(
    "k = 32, 64, 128, 256).",
    "k = 32, 64, 128, 256, 512).",
    "#2: k=512 added to Methods"
)

# 3. Verify 60,000 context
count = content.count("60,000")
print(f"'60,000' count: {count}")
for i, line in enumerate(content.split('\n')):
    if "60,000" in line:
        print(f"  L{i+1}: ...{line.strip()[:120]}...")

for c in changes:
    print(c)

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

ok = sum(1 for c in changes if "[OK]" in c)
print(f"\nDone. {ok}/{len(changes)} applied.")