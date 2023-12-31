"""
    FastAPI Builder
"""

from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any

from fastapi import FastAPI as _FastAPI

from infrastructure.lifespan import ABCLifespan
from presentation.asgi.abc_builder import ASGIApp, ASGIAppBuilder
from presentation.asgi.fastapi.abc_router import ABCRouterBuilder
from utils.logging import Logging


class FastAPIAppBuilder(ASGIAppBuilder):
    def __init__(
        self,
        logging: Logging,
        router_builders: list[ABCRouterBuilder],
        lifespans: list[ABCLifespan],  # type: ignore - hack for DI Container
        title: str,
        description: str = "",
    ) -> None:
        self._logger = logging.get_logger(__name__)
        self._router_builders = router_builders
        self._lifespans: list[ABCLifespan[Any]] = lifespans
        self._title = title
        self._description = description

    def create_app(self) -> ASGIApp:
        self._app = _FastAPI(
            title=self._title,
            description=self._description,
            lifespan=self._lifespan_for_every_worker,
        )

        for router_builder in self._router_builders:
            self._logger.debug(
                f"Registering router from {router_builder.__class__.__name__}"
            )
            router = router_builder.create_router()
            self._app.include_router(router)
        return self._app

    @asynccontextmanager
    async def _lifespan_for_every_worker(self, _: ASGIApp):
        async with AsyncExitStack() as stack:
            for lifespan in self._lifespans:
                await stack.enter_async_context(lifespan)
            yield
