from datetime import date

from forecasting.const import EXAMPLE_INPUT
from forecasting.models.entities import Data, Item
from forecasting.models.simple_average import SimpleAverageModel


def test_simple_average_model__default_input__generates_prediction():
    model = SimpleAverageModel()

    data = Data.load_from_dict(EXAMPLE_INPUT)

    result = model.forecast(data)
    expected_result = [
        Item(date=date.fromisoformat(item["date"]), value=item["value"])
        for item in [
            {"date": "2024-05-10", "value": 11.0},
            {"date": "2024-05-11", "value": 10.75},
            {"date": "2024-05-12", "value": 15.25},
            {"date": "2024-05-13", "value": 9.8},
            {"date": "2024-05-14", "value": 4.0},
            {"date": "2024-05-15", "value": 11.0},
            {"date": "2024-05-16", "value": 8.0},
        ]
    ]
    assert len(result) == data.horizon
    assert expected_result == result
