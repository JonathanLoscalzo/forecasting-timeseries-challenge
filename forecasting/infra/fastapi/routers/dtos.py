from datetime import date
from typing import Dict

from pydantic import BaseModel, Field


class Item(BaseModel):
    date: date
    value: float | None = Field(ge=0.0)


class Data(BaseModel):
    historical: Dict[date, float]
    start_date: date = Field(...)
    horizon: int = Field(default=7, gt=0)
