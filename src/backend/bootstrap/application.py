from fastapi import FastAPI

from backend.presentation.http.routers.health import router as health_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="Backend Starter",
        version="0.1.0",
    )

    application.include_router(health_router)

    return application