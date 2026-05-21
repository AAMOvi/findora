from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.sessions import SessionMiddleware

from findora.api.v1.api_router import api_router
from findora.core.config import settings
from findora.core.exceptions import (
    http_exception_handler,
    internal_server_error_handler,
    not_found_exception_handler,
    rate_limit_exception_handler,
    validation_exception_handler,
)
from findora.core.rate_limit import limiter
from findora.routers import media_router, page_router

app = FastAPI(title=settings.app_name)

app.state.limiter = limiter

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie=settings.session_cookie_name,
    https_only=False,
)

app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

app.add_exception_handler(500, internal_server_error_handler)

app.include_router(page_router.router)
app.include_router(api_router, prefix="/api/v1")
app.include_router(media_router.router)