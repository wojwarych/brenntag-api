import logging
import typing as t
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.db.models import Book as BookORM
from src.entities import Book

logger = logging.getLogger(__name__)

T = t.TypeVar("T", bound=BookORM)
R = t.TypeVar("R", bound=Book, contravariant=True)


class NotSupportedAttributeException(Exception): ...


class RepositoryInterface(t.Protocol[T, R]):
    async def get_all_items(self) -> Sequence[T]: ...

    async def get_items_by_attribute(
        self, attr_type: str, attr_value: str | int
    ) -> Sequence[T]: ...

    async def get_item_by_id(self, id_: int) -> T | None: ...

    async def create_item(self, input_model: R) -> T: ...

    async def update_item(self, previous: T, input_model: R) -> T | None: ...


class SQLBooksRepository(RepositoryInterface[BookORM, Book]):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_items(self) -> Sequence[BookORM]:
        try:
            stmt = select(BookORM)
            books = await self._session.scalars(stmt)
        except Exception as exc:
            logger.exception(exc)
            return []
        else:
            return books.all()

    async def get_items_by_attribute(
        self, attr_type: str, attr: str | int
    ) -> Sequence[BookORM]:
        if attr_type == "title":
            stmt = select(BookORM).where(BookORM.title == attr)
        elif attr_type == "min_pages":
            stmt = select(BookORM).where(BookORM.pages >= attr)
        else:
            raise NotSupportedAttributeException()

        try:
            books = await self._session.scalars(stmt)
        except Exception as exc:
            logger.exception(exc)
            return []
        else:
            return books.all()

    async def get_item_by_id(self, id_: int) -> BookORM | None:
        stmt = select(BookORM).where(BookORM.id == id_)
        try:
            book = (await self._session.scalars(stmt)).one()
        except Exception as exc:
            logger.exception(exc)
            return None
        else:
            return book

    async def create_item(self, input_model: Book) -> BookORM:
        book_orm: BookORM = input_model.to_orm()
        self._session.add(book_orm)
        return book_orm

    async def update_item(self, previous: BookORM, input_model: Book) -> BookORM | None:
        try:
            previous.price = float(input_model.price)
            previous.rating = float(input_model.rating)
            return previous
        except Exception as exc:
            logger.exception(exc)
            return None
