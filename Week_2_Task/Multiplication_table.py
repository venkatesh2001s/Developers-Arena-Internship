#Create a multiplication table generator

print("Welcome to Multiplication Table Generator!")

# Use while loop to repeatedly get user input until valid
while True:
    try:
        num = int(input("Enter the number for which you want the multiplication table (1-20): "))
        if 1 <= num <= 20:
            break
        else:
            print("Please enter a number between 1 and 20.")
    except ValueError:
        print("Invalid input! Please enter a valid integer.")

# Use a list to store the results
table = []

# Generate multiplication table using for loop
for i in range(1, 11):
    product = num * i
    table.append(product)

# Display the multiplication table
print(f"\nMultiplication Table for {num}:")
for i in range(1, 11):
    print(f"{num} x {i} = {table[i-1]}")
