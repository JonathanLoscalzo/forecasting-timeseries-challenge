from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from forecasting.infra.fastapi.dependencies import InferenceService
from forecasting.infra.fastapi.routers.dtos import Data, Item
from forecasting.infra.injector import ApiContainer
from forecasting.models.const import ModelName

router = APIRouter()


@router.post("/forecast/", tags=["inference"], response_model=list[Item])
@inject
async def forecast(
    data: Data,
    model_name: ModelName = ModelName.simple_average,
    inference_service: InferenceService = Depends(Provide[ApiContainer.inference_service]),
):
    return inference_service.forecast(data, model_name=model_name)
