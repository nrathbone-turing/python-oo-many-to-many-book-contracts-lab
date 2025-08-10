from typing import List

class Author:
    pass


class Book:
    """A book that can be written by many authors via contracts."""
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
        """All contracts that reference this book."""
        return [c for c in Contract.all if c.book is self]

    def authors(self) -> List["Author"]:
        """All authors for this book, via Contract (no duplicates)."""
        seen = set()
        out: List["Author"] = []
        for c in self.contracts():
            if c.author not in seen:
                out.append(c.author)
                seen.add(c.author)
        return out

    def __repr__(self) -> str:
        return f"Book(title={self.title!r})"


class Contract:
    pass