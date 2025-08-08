from decimal import Decimal

import pytest

from src.entities import Book


@pytest.fixture
def book() -> Book:
    return Book(id=3, title="Lord of the Rings", author="J.R.R. Tolkien", pages=1090, rating=Decimal(4.4), price=Decimal(2.33))

@pytest.fixture
def price_and_rating() -> dict[str, Decimal]:
    return {"price": Decimal(30.0), "rating": Decimal(6.0)}


def test_book_update_price_and_rating_sets_correct_values(
    book: Book, price_and_rating: dict[str, Decimal]
) -> None:
    book.update_price_and_rating(price_and_rating)

    assert book.price == price_and_rating["price"]
    assert book.rating == price_and_rating["rating"]
