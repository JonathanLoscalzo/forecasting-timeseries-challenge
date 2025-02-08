from abc import ABC, abstractmethod
from typing import List, Protocol

from forecasting.models.entities import Data, Item as Prediction


class ForecastModel(ABC):
    @abstractmethod
    def forecast(self, data: Data) -> List[Prediction]: ...


class ForecastModelProtocol(Protocol):
    def forecast(self, data: Data) -> List[Prediction]: ...
