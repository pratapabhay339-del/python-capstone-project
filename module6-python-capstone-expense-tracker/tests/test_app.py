import tempfile
from pathlib import Path

import pytest

import app as app_module


@pytest.fixture()
def client(monkeypatch):
    temp_dir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(app_module, "DB_PATH", temp_dir / "test.db")
    app_module.init_db()
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as client:
        yield client


def sample_expense():
    return {
        "title": "Hostel Food",
        "amount": 120.50,
        "category": "Food",
        "expense_date": "2026-10-07",
        "notes": "Monthly hostel meal expense",
    }


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_create_and_list_expense(client):
    created = client.post("/api/expenses", json=sample_expense())
    assert created.status_code == 201
    assert created.json["title"] == "Hostel Food"

    listed = client.get("/api/expenses")
    assert listed.status_code == 200
    assert len(listed.json) == 1


def test_update_expense(client):
    created = client.post("/api/expenses", json=sample_expense())
    expense_id = created.json["id"]

    payload = sample_expense()
    payload["amount"] = 250

    response = client.put(f"/api/expenses/{expense_id}", json=payload)
    assert response.status_code == 200
    assert response.json["amount"] == 250


def test_delete_expense(client):
    created = client.post("/api/expenses", json=sample_expense())
    expense_id = created.json["id"]

    deleted = client.delete(f"/api/expenses/{expense_id}")
    assert deleted.status_code == 200

    missing = client.get("/api/expenses")
    assert missing.json == []


def test_validation_rejects_negative_amount(client):
    payload = sample_expense()
    payload["amount"] = -10

    response = client.post("/api/expenses", json=payload)
    assert response.status_code == 400
    assert "greater than 0" in response.json["error"]
