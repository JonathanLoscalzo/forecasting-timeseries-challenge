import numpy as np
import pandas as pd
from loguru import logger

from forecasting.models.core import ForecastModel
from forecasting.models.entities import Data
from forecasting.models.entities import Item as Prediction


class SimpleAverageModel(ForecastModel):
    def __init__(self):
        pass

    def forecast(self, data: Data) -> list[Prediction]:
        """
        Generate a forecast of predicted values over a specified date range.

        The method will forecast the values starting from the given `start_date`
        and for a range defined by the `horizon`. The forecasted range will
        include the `start_date` and extend for the number of days specified in
        `horizon`, which is inclusive of the start and end dates.

        Args:
            data (Data): An object containing historical data and forecast parameters.

        Returns:
            List[Prediction]: A list of predicted values with corresponding dates.
        """
        logger.info("Generating forecast using Simple Average Model")
        # Creates a dataframe with the current values
        df = pd.DataFrame([item.model_dump() for item in data.historical])
        df.date = pd.to_datetime(df.date)
        df.value = df.value.astype("float64")

        prediction_dates = pd.date_range(
            data.start_date,
            periods=data.horizon,
            freq="d",
        )
        # concat the dates we must predict
        df = pd.concat(
            [
                df,
                pd.DataFrame.from_dict({"date": prediction_dates, "value": 0}),
            ]
        ).sort_values("date", ascending=True)

        for idx in range(data.horizon, 0, -1):
            weekday = df.iloc[-idx].date.weekday()
            # group by the weekday and filters the last four entries before current date
            value = df[(df.date < df.iloc[-idx].date) & (df.date.dt.weekday == weekday)][-5:].value.mean()
            # update value, it will be used if the horizon is further out
            df.iloc[-idx, 1] = value  # if data is not valid, some values could be NaN

        logger.info("Forecast generated successfully")

        return [
            Prediction(date=item.get("date", None), value=item.get("value", 0.0))
            for item in df[df.date >= prediction_dates[0]].replace({np.nan: None}).to_dict(orient="records")
        ]
