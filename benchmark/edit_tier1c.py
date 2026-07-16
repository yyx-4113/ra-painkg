filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Fix remaining "collapse KG distinctions" in Conclusion
old = "nonlinear models collapse KG distinctions. Domain KGs serve a complementary"
new = "nonlinear models attenuate KG distinctions. Domain KGs serve a complementary"
if old in content:
    content = content.replace(old, new)
    print("[OK] Conclusion collapse fixed")
else:
    print("[MISS] Conclusion collapse not found")
    # Try finding it
    idx = content.find("collapse KG distinctions")
    if idx >= 0:
        print(f"  Found at position {idx}: ...{content[idx-30:idx+40]}...")

# Fix "clinical recommendations" in Conclusion  
old2 = "clinical recommendations for hybrid KG design."
new2 = "recommendations for hybrid KG design."
if old2 in content:
    content = content.replace(old2, new2)
    print("[OK] clinical -> removed from conclusion")

with open(filepath, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("Done.")