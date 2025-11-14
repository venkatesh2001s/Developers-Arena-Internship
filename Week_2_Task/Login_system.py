#Build a simple login system with username/password

# Predefined list of users: each user is a dictionary with username and password
users = [
    {"username": "admin", "password": "admin123"},
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"}
]

print("Welcome to The Developer's Arena Simple Login System")

# Allow max 3 login attempts
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    # Error handling for empty inputs
    if not username or not password:
        print("Both fields are required. Try again.")
        continue

    # Check username and password against each user in the list using for loop
    login_success = False
    for user in users:
        if username == user["username"] and password == user["password"]:
            login_success = True
            break

    # Conditional statements to provide feedback
    if login_success:
        print("Login successful. Welcome,", username + "!")
        break
    else:
        attempts += 1
        print(f"Login failed. {max_attempts - attempts} attempts remaining.")

if attempts == max_attempts:
    print("Maximum login attempts reached. Access denied.")
