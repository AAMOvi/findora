def test_login_rate_limit(client):
    payload = {
        "email": "wrong@example.com",
        "password": "wrongpassword",
    }

    last_response = None

    for _ in range(101):
        last_response = client.post("/api/v1/auth/login", json=payload)

    assert last_response is not None
    assert last_response.status_code == 429

    body = last_response.json()

    assert body["success"] is False
    assert body["error"]["message"] == "Too many requests. Please try again later."