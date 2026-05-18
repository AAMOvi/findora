"""
Shared FastAPI dependencies.

This file will contain authentication and RBAC dependencies.
"""


def get_current_user():
    """
    Return currently authenticated user.

    Raise 401 if not logged in.
    """
    raise NotImplementedError("Authentication will be implemented later.")


def require_role(*allowed_roles: str):
    """
    Require one of the allowed roles.

    Example:
        current_user = Depends(require_role("admin"))
        current_user = Depends(require_role("admin", "moderator"))
    """

    def dependency():
        raise NotImplementedError("RBAC will be implemented later.")

    return dependency


def get_current_admin():
    """
    Shortcut dependency for admin-only routes.
    """
    raise NotImplementedError("Admin dependency will be implemented later.")