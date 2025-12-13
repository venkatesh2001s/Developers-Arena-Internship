# Create a Book class for library management

class Book:
    def __init__(self, title, author, isbn, year, copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.copies = copies  # Number of copies available

    def borrow_book(self):
        if self.copies > 0:
            self.copies -= 1
            print(f"You have borrowed '{self.title}'. Copies left: {self.copies}")
        else:
            print(f"Sorry, '{self.title}' is currently not available.")

    def return_book(self):
        self.copies += 1
        print(f"Thank you for returning '{self.title}'. Copies available now: {self.copies}")

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.isbn}")
        print(f"Year Published: {self.year}")
        print(f"Copies Available: {self.copies}")

# Example usage
book1 = Book("1984", "George Orwell", "9780451524935", 1949, 3)
book1.display_info()
book1.borrow_book()
book1.borrow_book()
book1.return_book()
book1.display_info()
