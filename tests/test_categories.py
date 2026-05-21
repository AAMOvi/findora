from findora.core.security import get_password_hash
from findora.db.seed import seed_categories
from findora.models.user import User


def create_admin_user(db_session):
    admin = User(
        name="Admin User",
        email="admin@example.com",
        password_hash=get_password_hash("password123"),
        role="admin",
        is_active=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)


def login_admin(client):
    client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@example.com",
            "password": "password123",
        },
    )


def test_public_categories_list(client, db_session):
    seed_categories(db_session)

    response = client.get("/api/v1/categories")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert len(body["data"]) == 10


def test_admin_can_create_category(client, db_session):
    create_admin_user(db_session)
    login_admin(client)

    response = client.post(
        "/api/v1/admin/categories",
        json={"name": "Umbrella"},
    )

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True
    assert body["data"]["name"] == "Umbrella"


def test_normal_user_cannot_create_category(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Normal User",
            "email": "user@example.com",
            "password": "password123",
        },
    )

    client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/v1/admin/categories",
        json={"name": "Umbrella"},
    )

    assert response.status_code == 403


def test_admin_can_update_category(client, db_session):
    seed_categories(db_session)
    create_admin_user(db_session)
    login_admin(client)

    response = client.patch(
        "/api/v1/admin/categories/1",
        json={"name": "Student ID Card"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["name"] == "Student ID Card"


def test_admin_can_delete_category(client, db_session):
    create_admin_user(db_session)
    login_admin(client)

    create_response = client.post(
        "/api/v1/admin/categories",
        json={"name": "Temporary Category"},
    )

    category_id = create_response.json()["data"]["id"]

    response = client.delete(f"/api/v1/admin/categories/{category_id}")

    assert response.status_code == 200
    assert response.json()["success"] is True