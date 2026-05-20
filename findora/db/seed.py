from sqlalchemy.orm import Session

from findora.models.category import Category


DEFAULT_CATEGORIES = [
    "ID Card",
    "Phone",
    "Wallet",
    "Bag",
    "Book",
    "Calculator",
    "Keys",
    "Laptop",
    "Headphone",
    "Others",
]


def seed_categories(db: Session) -> None:
    for category_name in DEFAULT_CATEGORIES:
        existing_category = (
            db.query(Category)
            .filter(Category.name == category_name)
            .first()
        )

        if existing_category:
            continue

        db.add(Category(name=category_name))

    db.commit()