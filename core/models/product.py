from decimal import Decimal

from core.models.base import BaseModel


class Product(BaseModel):
    name: str
    price: Decimal
