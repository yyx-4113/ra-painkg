filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Find the line containing "Intel i7"
lines = content.split("\n")
for i, line in enumerate(lines):
    if "Intel i7" in line:
        print(f"Line {i+1}: {repr(line[:100])}")
        # Replace this specific line
        old_line = line
        new_line = line.replace("Intel i7, 32 GB RAM", "Intel i9-13900K, 64 GB RAM").replace("10 KGs", "11 KGs") 
        content = content.replace(old_line, new_line)
        print(f"  -> {repr(new_line[:100])}")
        print("  [OK] Line fixed")
        break

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("Done.")