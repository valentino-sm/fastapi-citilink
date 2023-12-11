from fastapi import APIRouter

from core.models.product import Product
from core.services.shop import ShopService
from infrastructure.db.models.product import ProductModel
from presentation.asgi.fastapi.abc_router import ABCRouterBuilder
from utils.logging import Logging


class APIRouterBuilder(ABCRouterBuilder):
    def __init__(
        self,
        logging: Logging,
        shop_service: ShopService,
    ) -> None:
        self._logging = logging
        self._logger = logging.get_logger(__name__)
        self._shop_service = shop_service

    def create_router(self) -> APIRouter:
        router = APIRouter(prefix="/api/v1", tags=["API v1"])

        @router.post("/process", response_model=Product)
        async def _(product_link: str):
            """
            Save product to Database
            """
            return await self._shop_service.process_product(product_link)

        @router.get("/products", response_model=list[ProductModel])
        async def _():
            """
            Get all products from Database
            """
            return await self._shop_service.get_all_products()

        return router
