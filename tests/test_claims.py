from findora.db.seed import seed_categories
from findora.models.user import User
from findora.core.security import get_password_hash


def register_and_login(client, email="user@example.com"):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
        },
    )

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


def test_submit_claim_requires_login(client, db_session):
    item_id = create_test_item(client, db_session)

    response = client.post(
        f"/api/v1/items/{item_id}/claims",
        json={
            "message": "This wallet belongs to me.",
            "proof_text": "My ID card is inside it.",
        },
    )

    assert response.status_code == 401


def test_submit_claim(client, db_session):
    register_and_login(client)
    item_id = create_test_item(client, db_session)

    response = client.post(
        f"/api/v1/items/{item_id}/claims",
        json={
            "message": "This wallet belongs to me.",
            "proof_text": "My ID card is inside it.",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True
    assert body["data"]["item_id"] == item_id
    assert body["data"]["status"] == "pending"


def test_list_my_claims(client, db_session):
    register_and_login(client)
    item_id = create_test_item(client, db_session)

    client.post(
        f"/api/v1/items/{item_id}/claims",
        json={
            "message": "This wallet belongs to me.",
            "proof_text": "My ID card is inside it.",
        },
    )

    response = client.get("/api/v1/claims")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert len(body["data"]) == 1


def test_get_claim_detail(client, db_session):
    register_and_login(client)
    item_id = create_test_item(client, db_session)

    create_response = client.post(
        f"/api/v1/items/{item_id}/claims",
        json={
            "message": "This wallet belongs to me.",
            "proof_text": "My ID card is inside it.",
        },
    )

    claim_id = create_response.json()["data"]["id"]

    response = client.get(f"/api/v1/claims/{claim_id}")

    assert response.status_code == 200
    assert response.json()["data"]["id"] == claim_id


def test_normal_user_cannot_update_claim_status(client, db_session):
    register_and_login(client)
    item_id = create_test_item(client, db_session)

    create_response = client.post(
        f"/api/v1/items/{item_id}/claims",
        json={
            "message": "This wallet belongs to me.",
            "proof_text": "My ID card is inside it.",
        },
    )

    claim_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/api/v1/claims/{claim_id}/status",
        json={"status": "accepted"},
    )

    assert response.status_code == 403


def test_admin_can_update_claim_status(client, db_session):
    register_and_login(client)
    item_id = create_test_item(client, db_session)

    create_response = client.post(
        f"/api/v1/items/{item_id}/claims",
        json={
            "message": "This wallet belongs to me.",
            "proof_text": "My ID card is inside it.",
        },
    )

    claim_id = create_response.json()["data"]["id"]

    client.post("/api/v1/auth/logout")
    create_admin_user(db_session)
    login_admin(client)

    response = client.patch(
        f"/api/v1/claims/{claim_id}/status",
        json={"status": "accepted"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["status"] == "accepted"