from datetime import datetime

from pydantic import BaseModel


class ItemImageResponse(BaseModel):
    id: int
    item_id: int
    image_filename: str
    original_filename: str
    content_type: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ItemImageUploadResponse(BaseModel):
    success: bool = True
    data: ItemImageResponse