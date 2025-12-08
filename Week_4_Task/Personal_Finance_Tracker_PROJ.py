# Build a Complete Personal Finance Tracker that allows adding expenses, categorizing them, and saving data to files with monthly reports

import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

def write_expense(date, category, amount, description):
    """
    Append an expense record to the CSV file.
    """
    file_exists = os.path.isfile(FILE_NAME)
    try:
        with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # If file is new, write header
            if not file_exists:
                writer.writerow(["Date", "Category", "Amount", "Description"])
            writer.writerow([date, category, amount, description])
        print("Expense saved successfully.")
    except Exception as e:
        print(f"Error saving expense: {e}")

def read_expenses():
    """
    Load all expenses from the CSV file.
    Returns a list of dictionaries.
    """
    expenses = []
    if not os.path.isfile(FILE_NAME):
        print("No expenses recorded yet.")
        return expenses
    try:
        with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert Amount to float, parse date to datetime
                row["Amount"] = float(row["Amount"])
                row["Date"] = datetime.strptime(row["Date"], "%Y-%m-%d")
                expenses.append(row)
    except Exception as e:
        print(f"Error reading expenses: {e}")
    return expenses

def monthly_report(year, month):
    """
    Generate a report of expenses for a specific month and year.
    Returns sums per category and total spending.
    """
    expenses = read_expenses()
    report = {}
    total = 0
    for exp in expenses:
        if exp["Date"].year == year and exp["Date"].month == month:
            category = exp["Category"]
            report[category] = report.get(category, 0) + exp["Amount"]
            total += exp["Amount"]
    return report, total

def main():
    print("Welcome to Personal Finance Tracker")
    while True:
        print("\nMenu:\n1. Add Expense\n2. Monthly Report\n3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
            if not date_str:
                date_str = datetime.today().strftime("%Y-%m-%d")
            else:
                # Validate date format
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")
                    continue
                
            category = input("Enter category (e.g. Food, Transport): ").strip()
            amount_str = input("Enter amount: ").strip()
            try:
                amount = float(amount_str)
            except ValueError:
                print("Invalid amount.")
                continue
            description = input("Enter a description: ").strip()
            
            write_expense(date_str, category, amount, description)

        elif choice == '2':
            year_str = input("Enter year (e.g., 2025): ").strip()
            month_str = input("Enter month number (1-12): ").strip()
            try:
                year = int(year_str)
                month = int(month_str)
                if month < 1 or month > 12:
                    raise ValueError
            except ValueError:
                print("Invalid year or month.")
                continue
            report, total = monthly_report(year, month)
            if not report:
                print(f"No expenses recorded for {year}-{month:02d}.")
            else:
                print(f"\nExpense report for {year}-{month:02d}:")
                for cat, amt in report.items():
                    print(f"  {cat}: {amt:.2f}")
                print(f"Total: {total:.2f}")

        elif choice == '3':
            print("Exiting Personal Finance Tracker. Goodbye!")
            break
        else:
            print("Invalid choice, please select 1, 2 or 3.")

if __name__ == "__main__":
    main()

