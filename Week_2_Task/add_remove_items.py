# Make a shopping list manager with add/remove items

shopping_list = []

print("Welcome to Shopping List Manager!")
print("You can add items, remove items, or view your list.")
print("Type 'add', 'remove', 'view', or 'exit'.")

while True:
    action = input("\nEnter action (add/remove/view/exit): ").lower()

    if action == "add":
        item = input("Enter item to add: ").strip()
        if item:
            shopping_list.append(item)
            print(f"'{item}' has been added to your list.")
        else:
            print("Please enter a valid item.")

    elif action == "remove":
        if not shopping_list:
            print("Your shopping list is empty.")
            continue
        
        item = input("Enter item to remove: ").strip()
        # Using error handling for item removal
        try:
            shopping_list.remove(item)
            print(f"'{item}' has been removed from your list.")
        except ValueError:
            print(f"'{item}' is not in your shopping list.")

    elif action == "view":
        if shopping_list:
            print("Your shopping list contains:")
            for index, item in enumerate(shopping_list, start=1):
                print(f"{index}. {item}")
        else:
            print("Your shopping list is empty.")

    elif action == "exit":
        print("Exiting Shopping List Manager. Goodbye!")
        break

    else:
        print("Invalid action! Please choose add, remove, view, or exit.")
