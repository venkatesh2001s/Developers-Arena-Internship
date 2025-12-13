# Practice creating multiple objects from same class

class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age

    def display_info(self):
        print(f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}")

# Creating multiple Student objects
student1 = Student(101, "Venky", 20)
student2 = Student(102, "Divya", 22)
student3 = Student(103, "Kumari", 19)

# Calling method on each object to display info
student1.display_info()
student2.display_info()
student3.display_info()
