filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Find all occurrences of "Intel" and context
idx = content.find("Intel")
if idx >= 0:
    snippet = content[idx-30:idx+200]
    print(f"Found 'Intel' at position {idx}")
    print(f"Context: [{snippet}]")
    print(f"repr: {repr(snippet[:100])}")
else:
    print("Intel not found!")

# Find "40" near "seconds"
import re
matches = list(re.finditer(r'40.*?seconds.*?Intel', content))
for m in matches:
    s = m.start()
    print(f"\nFound at {s}: [{content[s:s+150]}]")