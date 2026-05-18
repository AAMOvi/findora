"""
Security utilities for authentication and authorization.

Initial strategy:
- Jinja2 web app will use session/cookie-based authentication.
- Passwords will be hashed using passlib/bcrypt.
- JWT may be added later if a separate React/Next.js frontend is introduced.
"""


def get_password_hash(password: str) -> str:
    raise NotImplementedError("Password hashing will be implemented in auth module.")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    raise NotImplementedError("Password verification will be implemented in auth module.")