import pandas as pd
import sys


df = pd.read_csv("output.log", index_col=0, sep=r"\s+")
# remove % and convert to float
df["Rate"] = df["Rate"].str.rstrip("%").astype(float)
print(df)
rate_value = df.loc[df["Table"] == 3, "Rate"].iloc[0]
print("Rate from Table 3:", rate_value)

# read comparison value
with open("tests/data/arm5.txt") as f:
    arm5_rate = float(f.read().strip())

print("Rate from arm5.txt:", arm5_rate)

# compare
if rate_value < arm5_rate:
    print("Rates lower than target")
else:
    print("Rates is higher or equal to target")
    sys.exit(1)
