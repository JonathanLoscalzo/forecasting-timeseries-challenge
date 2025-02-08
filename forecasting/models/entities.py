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

    @classmethod
    def load_from_dict(cls, dct):
        return Data(
            horizon=dct["horizon"],
            start_date=date.fromisoformat(dct.get("start_date")),
            historical=[Item(date=date.fromisoformat(d), value=v) for d, v in dct.get("historical").items()],
        )
