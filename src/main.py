import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status

from src.db.uow import UnitOfWorkInterface, create_sql_unit_of_work
from src.entities import Book, UpdateBookPriceAndRating
from src.log_conf import LOGGING_CONFIG
from src.usecases import (
    create_book,
    get_all_books,
    get_book_by_id,
    get_books_by_pages,
    get_books_by_title,
    update_books_price_and_rating,
)

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def hello_world() -> str:
    return "Hello world!"


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/books/{id_}")
async def get_book(
    id_: int, uow: Annotated[UnitOfWorkInterface, Depends(create_sql_unit_of_work)]
) -> Book:
    logger.info(f"Request for book of id: {id_}")
    book = await get_book_by_id(id_, uow)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return book


@app.get("/books")
async def get_books(
    uow: Annotated[UnitOfWorkInterface, Depends(create_sql_unit_of_work)],
    title: str | None = None,
    min_pages: int | None = None,
) -> list[Book]:
    logger.info(
        f"Request for list of book with query param title={title} or min_pages={min_pages}"
    )
    if title:
        return await get_books_by_title(title, uow)
    if min_pages:
        return await get_books_by_pages(min_pages, uow)
    else:
        return await get_all_books(uow)


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def post_book(
    uow: Annotated[UnitOfWorkInterface, Depends(create_sql_unit_of_work)], book: Book
) -> Book:
    logger.info(f"Request to create book with data: {book}")
    try:
        ret = await create_book(book, uow)
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return ret


@app.put("/books/{id_}")
async def update_book_price_and_rating(
    id_: int,
    price_and_rating: UpdateBookPriceAndRating,
    uow: Annotated[UnitOfWorkInterface, Depends(create_sql_unit_of_work)],
) -> Book:
    logger.info(f"Request to update price and rating of book with id: {id_}")
    logger.debug(f"New price and rating: {price_and_rating}")
    try:
        ret = await update_books_price_and_rating(
            id_, price_and_rating.model_dump(), uow
        )
        if not ret:
            raise Exception()
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return ret
