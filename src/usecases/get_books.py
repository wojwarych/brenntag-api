from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.db.models import Book as BookORM
from src.entities.entities import Book


async def get_all_books(async_session: AsyncSession) -> list[Book]:
    stmt = select(BookORM)
    async with async_session as async_sess:
        try:
            books = await async_sess.execute(stmt)
        except Exception as exc:
            print(exc)
            return []
        else:
            return [Book.from_orm(b) for b in books.scalars()]


async def get_book_by_id(book_id: int, async_session: AsyncSession) -> Book | None:
    stmt = select(BookORM).where(BookORM.id == book_id)
    async with async_session as async_sess:
        try:
            book = (await async_sess.scalars(stmt)).one()
        except Exception as exc:
            print(exc)
            return None
        else:
            return Book.from_orm(book)


async def get_books_by_title(title: str, async_session: AsyncSession) -> list[Book]:
    stmt = select(BookORM).where(BookORM.title == title)
    async with async_session as async_sess:
        try:
            books = await async_sess.scalars(stmt)
        except Exception as exc:
            print(exc)
            return []
        else:
            return [Book.from_orm(b) for b in books]


async def get_books_by_pages(min_pages: int, async_session: AsyncSession) -> list[Book]:
    stmt = select(BookORM).where(BookORM.pages >= min_pages)
    async with async_session as async_sess:
        try:
            books = await async_sess.scalars(stmt)
        except Exception as exc:
            print(exc)
            return []
        else:
            return [Book.from_orm(b) for b in books]
