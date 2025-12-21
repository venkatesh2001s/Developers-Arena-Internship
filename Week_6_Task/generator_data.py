# Create a program that generates random data

import random
import string

# 1. Random integer between 1 and 100
rand_int = random.randint(1, 100)

# 2. Random float between 0 and 1
rand_float = random.random()

# 3. Random choice from a list
colors = ["red", "green", "blue", "yellow"]
rand_color = random.choice(colors)

# 4. Random list of 5 integers between 10 and 50
rand_list = [random.randint(10, 50) for _ in range(5)]

# 5. Random string of length 8
rand_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

print("Random integer (1-100):", rand_int)
print("Random float (0-1):", rand_float)
print("Random color:", rand_color)
print("Random list of 5 ints:", rand_list)
print("Random string (8 chars):", rand_string)
