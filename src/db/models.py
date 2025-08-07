from sqlalchemy import Double, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    author: Mapped[str] = mapped_column(String(64))
    pages: Mapped[int]
    rating: Mapped[float] = mapped_column(Double())
    price: Mapped[float] = mapped_column(Double())

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r}, author={self.author!r}"
