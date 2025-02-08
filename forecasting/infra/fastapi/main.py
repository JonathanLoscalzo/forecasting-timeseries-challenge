from fastapi import FastAPI

from forecasting.infra.fastapi.routers import inference


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(inference.router)

    return app
