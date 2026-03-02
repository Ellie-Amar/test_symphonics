from __future__ import annotations
from fastapi import FastAPI

from app.config.settings import settings
from app.interface.routes.event_route import router as event_router
from app.interface.routes.health_route import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.include_router(health_router)
    app.include_router(event_router)

    return app


app = create_app()
