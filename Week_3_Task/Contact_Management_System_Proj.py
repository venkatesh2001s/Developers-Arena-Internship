# Create a Contact Management System that stores names and phone numbers, with functions to add, search, and display contacts

# Contact Management System

# Dictionary to store contacts with name as key and phone number as value
contacts = {}

def add_contact(name, phone):
    if name in contacts:
        print(f"{name} already exists with phone number {contacts[name]}.")
        return
    contacts[name] = phone
    print(f"Contact added: {name} -> {phone}")

def search_contact(name):
    phone = contacts.get(name)
    if phone:
        print(f"Found contact: {name} -> {phone}")
    else:
        print(f"Contact '{name}' not found.")

def display_contacts():
    if not contacts:
        print("No contacts to display.")
        return
    print("Contact List:")
    for name, phone in contacts.items():
        print(f"{name}: {phone}")

# Example usage:
add_contact("Alice", "123-456-7890")
add_contact("Bob", "987-654-3210")
search_contact("Alice")
search_contact("Charlie")
display_contacts()
