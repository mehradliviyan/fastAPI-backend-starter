from fastapi import FastAPI

from backend.config.settings import Settings
from backend.presentation.http.routers.health import router as health_router
from backend.presentation.http.errors.handlers import register_exception_handlers
from backend.infrastructure.logging.configuration import configure_logging
import logging

logger = logging.getLogger(__name__)

def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings if settings is not None else Settings()


    configure_logging(app_settings)
    application = FastAPI(
        title=app_settings.name,
        version=app_settings.version,
        debug=app_settings.debug,
    )

    register_exception_handlers(application)
    application.include_router(health_router)
    
    logger.info(
        "Application initialized in %s environment",
        app_settings.environment.value,
        extra={
            "environment": app_settings.environment.value,
        },
    )

    return application