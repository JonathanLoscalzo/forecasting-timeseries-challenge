import pytest
from fastapi.testclient import TestClient

from forecasting.clients.api import app
from forecasting.const import EXAMPLE_INPUT

client = TestClient(app)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("input_data", "expected_status_code", "expected_result"),
    [
        (
            EXAMPLE_INPUT,
            200,
            [
                {"date": "2024-05-10", "value": 11.0},
                {"date": "2024-05-11", "value": 10.75},
                {"date": "2024-05-12", "value": 15.25},
                {"date": "2024-05-13", "value": 9.8},
                {"date": "2024-05-14", "value": 4.0},
                {"date": "2024-05-15", "value": 11.0},
                {"date": "2024-05-16", "value": 8.0},
            ],
        )
    ],
)
def test_example_forecast_expected(input_data, expected_status_code, expected_result):
    result = client.post("/forecast/", json=input_data)

    assert result.status_code == expected_status_code
    assert result.json() == expected_result
