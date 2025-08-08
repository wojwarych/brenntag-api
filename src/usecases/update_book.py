from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.db.models import Book as BookORM
from src.entities.entities import Book


async def update_books_price_and_rating(
    id_: int, price_and_rating: dict[str, Decimal], async_session: AsyncSession
) -> Book:
    stmt = select(BookORM).where(BookORM.id == id_)
    async with async_session as async_sess:
        try:
            book = (await async_sess.scalars(stmt)).one()
            book_entity = Book.from_orm(book)
            book_entity.update_price_and_rating(price_and_rating)
            book.price = book_entity.price
            book.rating = book_entity.rating
            await async_sess.commit()
            return Book.from_orm(book)
        except Exception as exc:
            print(exc)
            return None
