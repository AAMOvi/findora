from fastapi import Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded


def error_response(
    status_code: int,
    message: str,
    details: object | None = None,
) -> JSONResponse:
    content: dict[str, object] = {
        "success": False,
        "error": {
            "message": message,
        },
    }

    if details is not None:
        content["error"]["details"] = details

    return JSONResponse(
        status_code=status_code,
        content=content,
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    message = str(exc.detail)

    if exc.status_code == status.HTTP_404_NOT_FOUND and message == "Not Found":
        message = "Route not found."

    return error_response(
        status_code=exc.status_code,
        message=message,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation error.",
        details=exc.errors(),
    )


async def rate_limit_exception_handler(
    request: Request,
    exc: RateLimitExceeded,
) -> JSONResponse:
    return error_response(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        message="Too many requests. Please try again later.",
    )


async def not_found_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        message="Route not found.",
    )


async def internal_server_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Internal server error.",
    )