"""App handlers."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog import get_logger

from shulker_box.api import router
from shulker_box.database.client import init_database
from shulker_box.handlers import EXCEPTION_HANDLERS
from shulker_box.settings import settings

log = get_logger(__name__)


def create_application() -> FastAPI:
    """Create the FastAPI application.

    Returns:
        FastAPI: created app.
    """
    log.info("Creating app...")
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url="/api/docs",
        on_startup=[init_database],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
    )
    app.include_router(router.api_router)
    app.exception_handlers = dict(EXCEPTION_HANDLERS)
    app.middleware_stack = app.build_middleware_stack()
    return app


app = create_application()
