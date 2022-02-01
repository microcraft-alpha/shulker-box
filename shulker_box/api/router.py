"""API router."""

from fastapi import APIRouter

from shulker_box.api.v1 import router

api_router = APIRouter(prefix="/api")
api_router.include_router(router.v1_router)
