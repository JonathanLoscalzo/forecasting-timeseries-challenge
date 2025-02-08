import pytest
from fastapi.testclient import TestClient

from forecasting.clients.api import app
from forecasting.const import EXAMPLE_INPUT

client = TestClient(app)


@pytest.mark.integration
def test_example_forecast_expected():
    result = client.post("/forecast/", json=EXAMPLE_INPUT)

    assert result.status_code == 200
    assert result.json() == [
        {"date": "2024-05-10", "value": 11.0},
        {"date": "2024-05-11", "value": 10.75},
        {"date": "2024-05-12", "value": 15.25},
        {"date": "2024-05-13", "value": 9.8},
        {"date": "2024-05-14", "value": 4.0},
        {"date": "2024-05-15", "value": 11.0},
        {"date": "2024-05-16", "value": 8.0},
    ]
