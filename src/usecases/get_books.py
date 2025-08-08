import logging

from src.db.uow import UnitOfWorkInterface
from src.entities.entities import Book

logger = logging.getLogger(__name__)


async def get_all_books(uow: UnitOfWorkInterface) -> list[Book]:
    async with uow:
        return [Book.from_orm(b) for b in await uow.books_repo.get_all_items()]


async def get_book_by_id(book_id: int, uow: UnitOfWorkInterface) -> Book | None:
    async with uow:
        book = await uow.books_repo.get_item_by_id(book_id)
        if book:
            return Book.from_orm(book)
    return None


async def get_books_by_title(title: str, uow: UnitOfWorkInterface) -> list[Book]:
    async with uow:
        return [
            Book.from_orm(b)
            for b in await uow.books_repo.get_items_by_attribute("title", title)
        ]


async def get_books_by_pages(min_pages: int, uow: UnitOfWorkInterface) -> list[Book]:
    async with uow:
        return [
            Book.from_orm(b)
            for b in await uow.books_repo.get_items_by_attribute("min_pages", min_pages)
        ]
