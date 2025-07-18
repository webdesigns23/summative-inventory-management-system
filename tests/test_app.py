import sys
import os
import json
import pytest

# Ensure the root project directory is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import app

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

def test_post_inventory_adds_new_item(client):
    payload = {"name": "New Test Item"}
    response = client.post("/inventory", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["name"] == payload["name"]
    assert "id" in data

