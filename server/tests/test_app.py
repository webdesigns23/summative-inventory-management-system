import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from inventory import items
import inventory as inventory

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
    response = client.post("/inventory", json={
        "name": "New Item", 
        "brand": "New Brand", 
        "price": 10.99, 
        "stock": 12})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data and "name" in data
    assert data["name"] == "New Item"
    assert data["brand"] == "New Brand"
    assert data["price"] == 10.99
    assert data["stock"] == 12

def test_get_item():
    items.clear()
    client = app.test_client()
    client.post("/inventory", json={
        "name": "Sample Item",
        "brand": "Brand1",
        "price": 5.99,
        "stock": 10
        })
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Sample Item"

def test_post_inventory_adds_new_item(client):
    payload = {
        "name": "New Test Item",
        "brand": "Brand Test",
        "price": 3.99,
        "stock": 5
        }
    response = client.post("/inventory", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["name"] == payload["name"]
    assert data["brand"] == payload["brand"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]
    assert "id" in data

def test_patch_item():
    items.clear()
    client = app.test_client()
    client.post("/inventory", json={
        "name": "Name1",
        "brand": "Brand1",
        "price": 3.99,
        "stock": 5
        })
    response = client.patch("/inventory/1", json={"price": 6.99, "stock": 8})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Name1"
    assert response.get_json()["brand"] == "Brand1"
    assert response.get_json()["price"] == 6.99
    assert response.get_json()["stock"] == 8

def test_delete_item():
    items.clear()
    client = app.test_client()
    client.post("/inventory", json={
        "name": "Delete Name",
        "brand": "Delete Brand",
        "price": 2.99,
        "stock": 3
        })
    response = client.delete("/inventory/1")
    assert response.status_code == 204
    get_response = client.get("/inventory/1")
    assert get_response.status_code == 404

def test_count_items(client):
    inventory.items.clear()
    inventory.items.append({"id": 1, "name": "Item One"})
    inventory.items.append({"id": 2, "name": "Item Two"})

    response = client.get("/inventory/count")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 2