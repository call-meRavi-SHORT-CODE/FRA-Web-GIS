import pandas as pd
from explanation.explanation_ifr import explain_ifr_row

df = pd.read_csv("data/FINAL_IFR_FormA.csv")
row = df.iloc[[0]]

results = explain_ifr_row(row)

for r in results:
    print("\nSCHEME:", r["scheme"])
    print("  Probability:", round(r["probability"], 3), "| Eligible:", r["eligible"])
    print("  Reason:", r["reason"])
    print("  Benefit:", r["benefit"])
    print("  Impact:", r["impact"])
    print("  Top features:", r["top_features"])
