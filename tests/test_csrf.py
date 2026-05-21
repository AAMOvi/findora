import pytest
from fastapi import HTTPException

from findora.core.csrf import generate_csrf_token, validate_csrf_token


class FakeRequest:
    def __init__(self):
        self.session = {}


def test_generate_csrf_token_stores_token_in_session():
    request = FakeRequest()

    token = generate_csrf_token(request)

    assert token
    assert request.session["csrf_token"] == token


def test_validate_csrf_token_accepts_valid_token():
    request = FakeRequest()

    token = generate_csrf_token(request)

    validate_csrf_token(request, token)


def test_validate_csrf_token_rejects_missing_token():
    request = FakeRequest()

    with pytest.raises(HTTPException) as exc_info:
        validate_csrf_token(request, "")

    assert exc_info.value.status_code == 403


def test_validate_csrf_token_rejects_invalid_token():
    request = FakeRequest()

    generate_csrf_token(request)

    with pytest.raises(HTTPException) as exc_info:
        validate_csrf_token(request, "wrong-token")

    assert exc_info.value.status_code == 403