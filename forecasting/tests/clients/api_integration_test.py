import json
import os
from datetime import datetime

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
def test_example_forecast_expected(input_data, expected_status_code, expected_result):
    result = client.post("/forecast/", json=input_data)

    assert result.status_code == expected_status_code
    assert result.json() == expected_result


@pytest.mark.integration
@pytest.mark.parametrize(
    "filename",
    ["daily", "daily_n_weeks", "hourly", "hourly_n_weeks"],
)
def test_forecast_expected_from_files(filename: str):
    base_path = os.getcwd()
    with open(f"{base_path}/forecasting/tests/test_cases/{filename}/input.json", "rb") as f:
        input_data = f.read()
        input_data = json.loads(input_data)
    with open(f"{base_path}/forecasting/tests/test_cases/{filename}/output.json", "rb") as f:
        expected_result = f.read()
        expected_result = json.loads(expected_result)

    result = client.post("/forecast/", json=input_data)

    assert result.status_code == 200

    output: dict[datetime, float] = {datetime.fromisoformat(kv["date"]): kv["value"] for kv in result.json()}

    assert output == {datetime.fromisoformat(k): v for k, v in expected_result["forecast"].items()}
