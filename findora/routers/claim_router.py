from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from findora.core.dependencies import get_current_user, require_role
from findora.db.database import get_db
from findora.models.user import User
from findora.schemas.claim_schema import (
    ClaimCreate,
    ClaimDetailResponse,
    ClaimListResponse,
    ClaimStatusUpdate,
)
from findora.services.claim_service import (
    create_claim,
    get_claim_by_id,
    get_claims_for_user,
    update_claim_status,
)
from findora.services.item_service import get_item_by_id

router = APIRouter(tags=["Claims"])


@router.post(
    "/items/{item_id}/claims",
    response_model=ClaimDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_claim_endpoint(
    item_id: int,
    claim_data: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = get_item_by_id(db=db, item_id=item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    claim = create_claim(
        db=db,
        item_id=item_id,
        claimer_user_id=current_user.id,
        claim_data=claim_data,
    )

    return {
        "success": True,
        "data": claim,
    }


@router.get("/claims", response_model=ClaimListResponse)
def list_my_claims_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claims = get_claims_for_user(db=db, user_id=current_user.id)

    return {
        "success": True,
        "data": claims,
    }


@router.get("/claims/{claim_id}", response_model=ClaimDetailResponse)
def get_claim_detail_endpoint(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = get_claim_by_id(db=db, claim_id=claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found.",
        )

    if claim.claimer_user_id != current_user.id and current_user.role not in {
        "admin",
        "moderator",
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied.",
        )

    return {
        "success": True,
        "data": claim,
    }


@router.patch(
    "/claims/{claim_id}/status",
    response_model=ClaimDetailResponse,
)
def update_claim_status_endpoint(
    claim_id: int,
    status_data: ClaimStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "moderator")),
):
    claim = get_claim_by_id(db=db, claim_id=claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found.",
        )

    updated_claim = update_claim_status(
        db=db,
        claim=claim,
        new_status=status_data.status,
    )

    return {
        "success": True,
        "data": updated_claim,
    }