from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from src.db.models import Book as BookORM
from src.entities.entities import Book


async def create_book(book: Book, async_session: AsyncSession) -> Book:
    async with async_session as async_sess:
        book_orm: BookORM = book.to_orm()
        async_session.add(book_orm)
        await async_sess.commit()
    return book
