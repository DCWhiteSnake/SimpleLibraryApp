from user import user


class authenticationHandler:
    def __init__(self):
        self._test_borrower = user(username="testBorrower", password="pass", usertype="Borrower")
        self._test_librarian = user(username="testLibrarian", password="pass", usertype="Librarian")
        self._user_store = {'testBorrower': self._test_borrower,
                            'testLibrarian': self._test_librarian}

    def sign_in(self, username: str, password: str) -> [bool, str, str, str]:
        """
        signs in a regular user ie., a borrower
        :param username: the username you registered with
        :param password: the password you registered with
        :return: true if your signin was a success, your username and your usertype
        """
        usertype = "Invalid"
        errorReason = ""
        try:
            value = self._user_store[username] is None
        except KeyError:
            authStatus = False
            errorReason = "This user does not exist"
            return [authStatus, username, usertype, errorReason]
        if self._user_store[username].password == password:
            usertype = self._user_store[username].usertype
            authStatus = True
        else:
            authStatus = False
            errorReason = "userName and password don't match"

        return [authStatus, username, usertype, errorReason]

    def sign_in_librarian(self, username: str, password: str) -> [bool, str, str, str]:
        """
        signs in a regular user ie., a borrower
        :param username: the username you registered with
        :param password: the password you registered with
        :return: true if your signin was a success, your username and your usertype
        """
        usertype = "Invalid"
        errorReason = ""
        if not self._user_store[username]:
            authStatus = False
            errorReason = "This user does not exist"
        else:
            if self._user_store[username].usertype == "librarian":
                if self._user_store[username].password == password:
                    usertype = self._user_store[username].usertype
                    authStatus = True
                else:
                    authStatus = False
                    errorReason = "userName and password don't match"
            else:
                authStatus = False
                errorReason = "Unauthorized"

        return [authStatus, username, usertype, errorReason]

    def register(self, username: str, password: str) -> [bool, str, str]:
        """

        :param username: the username you registered with
        :param password: the password you registered with
        :return: true if your signin was a success, your username and your usertype
        """
        usertype = "Borrower"
        errorReason = ""
        # if we get a key error then the user name is unique
        try:
            _ = self._user_store[username]
            # automatically sign-in after registration
            errorReason = "A user with this username already exists"
            authStatus = False

        except:
            authStatus = True
            self._user_store[username] = user(username=username, password=password, usertype=usertype)
        return [authStatus, username, usertype, errorReason]

    @property
    def user_store(self):
        return self._user_store
