"""V1 API router."""

from fastapi.routing import APIRouter

from shulker_box.api.v1.items import routes

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(routes.router)
