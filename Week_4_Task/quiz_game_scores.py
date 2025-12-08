#Create a quiz game that saves scores

def save_score(username, score, filename="scores.txt"):
    """Save the username and score to a text file."""
    try:
        with open(filename, "a") as f:
            f.write(f"{username},{score}\n")
        print("Score saved successfully.")
    except Exception as e:
        print(f"Error saving score: {e}")

def quiz_game():
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["a) Berlin", "b) Paris", "c) Madrid", "d) Rome"],
            "answer": "b"
        },
        {
            "question": "Who wrote 'Romeo and Juliet'?",
            "options": ["a) Charles Dickens", "b) Jane Austen", "c) William Shakespeare", "d) Mark Twain"],
            "answer": "c"
        },
        {
            "question": "What is 5 + 7?",
            "options": ["a) 10", "b) 11", "c) 12", "d) 13"],
            "answer": "c"
        }
    ]
    
    print("Welcome to the Quiz Game!")
    username = input("Enter your name: ")
    score = 0

    for q in questions:
        print("\n" + q["question"])
        for option in q["options"]:
            print(option)
        answer = input("Your answer (a/b/c/d): ").lower()
        if answer == q["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was '{q['answer']}'.")
    
    print(f"\nQuiz completed. {username}, your score is {score} out of {len(questions)}.")
    save_score(username, score)

if __name__ == "__main__":
    quiz_game()
