#Build a Student Grade Calculator that takes marks and returns grade with comments, and stores results in a list
#Project

# List to store student results as dictionaries
results = []

print("Student Grade Calculator")

while True:
    name = input("Enter student name (or type 'done' to finish): ").strip()
    if name.lower() == "done":
        break
    
    try:
        marks = float(input(f"Enter marks for {name} (0-100): "))
        if marks < 0 or marks > 100:
            print("Marks should be between 0 and 100. Try again.")
            continue
    except ValueError:
        print("Invalid input! Please enter numeric marks.")
        continue
    
    # Determine grade and comments based on marks
    if marks >= 90:
        grade = "A+"
        comment = "Excellent work!"
    elif marks >= 80:
        grade = "A"
        comment = "Very good!"
    elif marks >= 70:
        grade = "B"
        comment = "Good effort"
    elif marks >= 60:
        grade = "C"
        comment = "Average performance"
    elif marks >= 50:
        grade = "D"
        comment = "Needs improvement"
    else:
        grade = "F"
        comment = "Fail - work harder"
    
    # Store result in list
    results.append({"name": name, "marks": marks, "grade": grade, "comment": comment})

# Display all results
print("\n---> Student Results <---")
for student in results:
    print(f"Name: {student['name']}, Marks: {student['marks']}, Grade: {student['grade']}, Comment: {student['comment']}")
