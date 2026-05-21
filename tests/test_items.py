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

def test_search_items_by_query(client, db_session):
    seed_categories(db_session)

    client.post(
        "/api/v1/items",
        json={
            "title": "Lost Wallet",
            "description": "Black wallet near library.",
            "status": "lost",
            "category_id": 3,
            "location": "Library",
        },
    )

    client.post(
        "/api/v1/items",
        json={
            "title": "Found Phone",
            "description": "Phone found near cafeteria.",
            "status": "found",
            "category_id": 2,
            "location": "Cafeteria",
        },
    )

    response = client.get("/api/v1/items?q=wallet")

    assert response.status_code == 200

    body = response.json()

    assert body["meta"]["total"] == 1
    assert body["data"][0]["title"] == "Lost Wallet"


def test_filter_items_by_status(client, db_session):
    seed_categories(db_session)

    client.post(
        "/api/v1/items",
        json={
            "title": "Lost Bag",
            "description": "Blue bag lost in classroom.",
            "status": "lost",
            "category_id": 4,
            "location": "Classroom",
        },
    )

    client.post(
        "/api/v1/items",
        json={
            "title": "Found Keys",
            "description": "Keys found near gate.",
            "status": "found",
            "category_id": 7,
            "location": "Main Gate",
        },
    )

    response = client.get("/api/v1/items?status=found")

    assert response.status_code == 200

    body = response.json()

    assert body["meta"]["total"] == 1
    assert body["data"][0]["status"] == "found"


def test_filter_items_by_category(client, db_session):
    seed_categories(db_session)

    client.post(
        "/api/v1/items",
        json={
            "title": "Lost Laptop",
            "description": "Laptop lost in lab.",
            "status": "lost",
            "category_id": 8,
            "location": "Computer Lab",
        },
    )

    response = client.get("/api/v1/items?category_id=8")

    assert response.status_code == 200

    body = response.json()

    assert body["meta"]["total"] == 1
    assert body["data"][0]["category_id"] == 8


def test_filter_items_by_location(client, db_session):
    seed_categories(db_session)

    client.post(
        "/api/v1/items",
        json={
            "title": "Found Book",
            "description": "Book found in central library.",
            "status": "found",
            "category_id": 5,
            "location": "Central Library",
        },
    )

    response = client.get("/api/v1/items?location=library")

    assert response.status_code == 200

    body = response.json()

    assert body["meta"]["total"] == 1
    assert body["data"][0]["location"] == "Central Library"


def test_filter_items_by_resolved_status(client, db_session):
    seed_categories(db_session)

    client.post(
        "/api/v1/items",
        json={
            "title": "Lost ID Card",
            "description": "ID card lost near office.",
            "status": "lost",
            "category_id": 1,
            "location": "Admin Office",
        },
    )

    response = client.get("/api/v1/items?resolved=false")

    assert response.status_code == 200

    body = response.json()

    assert body["meta"]["total"] == 1
    assert body["data"][0]["is_resolved"] is False


def test_items_pagination(client, db_session):
    seed_categories(db_session)

    for index in range(25):
        client.post(
            "/api/v1/items",
            json={
                "title": f"Lost Item {index}",
                "description": f"Description for lost item {index}.",
                "status": "lost",
                "category_id": 10,
                "location": "Campus",
            },
        )

    response = client.get("/api/v1/items?page=1&limit=10")

    assert response.status_code == 200

    body = response.json()

    assert len(body["data"]) == 10
    assert body["meta"]["page"] == 1
    assert body["meta"]["limit"] == 10
    assert body["meta"]["total"] == 25
    assert body["meta"]["total_pages"] == 3
    assert body["meta"]["has_next"] is True
    assert body["meta"]["has_prev"] is False


def test_items_sort_oldest(client, db_session):
    seed_categories(db_session)

    client.post(
        "/api/v1/items",
        json={
            "title": "First Item",
            "description": "First item description.",
            "status": "lost",
            "category_id": 10,
            "location": "Campus",
        },
    )

    client.post(
        "/api/v1/items",
        json={
            "title": "Second Item",
            "description": "Second item description.",
            "status": "found",
            "category_id": 10,
            "location": "Campus",
        },
    )

    response = client.get("/api/v1/items?sort=oldest")

    assert response.status_code == 200

    body = response.json()

    assert body["data"][0]["title"] == "First Item"