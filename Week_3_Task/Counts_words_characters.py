# Make a text analyzer that counts words and characters


def text_analyzer(text):
    # Count number of words
    words = text.split()
    word_count = len(words)
    
    # Count number of characters (excluding spaces)
    chars_no_spaces = len(text.replace(" ", ""))
    
    # Count number of characters (including spaces)
    chars_with_spaces = len(text)
    
    return {
        "word_count": word_count,
        "characters_including_spaces": chars_with_spaces,
        "characters_excluding_spaces": chars_no_spaces
    }

# Example usage
user_input = input("Enter text to analyze: ")
result = text_analyzer(user_input)

print(f"Word count: {result['word_count']}")
print(f"Character count (including spaces): {result['characters_including_spaces']}")
print(f"Character count (excluding spaces): {result['characters_excluding_spaces']}")
