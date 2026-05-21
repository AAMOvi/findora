from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from findora.db.database import get_db
from findora.schemas.category_schema import CategoryListResponse
from findora.services.category_service import get_categories

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=CategoryListResponse)
def list_categories_endpoint(db: Session = Depends(get_db)):
    categories = get_categories(db=db)

    return {
        "success": True,
        "data": categories,
    }