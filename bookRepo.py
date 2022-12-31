from book import book


class bookRepo:
    def __init__(self):
        self.books = {"In Search Of Lost Time": book(title="In Search Of Lost Time", author="Marcel Proust", qty=1),
                      "Game Of Thrones": book(title="Game Of Thrones", author="George", qty=2),
                      "The end of the beast": book(title="The end of the beast", author="Billy", qty=3)
                      }
        self._borrowedBooks = {
            ("test-borrower", "In Search Of Lost Time"): self.books["In Search Of Lost Time"]}

    def add_book(self, b: book) -> list[2]:
        """
        Used by a librarian to add a book to the database
        :type b: A book instance
        """
        if self.books[b.title]:
            outputString = "This book already exists, to you mean to increase the quantity? If so, please use the in " \
                           "\"title=booktitle;qty=quantityToIncreaseBy command\"\n"
            return [False, outputString]
        else:
            self.books[b.title] = b
            outputString = b.__str__() + " has been added"
            return [True, outputString]

    def borrow_book(self, username: str, title: str) -> list[2]:
        """
        Used by a borrower to take a book
        :param title: The title of the book you want ot borrow
        :param self:
        :param username: Your username
        :return: An array of size two, with the first value indicating the status of the action and
         the next an information string
        """
        try:

            if self.books[title] and self.books[title]._qty <= 0:
                outputString = "We have this book but none are available for borrowing"
                outputStatus = False
            elif not self.books[title]:
                outputString = "This  book doesn't exist"
                outputStatus = False
            else:
                borrowBookResult = self._borrow_book(title=title, username=username)
                if borrowBookResult[0]:
                    self.books[title].qty -= 1
                    outputString = username + f"\"{title}\" has been taken, please return on time"
                    outputStatus = True
                else:
                    outputString = borrowBookResult[1]
                    outputStatus = False
        except KeyError:
            outputString = "book does not exist"
            outputStatus = False
        return [outputStatus, outputString]

    def return_book(self, username: str, title: str) -> list[2]:
        """
        Used by a borrower to take a book
        :param title: The title of the book you want ot borrow
        :param self:
        :param username: Your username
        :return: An array of size two, with the first value indicating the status of the action and
         the next an information string
        """
        if not self.books[title]:
            outputString = "This  book doesn't exist"
            outputStatus = False
        else:
            returnBookResult = self._return_book(title=title, username=username)
            if returnBookResult[0]:
                self.books[title].qty += 1
                outputString = username + f"\"{title}\" has been returned\n"
                outputStatus = True
            else:
                outputString = returnBookResult[1]
                outputStatus = False
        return [outputStatus, outputString]

    def get_all_borrowed_books_by_user(self, username):
        all_borrowed_books = []
        for (user, book_title) in self._borrowedBooks.keys():
            if user == username:
                all_borrowed_books.append(f"{username} borrowed {book_title}")
        return all_borrowed_books

    def get_all_borrowed_books(self):
        all_borrowed_books = []
        for (username, book_title) in self._borrowedBooks.keys():
            all_borrowed_books.append(f"{username} borrowed {book_title}")
        return all_borrowed_books

    def get_all_available_books(self):
        available_books = []
        for book_title in self.books.keys():
            if self.books[book_title].qty > 0:
                available_books.append(self.books[book_title])
            continue
        return available_books

    def get_all_books(self):
        available_books = []
        for book_title in self.books.keys():
            available_books.append(self.books[book_title])
        return available_books

    def _borrow_book(self, title, username) -> list[2]:
        # watch for keyerror, i.e if the user has already borrowed the book then there would be no error
        try:
            x = self._borrowedBooks[(username, title)]
            outputString = "This book has already been borrow by you"
            outputStatus = False
        except KeyError:
            self._borrowedBooks[(username, title)] = self.books[title]
            outputString = "Borrow successful"
            outputStatus = False

        return [outputStatus, outputString]

    def _return_book(self, title, username) -> list[2]:
        if self._borrowedBooks[(username, title)]:
            outputString = "Successfully returned"
            outputStatus = True
            del self._borrowedBooks
        else:
            outputString = "This book was not borrowed in the first place??"
            outputStatus = False

        return [outputStatus, outputString]

    def _get_all_borrowed_books(self):
        all_borrowed_books = ""
        for (username, book_title) in self._borrowedBooks.keys():
            all_borrowed_books += f"{username} borrowed {book_title}\n"

    @property
    def borrowedBooks(self):
        return self._borrowedBooks
