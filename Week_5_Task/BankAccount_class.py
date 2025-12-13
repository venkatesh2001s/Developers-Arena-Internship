# Build a BankAccount class with deposit/withdraw methods

class BankAccount:
    def __init__(self, account_number, owner_name, balance=0.0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient balance.")
            return
        self.balance -= amount
        print(f"Withdrew {amount}. New balance: {self.balance}")

    def display_balance(self):
        print(f"Account: {self.account_number}, Owner: {self.owner_name}, Balance: {self.balance}")


# Example usage
account1 = BankAccount("12345", "Venky", 1000.0)
account1.display_balance()
account1.deposit(500)
account1.withdraw(300)
account1.withdraw(1500)  # should show insufficient balance
account1.display_balance()
