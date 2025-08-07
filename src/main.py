from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import create_session
from src.entities import Book, UpdateBookPriceAndRating
from src.usecases import (
    create_book,
    get_all_books,
    get_book_by_id,
    get_books_by_pages,
    get_books_by_title,
    update_books_price_and_rating,
)

app = FastAPI()


@app.get("/")
def hello_world() -> str:
    return "Hello world!"


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/books/{id_}")
async def get_book(
    id_: int, session: Annotated[AsyncSession, Depends(create_session)]
) -> Book:
    book = await get_book_by_id(id_, session)
    if not book:
        raise HTTPException(404)
    return book


@app.get("/books")
async def get_books(
    session: Annotated[AsyncSession, Depends(create_session)],
    title: str | None = None,
    min_pages: int | None = None,
) -> list[Book]:
    if title:
        return await get_books_by_title(title, session)
    if min_pages:
        return await get_books_by_pages(min_pages, session)
    else:
        return await get_all_books(session)


@app.post("/books")
async def post_book(
    session: Annotated[AsyncSession, Depends(create_session)], book: Book
) -> Book:
    try:
        ret = await create_book(book, session)
    except Exception as exc:
        print(exc)
        raise HTTPException(400)
    else:
        return ret


@app.put("/books/{id_}")
async def update_book_price_and_rating(
    id_: int,
    price_and_rating: UpdateBookPriceAndRating,
    session: Annotated[AsyncSession, Depends(create_session)],
) -> Book:
    try:
        ret = await update_books_price_and_rating(
            id_, price_and_rating.model_dump(), session
        )
    except Exception as exc:
        raise HTTPException(400)
    else:
        return ret
