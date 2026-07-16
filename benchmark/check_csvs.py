import csv

# Read all benchmark CSVs and understand structure
files = [
    "benchmark_jbi_extended.csv",
    "benchmark_alpha_sensitivity.csv", 
    "benchmark_k_sensitivity.csv",
    "benchmark_multisplit.csv",
    "benchmark_stratified.csv",
    "benchmark_real.csv",
    "k562_pain_expr.csv"
]

os.chdir(r"D:\麻醉科共病\ra-painkg\benchmark\results")

for fname in files:
    try:
        with open(fname, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)
        print(f"\n{fname}:")
        print(f"  Columns: {header}")
        print(f"  Rows: {len(rows)}")
        if rows:
            print(f"  First: {rows[0]}")
            print(f"  Last: {rows[-1]}")
    except Exception as e:
        print(f"  ERROR: {e}")