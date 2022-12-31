from book import book
import re
import bookRepo
from authenticationHandler import authenticationHandler
from bookRepo import bookRepo
from book import book


class Repl:
    """
    Description:
        repl = Read Evaluate Print Loop.
        Gets you input, evaluates it, returns a response and asks for your input again
    """

    def __init__(self):
        # self._book = book()
        self._authHandler = authenticationHandler()
        self._verb_regex = r"^(?P<verb>\w+)"
        self._fields_regex = r"(?P<field>\w+)=(?P<value>[^;]+);"
        self._user_storage = self._authHandler.user_store
        self._book_storage = bookRepo()
        self._librarian_signed_In = False
        self._borrower_signed_In = False
        self._userName = ""

    # todo
    def run(self):
        """
        star the program
        :return:
        """
        print(r"""
      ______ ______
    _/      Y      \_
   // ~~ ~~ | ~~ ~  \\
  // ~ ~ ~~ | ~~~ ~~ \\      Unilag
 //________.|.________\\     Libary
`----------`-'----------'
        """)
        print(r"Welcome to the Unilag library, "
              "please drop your bags and whatever downstairs, "
              "also don't steal anything, this isn't your hostel.")

        print(r"""Available Commands
        ▆ sign_in username=testBorrower;password=pass;
        ▆ register username=newUsername;password=password;
        ▆ sign_in_librarian username=testLibrarian;password=pass
        ▆ return title=Book Title;
        ▆ borrow title=Book Title;
        ▆ showAllBooks
        ▆ showAllAvailableBooks
        ▆ showAllBorrowedBooks
        ▆ add title=Book Title;qty=amountOfAvailableUnits;author=Book Author
        ▆ logout;""")
        try:
            quit_seen = False
            while not quit_seen:
                self.get_next_cmd()
        except KeyboardInterrupt:
            print("Please use the 'quit' command next time, anyways => goodbye, Mon chérie")

    def prompt(self):
        """
        Outputs the right arrow to mimic an old-school style console, and allows you to input commands inline
        """
        print("> ")

    def get_next_cmd(self):
        self.prompt()
        return self.map_cmd(input())

    def map_cmd(self, usr_input):
        """
        Maps the verb int user input to the appropriate function

        :param usr_input: The user input
        :return: nothing, just performs an action
        """
        if self.parse_line(usr_input):
            if self._verb == "sign_in_librarian":
                if self._librarian_signed_In or self._borrower_signed_In:
                    print("You're already signed in as a user, quit the app and sign in again")
                else:
                    signInResult = self._authHandler.sign_in_librarian(username=self._fields["username"],
                                                                       password=self._fields["password"])

                    if signInResult[0]:
                        self._librarian_signed_In = True
                        self._userName = signInResult[1]
                        print(f"Currently signed in as {self._fields['username']}")
                    else:
                        errorReason = signInResult[3]
                        print(errorReason)
            elif self._verb == "add":
                if self._librarian_signed_In:
                    bookToAdd = book(title=self._fields["title"], author=self._fields["author"],
                                     qty=self._fields["qty"])
                    addBookResult = self._book_storage.add_book(bookToAdd)
                    if addBookResult[0]:
                        self._borrower_signed_In = True
                        self._userName = addBookResult[1]
                    else:
                        errorReason = addBookResult[3]
                        print(errorReason)
                else:
                    print("You are not signed in, to sign in user this\"sign_in_librarian "
                          "username=test-librarian;password=Secret123$;\" to sign in ")


            elif self._verb == "sign_in":
                if self._librarian_signed_In or self._borrower_signed_In:
                    print("You're already signed in as a user, quit the app and sign in again")
                else:
                    signInResult = self._authHandler.sign_in(username=self._fields["username"],
                                                             password=self._fields["password"])
                    if signInResult[0]:
                        self._borrower_signed_In = True
                        self._userName = signInResult[1]
                        print(f"Currently signed in as {self._fields['username']}")
                    else:
                        errorReason = signInResult[3]
                        print(errorReason)
            elif self._verb == "register":
                if self._librarian_signed_In or self._borrower_signed_In:
                    print("You're already signed in as a user, use the 'logout' command  to signout then try again")
                else:
                    registerResult = self._authHandler.register(username=self._fields["username"],
                                                               password=self._fields["password"])
                    if registerResult[0]:
                        self._borrower_signed_In = True
                        self._userName = registerResult[1]
                        print("Registration successful, you can borrow books but first browse the catalog with the "
                              "commands 'showAllBooks', 'showAllMyBorrowedBooks', 'showAllAvailableBooks'")
                    else:
                        errorReason = registerResult[3]
                        print(errorReason)
            elif self._verb == "borrow":
                if self._borrower_signed_In:
                    borrowBookResult = self._book_storage.borrow_book(username=self._userName,
                                                                      title=self._fields["title"])
                    print(borrowBookResult[1])
                else:
                    print(
                        "You are not signed in, to sign in user this\"sign_in "
                        "username=test-borrower;password=Secret123$;")

            elif self._verb == "return":
                if self._borrower_signed_In:
                    returnBookResult = self._book_storage.return_book(username=self._userName,
                                                                      title=self._fields["title"])
                    print(returnBookResult[1])
                else:
                    print(
                        "You are not signed in, to sign in user this\"sign_in "
                        "username=test-borrower;password=Secret123$;")

            elif self._verb == "showAllBooks":
                if self._borrower_signed_In or self._librarian_signed_In:
                    all_books = self._book_storage.get_all_books()
                    for b in all_books:
                        print(b)
                else:
                    print(
                        "You are not signed in, to sign in user this\"sign_in "
                        "username=test-borrower;password=Secret123$;")


            elif self._verb == "showAllAvailableBooks":
                if self._borrower_signed_In or self._librarian_signed_In:
                    all_available_books = self._book_storage.get_all_available_books()
                    for b in all_available_books:
                        print(b)
                else:
                    print(
                        "You are not signed in, to sign in user this\"sign_in "
                        "username=test-borrower;password=Secret123$;")

            elif self._verb == "showAllMyBorrowedBooks":
                if self._borrower_signed_In:
                    all_my_borrowed_books = self._book_storage.get_all_borrowed_books_by_user(username=self._userName)
                    for b in all_my_borrowed_books:
                        print(b)
                else:
                    print(
                        "You are not signed in, to sign in user this\"sign_in "
                        "username=test-borrower;password=Secret123$;")

            elif self._verb == "logout":
                self._userName = None
                self._librarian_signed_In= False
                self._borrower_signed_In = False
                print("You've successfully signed out")
            elif self._verb == "quit":
                print("Goodbye, Mon chérie")
                exit()
            else:
                print("Unknown command, please enter a valid command")

            self.get_next_cmd()

    def parse_line(self, usr_input):
        """
        Description:
            Uses regex with named fields eg., <field> to parse verb and fields from user input
        :param usr_input: The users input
        :return: The 'True' in the case of a successful parsing or false otherwise
        """
        parsed_verb = False
        fields = {}
        verb = None
        verb_match = re.match(self._verb_regex, usr_input)
        if verb_match:
            verb = verb_match[0]
            parsed_verb = True

            try:
                field_matches = re.findall(self._fields_regex, usr_input)
                if field_matches:
                    for field, value in field_matches:
                        fields[field] = value
            except:
                print(f"bad input => '{usr_input}'")

        # todo: refactor into a property that takes these fields instead of creating instance fields on the fly
        self._fields = fields
        self._verb = verb
        return parsed_verb
