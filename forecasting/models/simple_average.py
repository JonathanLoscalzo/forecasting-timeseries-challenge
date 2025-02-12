from datetime import timedelta

import numpy as np
import pandas as pd
from loguru import logger

from forecasting.models.core import ForecastModel
from forecasting.models.entities import Data
from forecasting.models.entities import Item as Prediction


class SimpleAverageModel(ForecastModel):
    def __init__(self, weeks: int = 4, frequency="daily"):
        self.weeks = weeks
        self.frequency = frequency

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

        gap_dates = pd.date_range(
            start=df.iloc[-1].date.date() + timedelta(days=1),
            end=data.start_date,
            freq="d" if self.frequency == "daily" else "h",
            inclusive="left",
        )
        prediction_dates = pd.date_range(
            start=data.start_date,
            periods=data.horizon,
            freq="d" if self.frequency == "daily" else "h",
        )
        # concat the dates we must predict
        df = pd.concat(
            [
                df,
                pd.DataFrame.from_dict({"date": np.concat([gap_dates, prediction_dates]), "value": 0}),
            ]
        ).sort_values("date", ascending=True)

        initial_point = gap_dates.size + prediction_dates.size
        for idx in range(initial_point, 0, -1):
            weekday = df.iloc[-idx].date.weekday()
            hour = df.iloc[-idx].date.hour

            if self.frequency == "daily":
                filter_mask = (df.date < df.iloc[-idx].date) & (df.date.dt.weekday == weekday)
            else:
                filter_mask = (
                    (df.date < df.iloc[-idx].date) & (df.date.dt.weekday == weekday) & (df.date.dt.hour == hour)
                )

            # group by the weekday (or hourly) and filters the last four entries before current date
            value = df[filter_mask][-self.weeks :].value.mean()
            # update value, it will be used if the horizon is further out
            df.iloc[-idx, 1] = value  # if data is not valid, some values could be NaN

        logger.info("Forecast generated successfully")

        return [
            Prediction(date=item.get("date", None), value=item.get("value", 0.0))
            for item in df[df.date >= prediction_dates[0]].replace({np.nan: None}).to_dict(orient="records")
        ][-prediction_dates.size :]
