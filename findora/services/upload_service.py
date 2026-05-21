from pathlib import Path
import secrets

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from findora.core.config import settings
from findora.models.item_image import ItemImage


CONTENT_TYPE_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def get_allowed_image_types() -> set[str]:
    return {
        content_type.strip()
        for content_type in settings.allowed_image_types.split(",")
        if content_type.strip()
    }


def validate_image_content_type(file: UploadFile) -> None:
    allowed_types = get_allowed_image_types()

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported image type.",
        )


async def read_and_validate_file_size(file: UploadFile) -> bytes:
    file_content = await file.read()
    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024

    if len(file_content) > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded file is too large.",
        )

    return file_content


def generate_safe_filename(content_type: str) -> str:
    extension = CONTENT_TYPE_EXTENSIONS.get(content_type)

    if extension is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported image type.",
        )

    return f"{secrets.token_hex(16)}{extension}"


def save_file(file_content: bytes, filename: str) -> None:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / filename
    file_path.write_bytes(file_content)


async def save_item_image(
    db: Session,
    item_id: int,
    file: UploadFile,
) -> ItemImage:
    validate_image_content_type(file)

    file_content = await read_and_validate_file_size(file)
    safe_filename = generate_safe_filename(file.content_type or "")

    save_file(file_content=file_content, filename=safe_filename)

    item_image = ItemImage(
        item_id=item_id,
        image_filename=safe_filename,
        original_filename=file.filename or "unknown",
        content_type=file.content_type or "unknown",
    )

    db.add(item_image)
    db.commit()
    db.refresh(item_image)

    return item_image