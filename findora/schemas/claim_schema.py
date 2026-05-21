from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


ClaimStatusLiteral = Literal["pending", "accepted", "rejected"]


class ClaimCreate(BaseModel):
    message: str = Field(min_length=5)
    proof_text: str | None = None


class ClaimStatusUpdate(BaseModel):
    status: Literal["accepted", "rejected"]


class ClaimResponse(BaseModel):
    id: int
    item_id: int
    claimer_user_id: int
    message: str
    proof_text: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ClaimDetailResponse(BaseModel):
    success: bool = True
    data: ClaimResponse


class ClaimListResponse(BaseModel):
    success: bool = True
    data: list[ClaimResponse]