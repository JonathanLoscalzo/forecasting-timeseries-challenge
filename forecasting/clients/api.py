import uvicorn

from forecasting.infra.fastapi.main import create_app

app = create_app()


def main():
    """Entry point to run the FastAPI application."""
    uvicorn.run("forecasting.clients.api:app", host="0.0.0.0", port=8000, reload=True)
