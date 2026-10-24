from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "app is running"}

def test_get_user_found():
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Deepak"}

def test_get_user_not_found():
    response = client.get("/users/2")

    assert response.status_code == 404
    assert response.json() == {
        "error": "User not found",
        "status_code": 404,
        "path": "/users/2"
    }

def test_invalid_user():
    response = client.get("/users/abc")

    assert response.status_code == 422

def test_http_exception_handler():
    response = client.get("/forbidden")
    assert response.status_code == 403
    assert response.json() == {
        "error": "You are not allowed to access this resource",
        "status_code": 403,
        "path": "/forbidden",
    }