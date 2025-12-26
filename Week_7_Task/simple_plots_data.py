# Create simple plots from data

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")   # e.g., has columns: Date, Sales
plt.plot(df["Date"], df["Sales"], marker="o")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.title("Sales over time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
category_sum = df.groupby("Category")["Sales"].sum().reset_index()
plt.bar(category_sum["Category"], category_sum["Sales"], color="skyblue")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.title("Sales by Category")
plt.show()
plt.hist(df["Sales"], bins=10, edgecolor="black")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.title("Sales distribution")
plt.show()
