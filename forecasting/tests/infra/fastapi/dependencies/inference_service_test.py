from datetime import date, timedelta

from forecasting.infra.fastapi.dependencies import InferenceService
from forecasting.infra.fastapi.routers.dtos import Data as DataInput
from forecasting.models.factories import ForecastModelFactory


def test_inference_service__receives_default_input__returns_forecast():
    factory = ForecastModelFactory()
    service = InferenceService(factory)
    start_date = date(2021, 1, 1)
    historical_start_date = start_date - timedelta(days=20)
    data = DataInput(
        horizon=7,
        start_date=start_date,
        historical={historical_start_date + timedelta(days=i): i + 1 * 10 for i in range(15)},
    )
    result = service.forecast(
        data,
    )

    assert len(result) == data.horizon
    assert result[0].date == start_date
    assert result[-1].date == start_date + timedelta(days=data.horizon - 1)
