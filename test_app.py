# test_app.py

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI"}


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200

    users = response.json()

    assert isinstance(users, list)
    assert len(users) == 2


def test_get_existing_user():
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alice",
    }


def test_get_non_existing_user():
    response = client.get("/users/100")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found",
    }


def test_create_user():
    payload = {
        "name": "Charlie",
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 3
    assert data["name"] == "Charlie"
