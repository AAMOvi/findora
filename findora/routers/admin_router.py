from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from findora.core.dependencies import require_role
from findora.db.database import get_db
from findora.models.item import Item
from findora.models.user import User
from findora.schemas.category_schema import (
    CategoryCreate,
    CategoryDetailResponse,
    CategoryListResponse,
    CategoryUpdate,
    MessageResponse,
)
from findora.schemas.item_schema import ItemDetailResponse, ItemListResponse
from findora.services.category_service import (
    create_category,
    delete_category,
    get_categories,
    get_category_by_id,
    get_category_by_name,
    update_category,
)
from findora.services.item_service import get_item_by_id, get_items

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/items", response_model=ItemListResponse)
def admin_list_items_endpoint(
    include_deleted: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "moderator")),
):
    query = db.query(Item)

    if not include_deleted:
        query = query.filter(Item.is_deleted.is_(False))

    items = query.order_by(Item.created_at.desc()).all()

    meta = {
        "page": 1,
        "limit": len(items),
        "total": len(items),
        "total_pages": 1 if items else 0,
        "has_next": False,
        "has_prev": False,
    }

    return {
        "success": True,
        "data": items,
        "meta": meta,
    }


@router.patch("/items/{item_id}/resolve", response_model=ItemDetailResponse)
def admin_resolve_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "moderator")),
):
    item = get_item_by_id(db=db, item_id=item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    item.is_resolved = True

    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "success": True,
        "data": item,
    }


@router.delete("/items/{item_id}", response_model=MessageResponse)
def admin_soft_delete_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    item = get_item_by_id(db=db, item_id=item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found.",
        )

    item.is_deleted = True
    item.deleted_at = datetime.now(UTC)

    db.add(item)
    db.commit()

    return {
        "success": True,
        "message": "Item deleted successfully.",
    }


@router.get("/categories", response_model=CategoryListResponse)
def admin_list_categories_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    categories = get_categories(db=db)

    return {
        "success": True,
        "data": categories,
    }


@router.post(
    "/categories",
    response_model=CategoryDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def admin_create_category_endpoint(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    existing_category = get_category_by_name(db=db, name=category_data.name)

    if existing_category is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists.",
        )

    category = create_category(db=db, category_data=category_data)

    return {
        "success": True,
        "data": category,
    }


@router.get("/categories/{category_id}", response_model=CategoryDetailResponse)
def admin_get_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    category = get_category_by_id(db=db, category_id=category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return {
        "success": True,
        "data": category,
    }


@router.patch("/categories/{category_id}", response_model=CategoryDetailResponse)
def admin_update_category_endpoint(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    category = get_category_by_id(db=db, category_id=category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    existing_category = get_category_by_name(db=db, name=category_data.name)

    if existing_category is not None and existing_category.id != category_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists.",
        )

    updated_category = update_category(
        db=db,
        category=category,
        category_data=category_data,
    )

    return {
        "success": True,
        "data": updated_category,
    }


@router.delete("/categories/{category_id}", response_model=MessageResponse)
def admin_delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    category = get_category_by_id(db=db, category_id=category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    delete_category(db=db, category=category)

    return {
        "success": True,
        "message": "Category deleted successfully.",
    }