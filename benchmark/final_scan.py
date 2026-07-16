filepath = r"D:\麻醉科共病\ra-painkg\benchmark\methods_paper.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

print("="*60)
print("FINAL SCAN FOR ALL KNOWN ISSUES")
print("="*60)

checks = [
    ("38.6% gone", "38.6%" not in content),
    ("59.1% present", "59.1%" in content),
    ("0.032 gone (was wrong pain mean)", "0.032" not in content),
    ("0.117 present (correct pain mean)", "0.117" in content),
    ("0.008 gone (wrong SD)", "0.008" not in content),
    ("0.010 present (correct SD)", "0.010" in content),
    ("0.80-0.85 gone (wrong Kendall)", "0.80" not in content and "0.85" not in content),
    ("0.64-0.65 present (correct Kendall)", "0.64" in content and "0.65" in content),
    ("CI [-0.085, +0.007] gone", "[-0.085, +0.007]" not in content),
    ("CI [-0.078, +0.000] present", "[-0.078, +0.000]" in content),
    ("[+0.043, +0.112] gone (old CI)", "[+0.043, +0.112]" not in content),
    ("[+0.059, +0.096] present (correct CI)", "[+0.059, +0.096]" in content),
    ("[+0.081, +0.152] gone (old CI)", "[+0.081, +0.152]" not in content),
    ("[+0.083, +0.150] present (correct CI)", "[+0.083, +0.150]" in content),
    ("10 KG variants gone", "10 KG variants" not in content),
    ("11 KG variants present", "11 KG variants" in content),
    ("Intel i7 gone", "Intel i7" not in content),
    ("Intel i9-13900K present", "i9-13900K" in content),
    ("[username] gone", "[username]" not in content),
    ("[To be completed] gone", "[To be completed]" not in content),
    ("GitHub yyx-4113 URL present", "yyx-4113" in content),
    ("Author Yang Yongxin present", "杨永新" in content),
    ("Email present", "960856791@qq.com" in content),
    ("collapse KG distinctions gone", "collapse KG distinctions" not in content),
    ("attenuated KG distinctions present", "attenuated KG distinctions" in content),
    ("44 pain genes overlap noted", "44 pain genes" in content),
    ("37.5% reference present", "37.5%" in content),
    ("60,000 caveat present", "only two" in content),
    ("RA prevalence 0.24% present", "0.24%" in content),
    ("scGPT reference present", "scGPT" in content),
    ("Reference [11]-[13] present", "[11]" in content and "[13]" in content),
    ("Author Contributions complete", "Yongxin Yang:" in content and "Conceptualization" in content),
    ("Supplementary Tables reference", "supplementary_table_S" in content),
]

pass_count = 0
fail_count = 0
for name, result in checks:
    status = "PASS" if result else "FAIL"
    if result: pass_count += 1
    else: fail_count += 1
    print(f"  [{status}] {name}")

print(f"\nTOTAL: {pass_count} PASS, {fail_count} FAIL")
print(f"File size: {len(content)} chars")