from decimal import Decimal
from typing import Sequence, TypeVar

from infrastructure.db.abc_repository import BaseRepository
from infrastructure.db.models.product import ProductModel

T = TypeVar("T")


class ProductRepository:
    def __init__(
        self,
        repository: BaseRepository,  # type: ignore - hack for DI
    ) -> None:
        self._repository: BaseRepository[ProductModel] = repository

    async def save_product(self, link: str, name: str, price: Decimal) -> None:
        await self._repository.create_obj(
            ProductModel, link=link, name=name, price=price
        )

    async def get_all_products(self) -> Sequence[ProductModel]:
        return await self._repository.get_all(ProductModel)
