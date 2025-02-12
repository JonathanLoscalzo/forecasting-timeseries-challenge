from datetime import datetime

from forecasting.const import EXAMPLE_INPUT
from forecasting.models.entities import Data, Item
from forecasting.models.simple_average import SimpleAverageModel


def test_simple_average_model__default_input__generates_prediction():
    model = SimpleAverageModel()

    data = Data.load_from_dict(EXAMPLE_INPUT)

    result = model.forecast(data)
    expected_result = [
        Item(date=datetime.fromisoformat(item["date"]), value=item["value"])
        for item in [
            {"date": "2024-05-10T00:00:00", "value": 10.0},
            {"date": "2024-05-11T00:00:00", "value": 11.9375},
            {"date": "2024-05-12T00:00:00", "value": 16.3125},
            {"date": "2024-05-13T00:00:00", "value": 10.1875},
            {"date": "2024-05-14T00:00:00", "value": 2.0625},
            {"date": "2024-05-15T00:00:00", "value": 10.0625},
            {"date": "2024-05-16T00:00:00", "value": 7.75},
        ]
    ]
    assert len(result) == data.horizon
    assert expected_result == result
