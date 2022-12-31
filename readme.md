# Simple Python Library App
# Auth Commands
## Borrower
- sign_in username=testBorrower;password=pass;

  This signs in the borrower
- register username=newUsername;password="password";

  register a new borrower with newUsername as username etc. 
  The user is automatically signed in after registration

## Librarian
- sign_in_librarian username=testLibrarian;password="pass"
  
  the default librarian sign in command

~ Librarian cannot be registered

## Borrower abilities
- borrow title=Book Title;
- return title=Book Title;
- showAllBorrowedBooks;

## Librarian abilities
- add title=Book Title;qty=amountOfAvailableUnits;author=Book Author

## General abilities (i.e., shared librarian and  borrower)
- showAllBooks
- showAllAvailableBooks

## How to run
python main.py
