from datetime import date, timedelta

from forecasting.const import EXAMPLE_INPUT
from forecasting.models.entities import Data
from forecasting.models.prophet import ProphetModel


def test_simple_average_model_generates_prediction():
    model = ProphetModel()

    data = Data.load_from_dict(EXAMPLE_INPUT)
    start_date = date.fromisoformat(EXAMPLE_INPUT["start_date"])

    result = model.forecast(data)
    assert len(result) == data.horizon

    for i in range(data.horizon):
        assert result[i].date == start_date + timedelta(days=i)
