from pydantic import BaseModel
from datetime import date
from typing import List


class Item(BaseModel):
    date: date
    value: float


class Data(BaseModel):
    historical: List[Item]
    start_date: date
    horizon: int = 7
