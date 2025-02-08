from typing import Optional

from forecasting.infra.fastapi.routers.dtos import Data as DataInput
from forecasting.infra.fastapi.routers.dtos import Item as DataOutput
from forecasting.models.const import ModelName
from forecasting.models.entities import Data
from forecasting.models.factories import ForecastModelFactory


class InferenceService:
    def __init__(self, model_factory: ForecastModelFactory):
        self.model_factory = model_factory

    def forecast(self, data: DataInput, model_name: Optional[ModelName] = None) -> list[DataOutput]:
        interim = data.model_dump()
        historical = interim["historical"].copy()
        del interim["historical"]
        features = Data(
            **interim,
            historical=[{"date": dt, "value": value} for dt, value in historical.items()],  # type: ignore
        )
        result = self.model_factory.create(model_name).forecast(data=features)
        return [DataOutput(**item.model_dump()) for item in result]
