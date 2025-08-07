from decimal import Decimal

from pydantic import BaseModel, field_serializer

from src.db.models import Book as BookORM


def decimal_encoder(dec_value: Decimal) -> int | float:
    exponent = dec_value.as_tuple().exponent
    if isinstance(exponent, int) and exponent >= 0:
        return int(dec_value)
    else:
        return float(dec_value)


class Book(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    rating: Decimal
    price: Decimal

    @classmethod
    def from_orm(cls, book_orm: BookORM) -> "Book":
        return cls(
            id=book_orm.id,
            title=book_orm.title,
            author=book_orm.author,
            pages=book_orm.pages,
            rating=book_orm.rating,
            price=book_orm.price,
        )

    def to_orm(self) -> BookORM:
        return BookORM(
            id=self.id,
            title=self.title,
            author=self.author,
            pages=self.pages,
            rating=self.rating,
            price=self.price,
        )

    @field_serializer("rating")
    def serialize_rating(self, rating: Decimal, _info):
        return decimal_encoder(rating)

    @field_serializer("price")
    def serialize_price(self, price: Decimal, _info):
        return decimal_encoder(price)
