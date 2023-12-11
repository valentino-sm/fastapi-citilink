from core.models.product import Product
from core.services.scraper import ABCProductScraper
from infrastructure.db.repositories.product import ProductRepository
from infrastructure.db.session_manager import ABCSessionManager
from utils.logging import Logging


class ShopService:
    """
    Business logic
    """

    def __init__(
        self,
        logging: Logging,
        session_manager: ABCSessionManager,
        product_scraper: ABCProductScraper,
        product_repository: ProductRepository,
    ) -> None:
        self._logger = logging.get_logger(__name__)
        self._session_manager = session_manager
        self._product_scraper = product_scraper
        self._product_repository = product_repository

    async def process_product(self, product_link: str) -> Product:
        self._logger.debug(f"Save product {product_link}")
        product = await self._product_scraper.get_product(product_link)
        async with self._session_manager():
            await self._product_repository.save_product(
                link=product_link, name=product.name, price=product.price
            )
        return product

    async def get_all_products(self):
        self._logger.debug("Get all products")
        async with self._session_manager():
            return await self._product_repository.get_all_products()
