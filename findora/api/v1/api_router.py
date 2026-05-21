from fastapi import APIRouter

from findora.routers import (
    admin_router,
    auth_router,
    category_router,
    claim_router,
    health_router,
    item_router,
)

api_router = APIRouter()

api_router.include_router(health_router.router)
api_router.include_router(item_router.router)
api_router.include_router(auth_router.router)
api_router.include_router(claim_router.router)
api_router.include_router(category_router.router)
api_router.include_router(admin_router.router)