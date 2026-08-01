import pandas as pd

df = pd.read_parquet("data/raw/green_tripdata_2026-04.parquet")

print(df.columns.tolist())
print(df.head())