from fastapi import FastAPI

from backend.config.settings import Settings
from backend.presentation.http.routers.health import router as health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings if settings is not None else Settings()

    application = FastAPI(
        title=app_settings.name,
        version=app_settings.version,
        debug=app_settings.debug,
    )

    application.include_router(health_router)

    return application