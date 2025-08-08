import logging


from src.db.uow import UnitOfWorkInterface
from src.entities.entities import Book

logger = logging.getLogger(__name__)


async def create_book(book: Book, uow: UnitOfWorkInterface) -> Book:
    async with uow:
        await uow.books_repo.create_item(book)
        await uow.commit()
    logging.info(f"Successfully created book: {book}")
    return book
