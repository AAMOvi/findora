from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from findora.core.dependencies import get_current_user
from findora.db.database import get_db
from findora.models.user import User
from findora.schemas.auth_schema import (
    AuthResponse,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
)
from findora.schemas.user_schema import CurrentUserResponse
from findora.services.auth_service import (
    authenticate_user,
    create_user,
    get_user_by_email,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(db=db, email=user_data.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )

    user = create_user(db=db, user_data=user_data)

    return {
        "success": True,
        "data": user,
    }


@router.post("/login", response_model=AuthResponse)
def login_user(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    request.session["user_id"] = user.id

    return {
        "success": True,
        "data": user,
    }


@router.post("/logout", response_model=MessageResponse)
def logout_user(request: Request):
    request.session.clear()

    return {
        "success": True,
        "message": "Logged out successfully.",
    }


@router.get("/me", response_model=CurrentUserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "data": current_user,
    }