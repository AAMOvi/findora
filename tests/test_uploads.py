from io import BytesIO

from findora.db.seed import seed_categories


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


def test_upload_item_image(client, db_session, tmp_path, monkeypatch):
    from findora.core.config import settings

    monkeypatch.setattr(settings, "upload_dir", str(tmp_path))

    item_id = create_test_item(client, db_session)

    response = client.post(
        f"/api/v1/items/{item_id}/images",
        files={
            "file": (
                "wallet.png",
                BytesIO(b"fake image content"),
                "image/png",
            )
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True
    assert body["data"]["item_id"] == item_id
    assert body["data"]["original_filename"] == "wallet.png"
    assert body["data"]["content_type"] == "image/png"

    saved_filename = body["data"]["image_filename"]
    assert saved_filename.endswith(".png")
    assert (tmp_path / saved_filename).exists()


def test_upload_invalid_image_type_returns_415(client, db_session, tmp_path, monkeypatch):
    from findora.core.config import settings

    monkeypatch.setattr(settings, "upload_dir", str(tmp_path))

    item_id = create_test_item(client, db_session)

    response = client.post(
        f"/api/v1/items/{item_id}/images",
        files={
            "file": (
                "malware.txt",
                BytesIO(b"not an image"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 415


def test_upload_image_for_missing_item_returns_404(client, tmp_path, monkeypatch):
    from findora.core.config import settings

    monkeypatch.setattr(settings, "upload_dir", str(tmp_path))

    response = client.post(
        "/api/v1/items/999/images",
        files={
            "file": (
                "wallet.png",
                BytesIO(b"fake image content"),
                "image/png",
            )
        },
    )

    assert response.status_code == 404


def test_serve_uploaded_media_file(client, db_session, tmp_path, monkeypatch):
    from findora.core.config import settings

    monkeypatch.setattr(settings, "upload_dir", str(tmp_path))

    item_id = create_test_item(client, db_session)

    upload_response = client.post(
        f"/api/v1/items/{item_id}/images",
        files={
            "file": (
                "wallet.png",
                BytesIO(b"fake image content"),
                "image/png",
            )
        },
    )

    filename = upload_response.json()["data"]["image_filename"]

    response = client.get(f"/media/{filename}")

    assert response.status_code == 200
    assert response.content == b"fake image content"


def test_missing_media_file_returns_404(client, tmp_path, monkeypatch):
    from findora.core.config import settings

    monkeypatch.setattr(settings, "upload_dir", str(tmp_path))

    response = client.get("/media/missing.png")

    assert response.status_code == 404