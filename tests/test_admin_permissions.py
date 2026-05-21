from findora.core.security import get_password_hash
from findora.db.seed import seed_categories
from findora.models.user import User


def create_user_with_role(db_session, role: str, email: str):
    user = User(
        name=f"{role.title()} User",
        email=email,
        password_hash=get_password_hash("password123"),
        role=role,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def login(client, email: str):
    client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "password123",
        },
    )


def create_test_item(client, db_session) -> int:
    seed_categories(db_session)

    response = client.post(
        "/api/v1/items",
        json={
            "title": "Lost Wallet",
            "description": "Black wallet near library.",
            "status": "lost",
            "category_id": 3,
            "location": "Library",
        },
    )

    return response.json()["data"]["id"]


def test_admin_items_requires_login(client):
    response = client.get("/api/v1/admin/items")

    assert response.status_code == 401


def test_normal_user_cannot_access_admin_items(client, db_session):
    create_user_with_role(db_session, "user", "user@example.com")
    login(client, "user@example.com")

    response = client.get("/api/v1/admin/items")

    assert response.status_code == 403


def test_moderator_can_access_admin_items(client, db_session):
    create_user_with_role(db_session, "moderator", "mod@example.com")
    login(client, "mod@example.com")

    response = client.get("/api/v1/admin/items")

    assert response.status_code == 200


def test_admin_can_mark_item_resolved(client, db_session):
    item_id = create_test_item(client, db_session)

    create_user_with_role(db_session, "admin", "admin@example.com")
    login(client, "admin@example.com")

    response = client.patch(f"/api/v1/admin/items/{item_id}/resolve")

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["is_resolved"] is True


def test_moderator_can_mark_item_resolved(client, db_session):
    item_id = create_test_item(client, db_session)

    create_user_with_role(db_session, "moderator", "mod@example.com")
    login(client, "mod@example.com")

    response = client.patch(f"/api/v1/admin/items/{item_id}/resolve")

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["is_resolved"] is True


def test_moderator_cannot_delete_item(client, db_session):
    item_id = create_test_item(client, db_session)

    create_user_with_role(db_session, "moderator", "mod@example.com")
    login(client, "mod@example.com")

    response = client.delete(f"/api/v1/admin/items/{item_id}")

    assert response.status_code == 403


def test_admin_can_soft_delete_item(client, db_session):
    item_id = create_test_item(client, db_session)

    create_user_with_role(db_session, "admin", "admin@example.com")
    login(client, "admin@example.com")

    response = client.delete(f"/api/v1/admin/items/{item_id}")

    assert response.status_code == 200

    list_response = client.get("/api/v1/items")

    assert list_response.status_code == 200
    assert list_response.json()["meta"]["total"] == 0