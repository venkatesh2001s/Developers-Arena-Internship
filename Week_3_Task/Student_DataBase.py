# Create a student database using dictionaries


# Student database where keys are student IDs and values are dictionaries of student details
student_db = {}

def add_student(student_id, name, age, grades):
    """Add a new student record to the database."""
    if student_id in student_db:
        print(f"Student ID {student_id} already exists.")
        return
    student_db[student_id] = {
        "name": name,
        "age": age,
        "grades": grades  # List of grades
    }
    print(f"Student {name} added successfully.")

def get_student(student_id):
    """Retrieve student details given an ID."""
    student = student_db.get(student_id)
    if student:
        return student
    else:
        print("Student not found.")
        return None

def update_student_grades(student_id, new_grades):
    """Update the grades of an existing student."""
    if student_id in student_db:
        student_db[student_id]["grades"] = new_grades
        print(f"Grades updated for student {student_db[student_id]['name']}.")
    else:
        print("Student not found.")

def delete_student(student_id):
    """Remove a student from the database."""
    if student_id in student_db:
        removed = student_db.pop(student_id)
        print(f"Student {removed['name']} deleted.")
    else:
        print("Student not found.")

def list_all_students():
    """Prints all students in database."""
    if not student_db:
        print("No students in the database.")
        return
    for sid, info in student_db.items():
        print(f"ID: {sid}, Name: {info['name']}, Age: {info['age']}, Grades: {info['grades']}")

# Example usage
add_student(101, "Venky", 20, [85, 90, 78])
add_student(102, "Divya", 22, [88, 76, 92])

list_all_students()

student = get_student(101)
if student:
    print(f"\nDetails for student 101:\nName: {student['name']}\nGrades: {student['grades']}")

update_student_grades(101, [88, 92, 81])
delete_student(102)

list_all_students()
