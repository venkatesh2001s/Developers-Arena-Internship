#Create a number guessing game

import random

# --- Variables and data types ---
secret_number = random.randint(1, 10)     # number (int)
attempts = []                              # list to store guesses
is_guessed = False                         # boolean flag
player_name = input("Enter your name: ")   # string

print("Hello, " + player_name + "! Welcome to the Number Guessing Game.")
print("Guess a number between 1 and 10.")

# --- While loop: repeat until guessed ---
while not is_guessed:
    # --- Basic error handling ---
    try:
        guess = int(input("Enter your guess: "))  # input and type conversion
    except ValueError:
        print("Please enter a valid number.")  # string output
        continue
    
    attempts.append(guess)  # --- Lists: modifying collections ---
    
    # --- Conditional statements and comparison operators ---
    if guess == secret_number:
        print("Congratulations, " + player_name + "! You guessed it right.")  # string concatenation
        is_guessed = True   # set boolean flag
    elif guess > secret_number:
        print("Too high! Try again.")
    elif guess < secret_number:
        print("Too low! Try again.")
    else:
        print("Unexpected comparison result.")

# --- Basic operations: arithmetic ---
num_attempts = len(attempts)                # number of attempts (arithmetic)
print("You took " + str(num_attempts) + " attempts.")  # string concatenation

# --- For loop: print all guesses ---
print("Your guesses were:")
for attempt in attempts:                    # for loop with list
    print(attempt)
