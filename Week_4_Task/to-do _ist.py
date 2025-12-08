#Build a to-do list that persists between runs 

import os

TODO_FILE = "todo_list.txt"

def load_tasks():
    """Load tasks from todo_list.txt file."""
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        tasks = [line.strip() for line in f.readlines()]
    return tasks

def save_tasks(tasks):
    """Save tasks list to todo_list.txt file."""
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(task + "\n")

def show_tasks(tasks):
    if not tasks:
        print("Your to-do list is empty.")
    else:
        print("Your To-Do List:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")

def main():
    tasks = load_tasks()
    print("Welcome to the Persistent To-Do List!")
    while True:
        print("\nOptions:\n1. Show tasks\n2. Add task\n3. Remove task\n4. Exit")
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            new_task = input("Enter the new task: ").strip()
            if new_task:
                tasks.append(new_task)
                save_tasks(tasks)
                print("Task added.")
            else:
                print("Empty task not added.")
        elif choice == "3":
            show_tasks(tasks)
            try:
                task_num = int(input("Enter task number to remove: "))
                if 1 <= task_num <= len(tasks):
                    removed = tasks.pop(task_num - 1)
                    save_tasks(tasks)
                    print(f"Removed task: {removed}")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
