from typing import Any, Protocol

from httpx import AsyncClient
from tenacity import (RetryCallState, retry, retry_if_exception_type,
                      stop_after_attempt, wait_exponential, wait_random)

from utils.exceptions import QuietException
from utils.logging import Logging


class RetryException(QuietException):
    pass


class ABCHTTPClient(Protocol):
    async def request(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError

    async def get(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError

    async def post(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError


class HTTPXUtils:
    @staticmethod
    def error_callback(retry_state: RetryCallState) -> None:
        raise RetryException(retry_state, retry_state.args, retry_state.kwargs)


class HTTPXClient(ABCHTTPClient):
    def __init__(self, logging: Logging) -> None:
        self._logger = logging.get_logger(__name__)

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(6),
        wait=wait_exponential(multiplier=1, min=1, max=10)
        + wait_random(min=0.1, max=0.5),
        retry_error_callback=HTTPXUtils.error_callback,
    )
    async def request(self, *args: Any, **kwargs: Any) -> str:
        async with AsyncClient() as client:
            response = await client.request(*args, **kwargs)
        response.raise_for_status()
        return response.text

    async def get(self, *args: Any, **kwargs: Any) -> str:
        return await self.request(method="GET", *args, **kwargs)

    async def post(self, *args: Any, **kwargs: Any) -> str:
        return await self.request(method="POST", *args, **kwargs)
