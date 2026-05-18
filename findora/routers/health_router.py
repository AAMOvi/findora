from fastapi import APIRouter

from findora.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "version": settings.app_version,
    }