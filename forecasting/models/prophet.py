import pandas as pd
from loguru import logger
from prophet import Prophet

from forecasting.models.core import ForecastModel
from forecasting.models.entities import Data
from forecasting.models.entities import Item as Prediction


class ProphetModel(ForecastModel):
    def __init__(self):
        pass

    def forecast(self, data: Data) -> list[Prediction]:
        """
        Generate a forecast of predicted values over a specified date range using Prophet.

        Args:
            data (Data): An object containing historical data and forecast parameters.

        Returns:
            List[Prediction]: A list of predicted values with corresponding dates.
        """
        logger.info("Generating forecast using Prophet Model")

        # Prepare the data for Prophet
        df = pd.DataFrame([item.model_dump() for item in data.historical])
        df["date"] = pd.to_datetime(df.date)
        df["value"] = df.value.astype("float64")

        # Prophet expects columns "ds" for dates and "y" for values
        df_prophet = df.rename(columns={"date": "ds", "value": "y"})

        # Initialize the Prophet model
        model = Prophet()
        model.fit(df_prophet)
        # TODO: replace prophet logging with loguru

        # Calculate the number of days between the last historical date and the start date
        last_historical_date = df["date"].max()
        days_gap = (pd.to_datetime(data.start_date) - last_historical_date).days

        # Calculate the total number of periods to predict (gap + horizon)
        total_periods = days_gap + data.horizon - 1

        # Create a DataFrame for future dates
        future = model.make_future_dataframe(periods=total_periods, freq="D")

        # Forecast the future
        forecast = model.predict(future)

        # Extract the relevant prediction columns (date and predicted value)
        forecast_results = forecast[["ds", "yhat"]][-(data.horizon) :]  # noqa: E203

        # Prepare the predictions as a list of Prediction objects
        predictions = [Prediction(date=row[0], value=row[1]) for row in forecast_results.values]

        logger.info("Forecast generated successfully")
        return predictions
