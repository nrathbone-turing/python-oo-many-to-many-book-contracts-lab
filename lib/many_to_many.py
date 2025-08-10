from typing import List

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
    pass