from pathlib import Path

from fastapi import HTTPException, status

from findora.core.config import settings


def get_media_file_path(filename: str) -> Path:
    if Path(filename).name != filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename.",
        )

    file_path = Path(settings.upload_dir) / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media file not found.",
        )

    return file_path