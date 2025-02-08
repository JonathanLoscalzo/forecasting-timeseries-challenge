from matplotlib.pylab import Enum

from forecasting.models.simple_average import SimpleAverageModel


class ModelName(str, Enum):
    simple_average = "simple_average"


MODEL_REGISTRY = {ModelName.simple_average: SimpleAverageModel}
