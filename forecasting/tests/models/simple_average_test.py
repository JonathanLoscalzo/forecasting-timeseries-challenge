from forecasting.models.entities import Data, Item
from forecasting.models.simple_average import SimpleAverageModel
from datetime import date


def test_simple_average_model_generates_prediction():
    model = SimpleAverageModel()

    data = Data(
        horizon=7,
        start_date=date(2024, 5, 10),
        historical=[
            Item(date=date.fromisoformat(d), value=v)
            for d, v in {
                "2024-04-01": 10,
                "2024-04-02": 11,
                "2024-04-03": 14,
                "2024-04-04": 8,
                "2024-04-05": 15,
                "2024-04-06": 6,
                "2024-04-07": 11,
                "2024-04-08": 8,
                "2024-04-09": 3,
                "2024-04-10": 11,
                "2024-04-11": 9,
                "2024-04-12": 6,
                "2024-04-13": 19,
                "2024-04-14": 21,
                "2024-04-15": 6,
                "2024-04-16": 2,
                "2024-04-17": 9,
                "2024-04-18": 7,
                "2024-04-19": 8,
                "2024-04-20": 4,
                "2024-04-21": 20,
                "2024-04-22": 13,
                "2024-04-23": 1,
                "2024-04-24": 10,
                "2024-04-25": 8,
                "2024-04-26": 15,
                "2024-04-27": 14,
                "2024-04-28": 9,
                "2024-04-29": 12,
                "2024-04-30": 3,
            }.items()
        ],
    )

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
