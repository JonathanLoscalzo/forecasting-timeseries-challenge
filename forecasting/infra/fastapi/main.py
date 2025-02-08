from fastapi import FastAPI

from forecasting.infra.fastapi.routers import inference
from forecasting.infra.injector import ApiContainer


def create_app() -> FastAPI:
    app = FastAPI()

    container = ApiContainer()
    app.container = container  # type: ignore

    app.include_router(inference.router)

    return app
