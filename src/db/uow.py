import typing as t
from collections.abc import AsyncIterator
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.engine import DEFAULT_SESSION_FACTORY
from src.db.models import Book as BookORM
from src.db.repository import RepositoryInterface, SQLBooksRepository
from src.entities import Book

T = t.TypeVar("T", bound=BookORM)
R = t.TypeVar("R", bound=Book)


class UnitOfWorkInterface(t.Protocol):
    books_repo: RepositoryInterface[BookORM, Book]

    async def __aenter__(self) -> t.Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.rollback()

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class SQLAlchemyUnitOfWork(UnitOfWorkInterface):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = DEFAULT_SESSION_FACTORY,
    ) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> t.Self:
        self.session = self._session_factory()
        self.books_repo = SQLBooksRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_value, traceback)
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


async def create_sql_unit_of_work() -> AsyncIterator[SQLAlchemyUnitOfWork]:
    uow = SQLAlchemyUnitOfWork()
    yield uow
