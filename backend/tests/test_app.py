import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def client():
    with patch("app.get_conn") as mock_conn:
        mock_cursor = MagicMock()

        mock_conn.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            (1, "Nota test", "Contenido test", "2026-05-13 00:00:00")
        ]
        mock_cursor.fetchone.return_value = (1,)

        import app as flask_app  # noqa: E402

        flask_app.app.config["TESTING"] = True

        with flask_app.app.test_client() as client:
            yield client


def test_health(client):
    with patch("app.get_conn"):
        response = client.get("/health")

    assert response.status_code == 200

    data = json.loads(response.data)
    assert "status" in data


def test_get_notes(client):
    response = client.get("/api/notes")

    assert response.status_code == 200

    data = json.loads(response.data)
    assert isinstance(data, list)


def test_create_note(client):
    response = client.post(
        "/api/notes",
        data=json.dumps({"title": "Test", "content": "Contenido"}),
        content_type="application/json",
    )

    assert response.status_code == 201


def test_create_note_sin_titulo(client):
    response = client.post(
        "/api/notes",
        data=json.dumps({"content": "Sin título"}),
        content_type="application/json",
    )

    assert response.status_code in (400, 500)


def test_delete_note(client):
    response = client.delete("/api/notes/1")

    assert response.status_code == 200
