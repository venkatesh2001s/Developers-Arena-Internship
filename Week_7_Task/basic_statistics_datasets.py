# Calculate basic statistics on datasets

import pandas as pd

df = pd.read_csv("data.csv")  # or pd.read_excel("data.xlsx")
print(df.describe())          # count, mean, std, min, quartiles, max for numeric columns
print(df["column_name"].mean())
print(df["column_name"].median())
print(df["column_name"].min(), df["column_name"].max())
print(df["column_name"].std())
print(df["column_name"].var())
print(df["category_col"].value_counts())        # frequency of each category
print(df["category_col"].value_counts(normalize=True))  # as proportions
print(df.corr(numeric_only=True))  # correlation matrix for numeric columns
print(df.isna().sum())             # check missing
col = df["column_name"].dropna()   # remove NaNs for that column
print(col.mean(), col.median())

