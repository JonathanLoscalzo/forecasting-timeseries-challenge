from datetime import date

from pydantic import BaseModel


class Item(BaseModel):
    date: date
    value: float | None


class Data(BaseModel):
    historical: list[Item]
    start_date: date
    horizon: int = 7

    @classmethod
    def load_from_dict(cls, dct):
        return Data(
            horizon=dct["horizon"],
            start_date=date.fromisoformat(dct.get("start_date")),
            historical=[Item(date=date.fromisoformat(d), value=v) for d, v in dct.get("historical").items()],
        )
