import pandas as pd
from pathlib import Path

data_dir = Path("data")

csv_files = list(data_dir.glob("daily_sales_data_*.csv"))
dfs = [pd.read_csv(file) for file in csv_files]
df = pd.concat(dfs, ignore_index=True)

df = df[df["product"] == "pink morsel"].copy()

df["price"] = df["price"].replace("[$,]", "", regex=True).astype(float)
df["Sales"] = df["quantity"] * df["price"]

output = df[["Sales", "date", "region"]].rename(columns={
    "date": "Date",
    "region": "Region"
})

output.to_csv(data_dir / "processed_sales.csv", index=False)

print("processed_sales.csv created successfully")