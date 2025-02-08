from dependency_injector import containers, providers

from forecasting.infra.fastapi.dependencies import InferenceService
from forecasting.models.const import MODEL_REGISTRY
from forecasting.models.factories import ForecastModelFactory


class ApiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "forecasting.infra.fastapi.routers.inference",
        ]
    )

    # config = providers.Configuration(yaml_files=["config.yml"])
    model_factory = providers.Factory(
        ForecastModelFactory,
        registry=MODEL_REGISTRY,
    )
    inference_service = providers.Factory(
        InferenceService,
        model_factory=model_factory,
    )
