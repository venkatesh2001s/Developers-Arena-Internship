# Build a simple bank account system

# Bank account system using functions and a dictionary

# Account database: keys are account numbers, values are dictionaries with details
accounts = {}

def create_account(acc_no, name, initial_balance=0):
    if acc_no in accounts:
        print("Account already exists.")
        return
    accounts[acc_no] = {
        "name": name,
        "balance": initial_balance
    }
    print(f"Account created for {name} with account number {acc_no}.")

def deposit(acc_no, amount):
    if acc_no not in accounts:
        print("Account not found.")
        return
    accounts[acc_no]["balance"] += amount
    print(f"Deposited {amount}. New balance: {accounts[acc_no]['balance']}")

def withdraw(acc_no, amount):
    if acc_no not in accounts:
        print("Account not found.")
        return
    if accounts[acc_no]["balance"] < amount:
        print("Insufficient balance.")
        return
    accounts[acc_no]["balance"] -= amount
    print(f"Withdrew {amount}. New balance: {accounts[acc_no]['balance']}")

def show_balance(acc_no):
    if acc_no not in accounts:
        print("Account not found.")
        return
    print(f"Account {acc_no} ({accounts[acc_no]['name']}) - Balance: {accounts[acc_no]['balance']}")

# Example usage:
create_account(1001, "Alice", 500)
create_account(1002, "Bob")
deposit(1001, 200)
withdraw(1001, 100)
show_balance(1001)
withdraw(1002, 50)
deposit(1002, 300)
show_balance(1002)
