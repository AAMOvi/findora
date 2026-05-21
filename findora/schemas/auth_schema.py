from pydantic import BaseModel, Field

from findora.schemas.user_schema import UserResponse


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    department: str | None = Field(default=None, max_length=100)
    student_id: str | None = Field(default=None, max_length=50)


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class AuthResponse(BaseModel):
    success: bool = True
    data: UserResponse


class MessageResponse(BaseModel):
    success: bool = True
    message: str