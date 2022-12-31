class book:

    def __init__(self, title: str, author: str, qty: int) -> None:
        """

        :param title: The title of  the book
        :param author: The author of the book
        :param qty: The amount of this particular books available in the library
        """
        self._title = title
        self._author = author
        self._qty = qty

    def __str__(self):
        return f"Title = {self._title}, Author = {self._author}, qty = {self._qty}"

    @property
    def title(self):
        return self._title

    @property
    def qty(self):
        return self._qty