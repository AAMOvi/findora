"""
CSRF protection utilities.

Final implementation will use manual session-based CSRF tokens with
secrets.token_urlsafe().
"""


def generate_csrf_token():
    raise NotImplementedError("CSRF token generation will be implemented in auth module.")


def validate_csrf_token():
    raise NotImplementedError("CSRF token validation will be implemented in auth module.")