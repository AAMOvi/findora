from fastapi import APIRouter

from findora.routers import health_router, item_router

api_router = APIRouter()

api_router.include_router(health_router.router)
api_router.include_router(item_router.router)