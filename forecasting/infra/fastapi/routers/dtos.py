from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field

from forecasting.const import EXAMPLE_INPUT


class Item(BaseModel):
    date: datetime
    value: float | None = Field(ge=0.0)


class Data(BaseModel):
    historical: Dict[datetime, float]
    start_date: datetime = Field(...)
    horizon: int = Field(default=7, gt=0)
    n_weeks: int = Field(default=4, gt=0)
    frequency: str = Field(default="daily")

    model_config = {"json_schema_extra": {"examples": [EXAMPLE_INPUT]}}
