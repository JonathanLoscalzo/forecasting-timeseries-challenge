from datetime import date
from typing import Dict

from pydantic import BaseModel, Field

from forecasting.const import EXAMPLE_INPUT


class Item(BaseModel):
    date: date
    value: float | None = Field(ge=0.0)


class Data(BaseModel):
    historical: Dict[date, float]
    start_date: date = Field(...)
    horizon: int = Field(default=7, gt=0)

    model_config = {"json_schema_extra": {"examples": [EXAMPLE_INPUT]}}
