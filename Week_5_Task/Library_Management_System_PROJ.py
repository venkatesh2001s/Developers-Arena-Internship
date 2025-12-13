# 🎯 Project: Library Management System with OOP

import json
from datetime import datetime, timedelta

# ------------ Book class (from your sample, slightly adjusted) ------------

class Book:
    """Represents a book in the library"""

    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True
        self.borrowed_by = None
        self.due_date = None
        self.date_added = datetime.now().strftime('%Y-%m-%d')

    def check_out(self, member_id, loan_period=14):
        """Check out the book to a member"""
        if not self.available:
            return False, "Book is already checked out"

        self.available = False
        self.borrowed_by = member_id
        self.due_date = (datetime.now() + timedelta(days=loan_period)).strftime('%Y-%m-%d')
        return True, f"Book checked out successfully. Due date: {self.due_date}"

    def return_book(self):
        """Return the book to the library"""
        if self.available:
            return False, "Book is already available"

        was_overdue = self.is_overdue()
        self.available = True
        self.borrowed_by = None
        self.due_date = None

        if was_overdue:
            return True, "Book returned (was overdue)"
        return True, "Book returned successfully"

    def is_overdue(self):
        """Check if the book is overdue"""
        if self.due_date and not self.available:
            due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
            return datetime.now() > due_date
        return False

    def days_overdue(self):
        """Calculate days overdue"""
        if self.is_overdue():
            due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
            return (datetime.now() - due_date).days
        return 0

    def to_dict(self):
        """Convert book to dictionary for serialization"""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'available': self.available,
            'borrowed_by': self.borrowed_by,
            'due_date': self.due_date,
            'date_added': self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        """Create Book instance from dictionary"""
        book = cls(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            year=data.get('year')
        )
        book.available = data['available']
        book.borrowed_by = data.get('borrowed_by')
        book.due_date = data.get('due_date')
        book.date_added = data.get('date_added', datetime.now().strftime('%Y-%m-%d'))
        return book

    def __str__(self):
        status = "Available" if self.available else f"Borrowed by {self.borrowed_by} (Due: {self.due_date})"
        return f"{self.title} by {self.author} ({self.isbn}) - {status}"


# ------------ Member class ------------

class Member:
    """Represents a library member"""

    MAX_BORROW = 5

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # list of ISBNs

    def can_borrow(self):
        return len(self.borrowed_books) < self.MAX_BORROW

    def borrow_book(self, isbn):
        if not self.can_borrow():
            return False, f"Borrow limit reached ({self.MAX_BORROW} books)."
        if isbn in self.borrowed_books:
            return False, "This book is already borrowed by this member."
        self.borrowed_books.append(isbn)
        return True, "Book added to member's borrowed list."

    def return_book(self, isbn):
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            return True, "Book removed from member's borrowed list."
        return False, "This member did not borrow that book."

    def to_dict(self):
        return {
            'name': self.name,
            'member_id': self.member_id,
            'borrowed_books': self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        m = cls(data['name'], data['member_id'])
        m.borrowed_books = data.get('borrowed_books', [])
        return m

    def __str__(self):
        return f"{self.member_id} - {self.name} (Borrowed: {len(self.borrowed_books)} books)"


# ------------ Library class ------------

class Library:
    """Main library manager"""

    BOOKS_FILE = "books.json"
    MEMBERS_FILE = "members.json"

    def __init__(self):
        self.books = {}   # isbn -> Book
        self.members = {} # member_id -> Member
        self.load_data()

    # ----- Persistence -----

    def load_data(self):
        # Load books
        try:
            with open(self.BOOKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for b in data:
                    book = Book.from_dict(b)
                    self.books[book.isbn] = book
        except FileNotFoundError:
            self.books = {}
        except json.JSONDecodeError:
            self.books = {}

        # Load members
        try:
            with open(self.MEMBERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for m in data:
                    member = Member.from_dict(m)
                    self.members[member.member_id] = member
        except FileNotFoundError:
            self.members = {}
        except json.JSONDecodeError:
            self.members = {}

    def save_data(self):
        # Save books
        books_list = [b.to_dict() for b in self.books.values()]
        with open(self.BOOKS_FILE, "w", encoding="utf-8") as f:
            json.dump(books_list, f, indent=2)

        # Save members
        members_list = [m.to_dict() for m in self.members.values()]
        with open(self.MEMBERS_FILE, "w", encoding="utf-8") as f:
            json.dump(members_list, f, indent=2)

    # ----- Book & member management -----

    def add_book(self):
        title = input("Enter title: ").strip()
        author = input("Enter author: ").strip()
        isbn = input("Enter ISBN: ").strip()
        year_input = input("Enter year (optional): ").strip()
        year = int(year_input) if year_input else None

        if isbn in self.books:
            print("Book with this ISBN already exists.")
            return

        book = Book(title, author, isbn, year)
        self.books[isbn] = book
        print("Book added successfully.")

    def register_member(self):
        name = input("Enter member name: ").strip()
        member_id = input("Enter member ID: ").strip()

        if member_id in self.members:
            print("Member ID already exists.")
            return

        member = Member(name, member_id)
        self.members[member_id] = member
        print("Member registered successfully.")

    def find_book(self, keyword, mode="title"):
        """Search by title, author or isbn"""
        results = []
        keyword_lower = keyword.lower()
        for book in self.books.values():
            if mode == "title" and keyword_lower in book.title.lower():
                results.append(book)
            elif mode == "author" and keyword_lower in book.author.lower():
                results.append(book)
            elif mode == "isbn" and keyword_lower in book.isbn.lower():
                results.append(book)
        return results

    def borrow_book(self):
        member_id = input("Enter member ID: ").strip()
        isbn = input("Enter book ISBN: ").strip()

        if member_id not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return

        member = self.members[member_id]
        book = self.books[isbn]

        if not book.available:
            print("Book is already checked out.")
            return

        if not member.can_borrow():
            print(f"Member has reached the maximum borrow limit ({Member.MAX_BORROW}).")
            return

        ok_member, msg_member = member.borrow_book(isbn)
        if not ok_member:
            print(msg_member)
            return

        ok_book, msg_book = book.check_out(member_id)
        print(msg_book)

    def return_book(self):
        member_id = input("Enter member ID: ").strip()
        isbn = input("Enter book ISBN: ").strip()

        if member_id not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return

        member = self.members[member_id]
        book = self.books[isbn]

        ok_member, msg_member = member.return_book(isbn)
        if not ok_member:
            print(msg_member)
            return

        ok_book, msg_book = book.return_book()
        print(msg_book)
        if book.days_overdue() > 0:
            print(f"Book was overdue by {book.days_overdue()} days.")

    def view_all_books(self):
        if not self.books:
            print("No books in library.")
            return
        for book in self.books.values():
            print(book)

    def view_all_members(self):
        if not self.members:
            print("No members registered.")
            return
        for member in self.members.values():
            print(member)

    def view_overdue_books(self):
        found = False
        for book in self.books.values():
            if book.is_overdue():
                found = True
                print(f"{book} - Overdue by {book.days_overdue()} days")
        if not found:
            print("No overdue books.")

    def stats(self):
        total = len(self.books)
        available = sum(1 for b in self.books.values() if b.available)
        borrowed = total - available
        print(f"Total books: {total}")
        print(f"Available books: {available}")
        print(f"Borrowed books: {borrowed}")

    # ----- Menu -----

    def menu(self):
        print("================================")
        print("      LIBRARY MANAGEMENT SYSTEM ")
        print("================================")
        print(f"Loaded {len(self.books)} books from file")
        print(f"Loaded {len(self.members)} members from file\n")

        while True:
            print("1. Add New Book")
            print("2. Register New Member")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Search Books")
            print("6. View All Books")
            print("7. View All Members")
            print("8. View Overdue Books")
            print("9. View Statistics")
            print("10. Save & Exit")
            print("0. Exit Without Saving")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.register_member()
            elif choice == "3":
                self.borrow_book()
            elif choice == "4":
                self.return_book()
            elif choice == "5":
                self.search_menu()
            elif choice == "6":
                self.view_all_books()
            elif choice == "7":
                self.view_all_members()
            elif choice == "8":
                self.view_overdue_books()
            elif choice == "9":
                self.stats()
            elif choice == "10":
                self.save_data()
                print("Data saved. Goodbye!")
                break
            elif choice == "0":
                print("Goodbye (no save)!")
                break
            else:
                print("Invalid choice, please try again.")

    def search_menu(self):
        print("\nSearch books by:")
        print("1. Title")
        print("2. Author")
        print("3. ISBN")
        print("4. Show all available books")

        option = input("Enter search option: ").strip()

        if option == "1":
            keyword = input("Enter title to search: ")
            results = self.find_book(keyword, mode="title")
        elif option == "2":
            keyword = input("Enter author to search: ")
            results = self.find_book(keyword, mode="author")
        elif option == "3":
            keyword = input("Enter ISBN to search: ")
            results = self.find_book(keyword, mode="isbn")
        elif option == "4":
            results = [b for b in self.books.values() if b.available]
            keyword = "all available books"
        else:
            print("Invalid option.")
            return

        if option != "4":
            print(f"\nSearch Results for '{keyword}':")
        else:
            print("\nAvailable books:")

        print("----------------------------------------")
        if not results:
            print("No books found.")
        else:
            for i, b in enumerate(results, start=1):
                status = "Available" if b.available else f"Borrowed by {b.borrowed_by} (Due: {b.due_date})"
                print(f"{i}. {b.title}")
                print(f"   Author: {b.author}")
                print(f"   ISBN: {b.isbn}")
                if b.year:
                    print(f"   Year: {b.year}")
                print(f"   Status: {status}\n")
            print(f"Found {len(results)} books.\n")


# ------------ Run system ------------

if __name__ == "__main__":
    lib = Library()
    lib.menu()
