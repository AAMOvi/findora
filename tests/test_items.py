from findora.db.seed import seed_categories


def test_create_item(client, db_session):
    seed_categories(db_session)

    response = client.post(
        "/api/v1/items",
        json={
            "title": "Lost Wallet",
            "description": "Black leather wallet lost near library.",
            "status": "lost",
            "category_id": 3,
            "location": "Central Library",
            "date_lost_or_found": "2026-05-20",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True
    assert body["data"]["title"] == "Lost Wallet"
    assert body["data"]["status"] == "lost"


def test_list_items(client, db_session):
    seed_categories(db_session)

    client.post(
        "/api/v1/items",
        json={
            "title": "Found Phone",
            "description": "Found a phone near cafeteria.",
            "status": "found",
            "category_id": 2,
            "location": "Cafeteria",
        },
    )

    response = client.get("/api/v1/items")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["meta"]["total"] == 1


def test_get_item_detail(client, db_session):
    seed_categories(db_session)

    create_response = client.post(
        "/api/v1/items",
        json={
            "title": "Lost Calculator",
            "description": "Scientific calculator lost in exam hall.",
            "status": "lost",
            "category_id": 6,
            "location": "Exam Hall",
        },
    )

    item_id = create_response.json()["data"]["id"]

    response = client.get(f"/api/v1/items/{item_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["id"] == item_id
    assert body["data"]["title"] == "Lost Calculator"


def test_get_missing_item_returns_404(client):
    response = client.get("/api/v1/items/999")

    assert response.status_code == 404