#Build a simple diary application

# diary_app.py

import os

def write_entry(filename, entry):
    """
    Appends a diary entry with date and time to the file.
    Handles file write errors.
    """
    from datetime import datetime
    try:
        with open(filename, 'a', encoding='utf-8') as f:  # open file in append mode
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp}\n")
            f.write(entry + "\n\n")
        print("Entry saved successfully.")
    except Exception as e:
        print(f"Error saving entry: {e}")

def read_entries(filename):
    """
    Reads and prints all diary entries.
    Handles file read errors and file not found.
    """
    try:
        if not os.path.exists(filename):
            print("No diary entries found.")
            return
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\nYour Diary Entries:\n")
            print(content)
    except Exception as e:
        print(f"Error reading diary: {e}")

def main():
    diary_file = "diary.txt"
    print("Welcome to Simple Diary Application!")
    
    while True:
        print("\nOptions:")
        print("1. Write a new entry")
        print("2. Read diary entries")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            entry = input("Write your diary entry:\n")
            # Basic debugging: print the entry length
            print(f"DEBUG: Entry length = {len(entry)} characters")
            write_entry(diary_file, entry)
        elif choice == '2':
            read_entries(diary_file)
        elif choice == '3':
            print("Exiting diary. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
