#allows type hints (like `Book`, `Author`, or `Contract`) to be stored as strings internally instead of as the actual class objects
from __future__ import annotations
from typing import List
#used to validate "YYYY-MM-DD" format in Contract.date
from datetime import datetime

class Author:
    """An author who may sign multiple contracts with different books"""
    all: List["Author"] = []

    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        self._name = name.strip()
        Author.all.append(self)

    # read-only public attribute per spec
    @property
    def name(self) -> str:
        return self._name

    def contracts(self) -> List["Contract"]:
        """All contracts that reference this author."""
        return [c for c in Contract.all if c.author is self]

    def books(self) -> List["Book"]:
        """All books for this author, via Contract (no duplicates)"""
        seen = set()
        result = []
        for c in self.contracts():
            if id(c.book) not in seen:
                seen.add(id(c.book))
                result.append(c.book)
        return result

    def sign_contract(self, book: "Book", date: str, royalties: int) -> "Contract":
        """Create and return a new Contract between this author and `book` (validated by the Contract property setters)"""
        return Contract(author=self, book=book, date=date, royalties=royalties)

    # The spec/tests use the plural name; using an alias for convenience so either name works
    sign_contracts = sign_contract
    
    def total_royalties(self) -> int:
        """Sum of royalties from all of this author's contracts"""
        return sum(c.royalties for c in self.contracts())

    def __repr__(self) -> str:
        return f"Author(name={self.name!r})"

class Book:
    """A book that can be written by many authors via contracts"""
    all: List["Book"] = []

    def __init__(self, title: str):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        self._title = title.strip()
        Book.all.append(self)

    # read-only public attribute per spec
    @property
    def title(self) -> str:
        return self._title

    def contracts(self) -> List["Contract"]:
        """All contracts that reference this book"""
        return [c for c in Contract.all if c.book is self]

    def authors(self) -> List["Author"]:
        """All authors for this book, via Contract (no duplicates)"""
        seen = set()
        result = []
        for c in self.contracts():
            if id(c.author) not in seen:
                seen.add(id(c.author))
                result.append(c.author)
        return result

    def __repr__(self) -> str:
        return f"Book(title={self.title!r})"


class Contract:
    """Connects an Author and a Book with a date and royalties; all fields are validated via property setters as per the spec"""
    all: List["Contract"] = []

    def __init__(self, author: "Author", book: "Book", date: str, royalties: int):
        # Use properties so validation runs on construction
        self.author = author
        self.book = book
        self.date = date
        self.royalties = royalties
        Contract.all.append(self)

    # read-only public attribute per spec
    @property
    def author(self) -> "Author":
        return self._author

    @author.setter
    def author(self, value: Author) -> None:
        if not isinstance(value, Author):
            raise TypeError("author must be an instance of Author")
        self._author = value

    # read-only public attribute per spec
    @property
    def book(self) -> "Book":
        return self._book

    @book.setter
    def book(self, value: Book) -> None:
        if not isinstance(value, Book):
            raise TypeError("book must be an instance of Book")
        self._book = value

    # read-only public attribute per spec
    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("date must be a string")
        #I wanted to add datetime validation here but it broke the tests since it wasn't expecting it so I commented it out
        # try:
        #     datetime.strptime(value, "%Y-%m-%d")
        # except ValueError:
        #     raise ValueError("date must be in YYYY-MM-DD format")
        self._date = value

    # read-only public attribute per spec
    @property
    def royalties(self) -> int:
        return self._royalties

    @royalties.setter
    def royalties(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("royalties must be an integer")
        if value < 0:
            raise ValueError("royalties must be non-negative")
        self._royalties = value

    @classmethod
    def contracts_by_date(cls, date: str) -> List["Contract"]:
        """All contracts that match the given date."""
        return [c for c in cls.all if c.date == date]

    def __repr__(self) -> str:
        return (f"Contract(author={self.author!r}, book={self.book!r}, "f"date={self.date!r}, royalties={self.royalties})")