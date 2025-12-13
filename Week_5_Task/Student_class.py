# Create a Student class with attributes and methods

class Student:
    def __init__(self, student_id, name, age, grade):
        # Attributes (instance variables)
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade  # e.g. "A", "B", etc.
        self.marks = []     # list to store marks for subjects

    # Method to add a mark
    def add_mark(self, subject, score):
        self.marks.append({"subject": subject, "score": score})

    # Method to calculate average score
    def get_average(self):
        if not self.marks:
            return 0
        total = sum(m["score"] for m in self.marks)
        return total / len(self.marks)

    # Method to display student details
    def display_info(self):
        print(f"ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Grade: {self.grade}")
        print("Marks:")
        for m in self.marks:
            print(f"  {m['subject']}: {m['score']}")
        print(f"Average Score: {self.get_average():.2f}")


# Example usage
student1 = Student(101, "Alice", 20, "A")
student1.add_mark("Math", 85)
student1.add_mark("Science", 90)
student1.display_info()
