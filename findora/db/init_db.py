from findora.db.database import SessionLocal
from findora.db.seed import seed_categories


def init_db() -> None:
    db = SessionLocal()

    try:
        seed_categories(db)
        print("Database seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()