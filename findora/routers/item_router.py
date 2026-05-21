from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from findora.db.database import get_db
from findora.schemas.item_schema import (
    ItemCreate,
    ItemDetailResponse,
    ItemListResponse,
)
from findora.services.item_service import create_item, get_item_by_id, get_items

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("", response_model=ItemDetailResponse, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(
    item_data: ItemCreate,
    db: Session = Depends(get_db),
):
    item = create_item(db=db, item_data=item_data)

    return {
        "success": True,
        "data": item,
    }


@router.get("", response_model=ItemListResponse)
def list_items_endpoint(
    q: str | None = None,
    status: Literal["lost", "found"] | None = None,
    category_id: int | None = None,
    location: str | None = None,
    resolved: bool | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    sort: Literal["newest", "oldest"] = "newest",
    db: Session = Depends(get_db),
):
    items, meta = get_items(
        db=db,
        q=q,
        status=status,
        category_id=category_id,
        location=location,
        resolved=resolved,
        page=page,
        limit=limit,
        sort=sort,
    )

    return {
        "success": True,
        "data": items,
        "meta": meta,
    }


@router.get("/{item_id}", response_model=ItemDetailResponse)
def get_item_detail_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = get_item_by_id(db=db, item_id=item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    return {
        "success": True,
        "data": item,
    }