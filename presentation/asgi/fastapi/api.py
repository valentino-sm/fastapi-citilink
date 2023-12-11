from fastapi import APIRouter

from core.models.product import Product
from core.services.shop import ShopService
from presentation.asgi.fastapi.abc_router import ABCRouterBuilder
from utils.logging import Logging


class APIRouterBuilder(ABCRouterBuilder):
    def __init__(
        self,
        logging: Logging,
        shop_service: ShopService,
        default_link: str,
    ) -> None:
        self._logging = logging
        self._logger = logging.get_logger(__name__)
        self._shop_service = shop_service
        self._default_link = default_link

    def create_router(self) -> APIRouter:
        router = APIRouter(prefix="/api/v1", tags=["API v1"])

        @router.post("/process", response_model=Product)
        async def _(product_link: str = self._default_link):
            """
            Save product to Database
            """
            return await self._shop_service.process_product(product_link)

        @router.get("/products")
        async def _():
            """
            Get all products from Database
            """
            return await self._shop_service.get_all_products()

        return router
