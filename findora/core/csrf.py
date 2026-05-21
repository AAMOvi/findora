import secrets

from fastapi import HTTPException, Request, status


CSRF_SESSION_KEY = "csrf_token"


def generate_csrf_token(request: Request) -> str:
    token = secrets.token_urlsafe(32)
    request.session[CSRF_SESSION_KEY] = token

    return token


def validate_csrf_token(request: Request, submitted_token: str) -> None:
    session_token = request.session.get(CSRF_SESSION_KEY)

    if not session_token or not submitted_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing CSRF token.",
        )

    if not secrets.compare_digest(session_token, submitted_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid CSRF token.",
        )