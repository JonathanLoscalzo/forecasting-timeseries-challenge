from typing import Type

from matplotlib.pylab import Enum

from forecasting.models.core import ForecastModelProtocol
from forecasting.models.prophet import ProphetModel
from forecasting.models.simple_average import SimpleAverageModel


class ModelName(str, Enum):
    simple_average = "simple_average"
    prophet = "prophet"


MODEL_REGISTRY: dict[ModelName | str, Type[ForecastModelProtocol]] = {
    ModelName.simple_average: SimpleAverageModel,
    ModelName.prophet: ProphetModel,
}
