from fastapi import APIRouter
from fastapi.responses import FileResponse

from findora.services.media_service import get_media_file_path

router = APIRouter(prefix="/media", tags=["Media"])


@router.get("/{filename}")
def serve_media_file(filename: str):
    file_path = get_media_file_path(filename)

    return FileResponse(file_path)