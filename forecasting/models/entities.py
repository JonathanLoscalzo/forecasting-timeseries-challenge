from datetime import datetime

from pydantic import BaseModel


class Item(BaseModel):
    date: datetime
    value: float | None


class Data(BaseModel):
    historical: list[Item]
    start_date: datetime
    horizon: int = 7

    @classmethod
    def load_from_dict(cls, dct):
        return Data(
            horizon=dct["horizon"],
            start_date=datetime.fromisoformat(dct.get("start_date")),
            historical=[Item(date=datetime.fromisoformat(d), value=v) for d, v in dct.get("historical").items()],
        )
