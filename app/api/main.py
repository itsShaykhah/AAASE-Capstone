"""FastAPI application factory.

`create_app()` rather than a bare module-level `app` almost everywhere else
so tests can build an isolated instance; the module-level `app` at the
bottom is what `uvicorn app.api.main:app` actually serves.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import campaigns, health
from app.config.settings import get_settings
from app.observability.logging_config import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title="AI Marketing Team API",
        description="Generates a complete marketing campaign from a product brief.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(campaigns.router)

    return app


app = create_app()
