import typing as t
from collections.abc import Sequence
from decimal import Decimal
from types import TracebackType

import pytest

from src.db.models import Book as BookORM
from src.db.repository import NotSupportedAttributeException, RepositoryInterface
from src.db.uow import UnitOfWorkInterface
from src.entities import Book
from src.usecases import (
    get_all_books,
    get_book_by_id,
    get_books_by_pages,
    get_books_by_title,
)


class FakeBooksRepository(RepositoryInterface[BookORM, Book]):
    def __init__(self, data: list[BookORM] | None = None) -> None:
        self._data: list[BookORM] = data or []

    async def get_all_items(self) -> Sequence[BookORM]:
        return self._data

    async def get_item_by_id(self, id_: int) -> BookORM | None:
        return next((item for item in self._data if item.id == id_), None)

    async def get_items_by_attribute(
        self, attr_type: str, attr: str | int
    ) -> Sequence[BookORM]:
        if attr_type == "title":
            ret = [b for b in self._data if b.title == attr]
        elif attr_type == "min_pages":
            ret = [b for b in self._data if b.pages >= attr]  # type: ignore[operator]
        else:
            raise NotSupportedAttributeException()
        return ret

    async def create_item(self, input_model: Book) -> BookORM:
        book_orm: BookORM = input_model.to_orm()
        self._data.append(book_orm)
        return book_orm

    async def update_item(
        self, previous: BookORM, input_model: Book
    ) -> BookORM | None:  # noqa: E501
        previous.price = float(input_model.price)
        previous.rating = float(input_model.rating)
        return previous


class FakeUnitOfWork(UnitOfWorkInterface):
    def __init__(self, fake_repo: FakeBooksRepository | None = None) -> None:
        self.commited = False
        self.books_repo = fake_repo or FakeBooksRepository()

    async def __aenter__(self) -> t.Self:
        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_value, traceback)

    async def commit(self) -> None:
        self.commited = True

    async def rollback(self) -> None:
        self.commited = False


@pytest.fixture
def fake_uow_with_data() -> tuple[FakeUnitOfWork, list[BookORM]]:
    input_ = [
        BookORM(
            id=1,
            title="Pinocchio",
            author="Carlo Collodi",
            pages=189,
            rating=Decimal(3.33),
            price=Decimal(1.99),
        ),
        BookORM(
            id=2,
            title="Some",
            author="Random Author",
            pages=2137,
            rating=Decimal(5.4),
            price=Decimal(2.33),
        ),
    ]
    fuow = FakeUnitOfWork(FakeBooksRepository(data=input_))
    return fuow, input_


async def test_get_all_books_returns_empty_list_on_no_data() -> None:
    fuow = FakeUnitOfWork()

    assert not await get_all_books(fuow)


async def test_get_all_books_returns_data(
    fake_uow_with_data: tuple[FakeUnitOfWork, list[BookORM]],
) -> None:
    fuow, data = fake_uow_with_data
    ret = await get_all_books(fuow)

    assert ret[0] == Book.from_orm(data[0])


async def test_get_book_by_id_returns_correct_book(
    fake_uow_with_data: tuple[FakeUnitOfWork, list[BookORM]],
) -> None:
    fuow, input_ = fake_uow_with_data

    ret = await get_book_by_id(2, fuow)

    assert ret == Book.from_orm(input_[1])


async def test_get_book_by_id_returns_none_on_not_found_book(
    fake_uow_with_data: tuple[FakeUnitOfWork, list[BookORM]],
) -> None:
    fuow, input_ = fake_uow_with_data

    assert not await get_book_by_id(5, fuow)


async def test_get_books_by_title_returns_correct_books(
    fake_uow_with_data: tuple[FakeUnitOfWork, list[BookORM]],
) -> None:
    fuow, input_ = fake_uow_with_data

    ret = await get_books_by_title(input_[0].title, fuow)

    assert ret[0] == Book.from_orm(input_[0])


async def test_get_books_by_title_returns_empty_list_on_no_match(
    fake_uow_with_data: tuple[FakeUnitOfWork, list[BookORM]],
) -> None:
    fuow, input_ = fake_uow_with_data

    assert not await get_books_by_title("Random Title", fuow)


async def test_get_books_by_pages_returns_correct_books(
    fake_uow_with_data: tuple[FakeUnitOfWork, list[BookORM]],
) -> None:
    fuow, input_ = fake_uow_with_data
    fuow = FakeUnitOfWork(FakeBooksRepository(data=input_))

    ret = await get_books_by_pages(100, fuow)

    assert len(ret) == len(input_)
    assert ret[0] == Book.from_orm(input_[0])


async def test_get_books_by_pages_returns_empty_list_on_no_match(
    fake_uow_with_data: tuple[FakeUnitOfWork, list[BookORM]],
) -> None:
    fuow, input_ = fake_uow_with_data

    assert not await get_books_by_pages(3000, fuow)
