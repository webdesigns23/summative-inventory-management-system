import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import app
from server.data import items

@pytest.fixture
def client():
    return app.test_client()

def test_homepage_returns_welcome_message(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "welcome" in data["message"].lower()

def test_create_inventory():
    items.clear()
    client = app.test_client()
    response = client.post("/inventory", json={"name": "New Item"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data and "name" in data
    assert data["name"] == "New Item"

def test_get_item():
    items.clear()
    client = app.test_client()
    client.post("/inventory", json={"name": "Sample Item"})
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Sample Item"

def test_post_inventory_adds_new_item(client):
    payload = {"name": "New Test Item"}
    response = client.post("/inventory", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["name"] == payload["name"]
    assert "id" in data

def test_patch_item():
    items.clear()
    client = app.test_client()
    client.post("/inventory", json={"name": "Old Name"})
    response = client.patch("/inventory/1", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Updated Name"

def test_delete_item():
    items.clear()
    client = app.test_client()
    client.post("/inventory", json={"name": "To Be Deleted"})
    response = client.delete("/inventory/1")
    assert response.status_code == 204
    get_response = client.get("/inventory/1")
    assert get_response.status_code == 404