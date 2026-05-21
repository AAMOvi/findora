def test_not_found_error_has_standard_shape(client):
    response = client.get("/api/v1/route-that-does-not-exist")

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["error"]["message"] == "Route not found."


def test_validation_error_has_standard_shape(client):
    response = client.post(
        "/api/v1/items",
        json={
            "title": "",
            "description": "Too short",
            "status": "lost",
            "category_id": "invalid",
            "location": "",
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert body["success"] is False
    assert body["error"]["message"] == "Validation error."
    assert "details" in body["error"]


def test_http_exception_has_standard_shape(client):
    response = client.get("/api/v1/items/999999")

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["error"]["message"] == "Item not found."