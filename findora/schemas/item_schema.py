from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


ItemStatusLiteral = Literal["lost", "found"]


class ItemCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str = Field(min_length=5)
    status: ItemStatusLiteral
    category_id: int
    location: str = Field(min_length=2, max_length=150)
    date_lost_or_found: date | None = None


class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    category_id: int
    location: str
    date_lost_or_found: date | None
    posted_by_user_id: int | None
    is_resolved: bool
    is_deleted: bool
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ItemListResponse(BaseModel):
    success: bool = True
    data: list[ItemResponse]
    meta: dict


class ItemDetailResponse(BaseModel):
    success: bool = True
    data: ItemResponse