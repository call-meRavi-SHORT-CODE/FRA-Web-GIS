import pandas as pd
from explanation.explanation_cr import explain_cr_row

# Load CR dataset
df = pd.read_csv("data/FINAL_CR_FormB.csv")

# Pick first row (you can change index)
row = df.iloc[[0]]  # keep as DataFrame

results = explain_cr_row(row)

for r in results:
    print("\nSCHEME:", r["scheme"])
    print("  Probability:", round(r["probability"], 3), "| Eligible:", r["eligible"])
    print("  Reason:", r["reason"])
    print("  Benefit:", r["benefit"])
    print("  Impact:", r["impact"])
    print("  Top features:", r["top_features"])
