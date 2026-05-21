from datetime import datetime

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class CategoryListResponse(BaseModel):
    success: bool = True
    data: list[CategoryResponse]


class CategoryDetailResponse(BaseModel):
    success: bool = True
    data: CategoryResponse


class MessageResponse(BaseModel):
    success: bool = True
    message: str