import uuid


class user:
    def __init__(self, username: str, password: str, usertype: str):
        self._username = username
        self._password = password
        self._usertype = usertype

    @property
    def password(self):
        return self._password

    @property
    def usertype(self):
        return self._usertype
