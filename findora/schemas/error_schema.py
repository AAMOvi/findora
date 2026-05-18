from pydantic import BaseModel

class ErrorDetail(BaseModel):
    code: int
    message: str
    details: str | None = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail