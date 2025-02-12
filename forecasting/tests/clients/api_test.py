from typing import Optional, Protocol

import pytest
from dependency_injector import providers
from fastapi import FastAPI
from fastapi.testclient import TestClient

from forecasting.clients.api import create_app
from forecasting.const import EXAMPLE_INPUT
from forecasting.models.const import ModelName
from forecasting.models.core import ForecastModelProtocol
from forecasting.models.factories import ForecastModelFactory
from forecasting.models.simple_average import SimpleAverageModel


class TestClientFixture(Protocol):
    __test__ = False

    def __call__(self) -> TestClient: ...


@pytest.fixture
def create_test_client() -> TestClient:
    return TestClient(create_app())


class ForecastModelFactoryFake(ForecastModelFactory):
    called = False

    def create(self, model: Optional[ModelName | str], **config) -> ForecastModelProtocol:
        ForecastModelFactoryFake.called = True
        return SimpleAverageModel(**config)


@pytest.mark.parametrize(
    ("input_data", "expected_status_code", "expected_result"),
    [
        (
            EXAMPLE_INPUT,
            200,
            [
                {"date": "2024-05-10T00:00:00", "value": 10.0},
                {"date": "2024-05-11T00:00:00", "value": 11.9375},
                {"date": "2024-05-12T00:00:00", "value": 16.3125},
                {"date": "2024-05-13T00:00:00", "value": 10.1875},
                {"date": "2024-05-14T00:00:00", "value": 2.0625},
                {"date": "2024-05-15T00:00:00", "value": 10.0625},
                {"date": "2024-05-16T00:00:00", "value": 7.75},
            ],
        )
    ],
)
def test_client_forecast(
    create_test_client: TestClient,
    input_data,
    expected_status_code,
    expected_result,
):
    client = create_test_client
    app: FastAPI = client.app  # type: ignore
    app.container.model_factory.override(providers.Factory(ForecastModelFactoryFake))  # type: ignore
    result = client.post("/forecast/", json=input_data)

    assert result.status_code == expected_status_code
    assert result.json() == expected_result
    assert ForecastModelFactoryFake.called  # type: ignore
