from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_reminder():
    response = client.post("/reminders", json={"title": "Buy milk"})

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Buy milk"
    assert data["status"] == "pending"
    assert data["id"] > 0

def test_get_reminders():
    response = client.get("/reminders")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_reminder_by_id():
    create_response = client.post("/reminders", json={"title": "Buy milk"})
    reminder_id = create_response.json()["id"]
    response = client.get(f"/reminders/{reminder_id}")

    assert response.status_code == 200
    assert response.json()["id"] == reminder_id
    assert response.json()["title"] == "Buy milk"
    
def test_api_endpoint_nonexist():
    response = client.get("/reminders/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Reminder not found"}

def test_update_reminder():
    create_response = client.post("/reminders", json={"title": "Buy milk"})
    reminder_id = create_response.json()["id"]
    response = client.put(f"/reminders/{reminder_id}", json={"title": "Buy eggs"})

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == reminder_id
    assert data["title"] == "Buy eggs"

def test_delete_reminder():
    create_response = client.post("/reminders", json={"title": "Buy milk"})
    reminder_id = create_response.json()["id"]
    response = client.delete(f"/reminders/{reminder_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Reminder deleted"}

    get_response = client.get(f"/reminders/{reminder_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Reminder not found"}

def test_create_reminder_with_empty_title():
    response = client.post("/reminders", json = {"title": ""})
    assert response.status_code == 422

def test_create_reminder_without_title():
    response = client.post("/reminders", json={})
    assert response.status_code == 422

def test_create_reminder_with_title_int():
    response = client.post("/reminders", json={"title": 123})
    assert response.status_code == 422
