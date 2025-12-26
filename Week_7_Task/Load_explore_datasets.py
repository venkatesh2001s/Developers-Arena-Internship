# Load and explore different datasets

import pandas as pd

# Load a CSV file
df = pd.read_csv("data.csv")  # put your CSV file name here

# Quick exploration
print(df.head())       # first 5 rows [web:52][web:56]
print(df.info())       # column types and non-null counts [web:55]
print(df.describe())   # numeric summary (mean, min, max, etc.) [web:55]
