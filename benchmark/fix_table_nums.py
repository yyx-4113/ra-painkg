import os, re
os.chdir(r"D:\麻醉科共病\ra-painkg")
with open("benchmark/methods_paper.md", "r", encoding="utf-8") as f:
    content = f.read()

# Fix double "Table 2" -> first one should be Table 1
# Find the first occurrence of "**Table 2." and change it to "**Table 1."
first_t2 = content.index("**Table 2.")
content = content[:first_t2] + "**Table 1." + content[first_t2 + len("**Table 2."):]

# Now fix all remaining references: "Table 2" in Results text should refer to the paired comparison table
# But "Table 1" references should refer to the benchmark results table
# Let me check what references exist

print("Table references found:")
for m in re.finditer(r'\*\*Table [12]\b', content):
    start = max(0, m.start()-10)
    end = min(len(content), m.end()+50)
    print(f"  ...{content[start:end].strip()}...")

# Find all "Table 1" and "Table 2" mentions in text (not headers)
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'Table 1' in line or 'Table 2' in line:
        print(f"  L{i+1}: {line.strip()[:120]}")

with open("benchmark/methods_paper.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("\n[OK] Fixed")