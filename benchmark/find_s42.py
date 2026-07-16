filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Find exact section 4.2 content
idx = content.find("### 4.2 Clinical Implications")
if idx >= 0:
    # Find the start of the next section
    next_idx = content.find("### 4.3", idx)
    if next_idx < 0:
        next_idx = content.find("### 4.4", idx)
    if next_idx < 0:
        next_idx = idx + 2000
    
    old = content[idx:next_idx]
    print(f"Section 4.2 length: {len(old)} chars")
    print(f"Starts with: {repr(old[:100])}")
    print(f"Ends with: {repr(old[-100:])}")