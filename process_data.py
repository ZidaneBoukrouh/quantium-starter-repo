import pandas as pd
from pathlib import Path

# Folder containing the CSVs
data_dir = Path("data")

# Load all CSV files in data/ into one DataFrame
csv_files = list(data_dir.glob("*.csv"))
dfs = [pd.read_csv(f) for f in csv_files]
df = pd.concat(dfs, ignore_index=True)

# Keep only Pink Morsels
df = df[df["product"] == "pink morsel"]

# Create Sales column
df["Sales"] = df["quantity"] * df["price"]

# Keep only required columns and rename to match spec
output = df[["Sales", "date", "region"]].rename(
    columns={"date": "Date", "region": "Region"}
)

# Save to output file
output_path = data_dir / "processed_sales.csv"
output.to_csv(output_path, index=False)

print(f"Saved processed data to {output_path}")