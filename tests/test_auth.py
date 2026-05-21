def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "department": "CSE",
            "student_id": "2026001",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True
    assert body["data"]["name"] == "Test User"
    assert body["data"]["email"] == "test@example.com"
    assert body["data"]["role"] == "user"
    assert "password_hash" not in body["data"]


def test_register_duplicate_email_returns_409(client):
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "department": "CSE",
        "student_id": "2026001",
    }

    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409


def test_login_user(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["email"] == "test@example.com"


def test_login_invalid_credentials_returns_401(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 401


def test_get_me_requires_login(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_get_me_after_login(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["email"] == "test@example.com"


def test_logout_user(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    logout_response = client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 200

    me_response = client.get("/api/v1/auth/me")
    assert me_response.status_code == 401