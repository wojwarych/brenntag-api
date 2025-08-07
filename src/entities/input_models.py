from decimal import Decimal

from pydantic import BaseModel


class UpdateBookPriceAndRating(BaseModel):
    rating: Decimal
    price: Decimal
