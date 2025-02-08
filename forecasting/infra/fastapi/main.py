import logging

from fastapi import FastAPI

from forecasting.infra.fastapi.routers import inference
from forecasting.infra.injector import ApiContainer
from forecasting.infra.logging import InterceptHandler


def create_app() -> FastAPI:
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    app = FastAPI()

    container = ApiContainer()
    app.container = container  # type: ignore

    app.include_router(inference.router)

    return app
