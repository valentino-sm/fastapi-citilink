from decimal import Decimal
from typing import Protocol

from bs4 import BeautifulSoup

from core.models.product import Product
from infrastructure.http import ABCHTTPClient
from utils.logging import Logging


class ABCProductScraper(Protocol):
    async def get_product(self, prodict_link: str) -> Product:
        ...


class CitilinkProductScraper(ABCProductScraper):
    def __init__(self, logging: Logging, http_client: ABCHTTPClient) -> None:
        self._logger = logging.get_logger(__name__)
        self._http_client = http_client

    async def get_product(self, prodict_link: str) -> Product:
        page_body = await self._http_client.get(url=prodict_link)
        soup = BeautifulSoup(page_body, "html.parser")
        try:
            product_name = (
                soup.body.find("div", {"data-meta-name": "ProductHeaderLayout__title"})
                .find("h1")
                .text
            )
            product_price = soup.body.find(
                "div", {"data-meta-name": "PriceBlock__price"}
            ).span.span.span.text
            product_name = str(product_name.strip())
            product_price = Decimal(product_price.strip())
        except Exception as e:
            self._logger.error(e)
            raise ValueError("Failed to parse product") from e
        return Product(name=product_name, price=product_price)
