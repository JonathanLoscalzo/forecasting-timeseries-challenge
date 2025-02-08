import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from forecasting.const import EXAMPLE_INPUT
from forecasting.models.simple_average import SimpleAverageModel
from forecasting.models.entities import Data

# Streamlit UI Title
st.title("📈 Forecasting App")

# File uploader
uploaded_file = st.file_uploader("Upload a JSON file", type="json")


if uploaded_file is not None:
    data = json.load(uploaded_file)
else:
    data = EXAMPLE_INPUT

historical_data = data["historical"]
start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
horizon = data["horizon"]

# Convert historical data to DataFrame
historical_df = pd.DataFrame(list(historical_data.items()), columns=["date", "value"])
historical_df["date"] = pd.to_datetime(historical_df["date"])
historical_df.sort_values("date", inplace=True)

model = SimpleAverageModel()

predictions = model.forecast(Data.load_from_dict({**data, "horizon": 20}))

# Convert predictions to DataFrame
forecast_df = pd.DataFrame([(pred.date, pred.value) for pred in predictions], columns=["date", "value"])
forecast_df["date"] = pd.to_datetime(forecast_df["date"])

# Plot the results
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(historical_df["date"], historical_df["value"], color="blue", label="Historical Data")
ax.plot(
    forecast_df["date"],
    forecast_df["value"],
    color="red",
    linestyle="dashed",
    label="Forecast",
)

# Labels and legend
ax.set_xlabel("Date")
ax.set_ylabel("Value")
ax.set_title("Forecasting Results")
ax.legend()

# Display plot
st.pyplot(fig)


def init():
    import sys
    from streamlit.web import cli as stcli

    sys.argv = ["", "run", "forecasting/clients/streamlit.py"]
    sys.exit(stcli.main())
