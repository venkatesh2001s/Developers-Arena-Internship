

def save_to_file(filename, user_data):
    """
    Saves user data (dictionary) to a file in CSV format.
    Handles errors during file operations.
    """
    try:
        with open(filename, 'a') as f:  # Append mode
            # Write header if file is empty
            if f.tell() == 0:
                f.write("Name,Age,Email\n")
            # Format user data for CSV
            line = f"{user_data['name']},{user_data['age']},{user_data['email']}\n"
            f.write(line)
        print(f"Data for {user_data['name']} saved to {filename}.")
    except Exception as e:
        print(f"Error saving to file: {e}")

def get_user_data():
    """
    Basic debugging: Print statements to verify user inputs.
    """
    name = input("Enter your name: ")
    print(f"DEBUG: Got name = {name}")

    age = input("Enter your age: ")
    print(f"DEBUG: Got age = {age}")

    email = input("Enter your email: ")
    print(f"DEBUG: Got email = {email}")

    return {"name": name, "age": age, "email": email}

if __name__ == "__main__":  # Keeps code organized
    filename = "users.csv"
    # Loop for demonstration (can be removed for single use)
    while True:
        user_data = get_user_data()
        save_to_file(filename, user_data)
        cont = input("Add another user? (y/n): ")
        if cont.lower() != 'y':
            break
