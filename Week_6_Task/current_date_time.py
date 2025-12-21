# Create a program that displays current date and time

from datetime import datetime

# Get current date and time
now = datetime.now()

# Format date and time as string
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

print("Current Date and Time:", current_time)
