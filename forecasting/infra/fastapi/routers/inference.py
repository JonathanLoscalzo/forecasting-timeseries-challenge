from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel, Field

from forecasting.models.const import ModelName

router = APIRouter()


class Item(BaseModel):
    date: date
    value: float = Field(gt=0)


class Data(BaseModel):
    historical: list[Item]
    start_date: date
    horizon: int = Field(default=7, gt=0)


@router.post("/forecast/", tags=["inference"])
async def forecast(data: Data, model_name: ModelName = ModelName.simple_average):
    print(data)
    print(model_name)
    return [{"username": "Rick"}, {"username": "Morty"}]
