#Practice with different list operations and methods

# Create an initial list
numbers = []

print("Practice List Operations! Type numbers to add, or 'done' to finish.")

# While loop for user input
while True:
    value = input("Enter a number (or 'done'): ")
    if value.lower() == "done":
        break
    try:
        num = int(value)
        numbers.append(num)  # Add to list
    except ValueError:
        print("Invalid input! Please enter a number or 'done'.")

print("\nInitial List:", numbers)

# Practice accessing and modifying data
if len(numbers) > 0:
    print("First item:", numbers[0])
    print("Last item:", numbers[-1])

# Practice removing an item
if len(numbers) > 0:
    remove_value = int(input("Enter a value to remove from the list: "))
    if remove_value in numbers:
        numbers.remove(remove_value)
        print(f"Removed {remove_value}. Updated list:", numbers)
    else:
        print(f"{remove_value} not in the list.")

# Practice inserting, sorting and reversing
numbers.insert(0, 99)
print("After inserting 99 at the beginning:", numbers)

numbers.sort()
print("Sorted list:", numbers)

numbers.reverse()
print("Reversed list:", numbers)

# Practice for loop: print all items
print("\nAll items in the list:")
for item in numbers:
    print(item)

# Practice counting & finding values with conditional statements and comparison operators
search_value = int(input("\nEnter a value to count in list: "))
count = numbers.count(search_value)
if count > 0:
    print(f"{search_value} appears {count} times.")
else:
    print(f"{search_value} does not appear in the list.")
