from math import ceil

from sqlalchemy import or_
from sqlalchemy.orm import Session

from findora.models.item import Item
from findora.schemas.item_schema import ItemCreate


def create_item(db: Session, item_data: ItemCreate) -> Item:
    item = Item(**item_data.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_item_by_id(db: Session, item_id: int) -> Item | None:
    return (
        db.query(Item)
        .filter(Item.id == item_id, Item.is_deleted.is_(False))
        .first()
    )


def get_items(
    db: Session,
    q: str | None = None,
    status: str | None = None,
    category_id: int | None = None,
    location: str | None = None,
    resolved: bool | None = None,
    page: int = 1,
    limit: int = 20,
    sort: str = "newest",
) -> tuple[list[Item], dict]:
    page = max(page, 1)
    limit = min(max(limit, 1), 100)

    query = db.query(Item).filter(Item.is_deleted.is_(False))

    if q:
        search_value = f"%{q}%"
        query = query.filter(
            or_(
                Item.title.ilike(search_value),
                Item.description.ilike(search_value),
                Item.location.ilike(search_value),
            )
        )

    if status:
        query = query.filter(Item.status == status)

    if category_id:
        query = query.filter(Item.category_id == category_id)

    if location:
        query = query.filter(Item.location.ilike(f"%{location}%"))

    if resolved is not None:
        query = query.filter(Item.is_resolved.is_(resolved))

    total = query.count()

    if sort == "oldest":
        query = query.order_by(Item.created_at.asc())
    else:
        query = query.order_by(Item.created_at.desc())

    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    total_pages = ceil(total / limit) if total else 0

    meta = {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }

    return items, meta