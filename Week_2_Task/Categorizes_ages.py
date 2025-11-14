#Build a program that categorizes ages (child, teen, adult)

ages = []
categories = []

print("Enter ages one by one. Type 'done' when finished.")

# Get ages from user until 'done'
while True:
    user_input = input("Enter age (or 'done'): ")
    if user_input.lower() == "done":
        break
    try:
        age = int(user_input)
        ages.append(age)
    except ValueError:
        print("Invalid input! Please enter a number or 'done'.")

print("\nAge Categorization Results:")
print("-" * 30)
# Categorize each age and display the result clearly
for age in ages:
    if age < 13:
        category = "child"
    elif 13 <= age < 20:
        category = "teen"
    elif age >= 20:
        category = "adult"
    else:
        category = "unknown"
    print(f"Age {age:2d} -> {category}")

print("-" * 30)
