from abc import ABC, abstractmethod
from typing import Protocol

from forecasting.models.entities import Data
from forecasting.models.entities import Item as Prediction


class ForecastModel(ABC):
    @abstractmethod
    def forecast(self, data: Data) -> list[Prediction]: ...


class ForecastModelProtocol(Protocol):
    def forecast(self, data: Data) -> list[Prediction]: ...
