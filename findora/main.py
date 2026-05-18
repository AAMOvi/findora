from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from findora.api.v1.api_router import api_router
from findora.core.config import settings
from findora.routers import page_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    app.mount(
        "/static",
        StaticFiles(directory="findora/static"),
        name="static",
    )

    app.include_router(api_router, prefix="/api/v1")
    app.include_router(page_router.router)

    return app


app = create_app()