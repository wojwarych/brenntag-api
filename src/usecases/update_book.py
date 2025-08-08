import logging
from decimal import Decimal

from src.db.uow import UnitOfWorkInterface
from src.entities.entities import Book

logger = logging.getLogger(__name__)


async def update_books_price_and_rating(
    id_: int, price_and_rating: dict[str, Decimal], uow: UnitOfWorkInterface
) -> Book:
    async with uow:
        try:
            book_orm = await uow.books_repo.get_item_by_id(id_)
            if book_orm:
                logger.debug(
                    f"Old price and rating: price={book_orm.price}, rating={book_orm.rating}"
                )
                book_entity = Book.from_orm(book_orm)
                book_entity.update_price_and_rating(price_and_rating)
                book_orm = await uow.books_repo.update_item(book_orm, book_entity)
                if book_orm:
                    await uow.commit()
                    logger.info(
                        f"Successfully updated price and rating for book: {book_orm}, price={book_orm.price}, rating={book_orm.rating}"
                    )
                    return book_entity
                else:
                    raise Exception()
            raise Exception()
        except Exception as exc:
            logger.exception(exc)
            return None
