import pytest
from fastapi.testclient import TestClient
from main import app, tasks

@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    tasks[1] = {
        "id": 1,
        "title": "Learn FastAPI",
        "status": "pending"
    }

client = TestClient(app)

def test_pending_to_in_progress():
    response = client.patch(
        "/tasks/1/status",
        json={"status": "in_progress"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

def test_in_progress_to_completed():
    client.patch(
        "/tasks/1/status",
        json={"status": "in_progress"}
    )

    response = client.patch(
        "/tasks/1/status",
        json={"status": "completed"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def invalid_transition_pending_to_completed():
    response = client.patch(
        "/tasks/1/status",
        json={"status": "completed"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Cannot transition from pending to completed"
    )

def test_invalid_status_value():
    response = client.patch(
        "/tasks/1/status",
        json={"status": "unknown"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid status"

def test_task_not_found():
    response = client.patch(
        "/tasks/99/status",
        json={"status": "in_progress"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task Not Found"