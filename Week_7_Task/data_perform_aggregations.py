# Group data and perform aggregations

import pandas as pd

df = pd.read_csv("data.csv")  # your dataset

# Example: group by a category column and get sum of another column
grouped = df.groupby("Category")["Sales"].sum()
print(grouped)

stats = df.groupby("Category")["Sales"].agg(["sum", "mean", "max", "min", "count"])
print(stats)

agg_multi = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Avg_Sales=("Sales", "mean"),
    Max_Quantity=("Quantity", "max"),
)
print(agg_multi)

group_multi = df.groupby(["Region", "Category"])["Sales"].sum()
print(group_multi)

result = df.groupby("Category")["Sales"].sum().reset_index()
print(result)

