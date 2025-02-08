from datetime import date, timedelta

from forecasting.const import EXAMPLE_INPUT
from forecasting.models.entities import Data
from forecasting.models.entities import Item as Prediction
from forecasting.models.factories import ForecastModelFactory
from forecasting.models.simple_average import SimpleAverageModel


def test_create_model_with_custom_registry():
    model = ForecastModelFactory({"TESTING": SimpleAverageModel}).create(model="TESTING")
    data = Data.load_from_dict(EXAMPLE_INPUT)
    data.horizon = 10
    start_date = date.fromisoformat(EXAMPLE_INPUT["start_date"])
    result = model.forecast(data)

    assert len(result) == data.horizon
    for i in range(data.horizon):
        assert result[i].date == start_date + timedelta(days=i)


def test_create_model_with_fake_model():
    today = date.today()

    class FakeModel:
        def forecast(self, data: Data) -> list[Prediction]:
            return [Prediction(date=today, value=0.0)]

    model = ForecastModelFactory({"TESTING": FakeModel}).create(model="TESTING")

    data = Data(historical=[], horizon=1, start_date=today)
    result = model.forecast(data)

    assert len(result) == 1
    for i in range(data.horizon):
        assert result[i].date == today + timedelta(days=i)
