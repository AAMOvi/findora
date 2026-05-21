from sqlalchemy.orm import Session

from findora.models.category import Category
from findora.schemas.category_schema import CategoryCreate, CategoryUpdate


def get_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name.asc()).all()


def get_category_by_id(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, name: str) -> Category | None:
    return db.query(Category).filter(Category.name == name).first()


def create_category(db: Session, category_data: CategoryCreate) -> Category:
    category = Category(name=category_data.name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def update_category(
    db: Session,
    category: Category,
    category_data: CategoryUpdate,
) -> Category:
    category.name = category_data.name

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()