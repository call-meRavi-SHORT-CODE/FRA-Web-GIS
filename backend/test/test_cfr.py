import pandas as pd
from explanation.explanation_cfr import explain_cfr_row

df = pd.read_csv("data/FINAL_CFR_FormC.csv")
row = df.iloc[[0]]

results = explain_cfr_row(row)

for r in results:
    print("\n-----------------------")
    print("SCHEME:", r["scheme"])
    print("Probability:", round(r["probability"], 3))
    print("Eligible:", r["eligible"])
    print("Reason:", r["reason"])
    print("Benefit:", r["benefit"])
    print("Impact:", r["impact"])
