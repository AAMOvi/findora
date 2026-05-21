from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department: str | None
    student_id: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class CurrentUserResponse(BaseModel):
    success: bool = True
    data: UserResponse