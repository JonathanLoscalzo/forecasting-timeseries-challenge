from typing import Optional, Type

from forecasting.models.const import MODEL_REGISTRY, ModelName
from forecasting.models.core import ForecastModelProtocol


class ForecastModelFactory:
    model: ForecastModelProtocol

    def __init__(self, registry: dict[ModelName | str, Type[ForecastModelProtocol]] = None):
        self.registry = registry if registry is not None else MODEL_REGISTRY

    def create(self, model: Optional[ModelName | str], **config) -> ForecastModelProtocol:
        return self.registry[model or ModelName.simple_average](**config)
