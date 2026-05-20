from findora.db.seed import DEFAULT_CATEGORIES, seed_categories
from findora.models.category import Category


def test_seed_categories(db_session):
    seed_categories(db_session)

    categories = db_session.query(Category).all()

    assert len(categories) == len(DEFAULT_CATEGORIES)
    assert categories[0].name == "ID Card"


def test_seed_categories_is_idempotent(db_session):
    seed_categories(db_session)
    seed_categories(db_session)

    categories = db_session.query(Category).all()

    assert len(categories) == len(DEFAULT_CATEGORIES)