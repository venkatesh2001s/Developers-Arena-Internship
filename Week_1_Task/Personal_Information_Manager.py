#Build a Personal Information Manager that stores and displays your name, age, city, and hobbies with formatted output

# Get user input for personal information
name = input("Enter your name: ")
age = int(input("Enter your age: "))  # Convert input string to integer
city = input("Enter your city: ")
hobbies = input("Enter your hobbies (separated by commas): ")

# Creating formatted output using string concatenation and f-strings
print("\n--- Personal Information ---")
print(f"Name   : {name}")
print(f"Age    : {age}")
print(f"City   : {city}")
print(f"Hobbies   : {hobbies}")


