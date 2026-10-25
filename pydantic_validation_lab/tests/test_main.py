from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user_success():
    response = client.post(
        "/users",
        json={
            "name": "John Doe",
            "age": 30,
            "email": "deepka@example.com",
            "bio": "A short bio"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["name"] == "John Doe"
    assert response.json()["data"]["age"] == 30
    assert response.json()["data"]["email"] == "deepka@example.com"
    assert response.json()["data"]["bio"] == "A short bio"

def test_create_user_invalid_name():
    response = client.post(
        "/users",
        json={
            "name": "J",
            "age": 30,
            "email": "[EMAIL_ADDRESS]",
            "bio": "A short bio"
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should have at least 2 characters"

def test_create_user_invalid_age():
    response = client.post(
        "/users",
        json={
            "name": "John Doe",
            "age": 17,
            "email": "deepka@example.com",
            "bio": "A short bio"
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be greater than or equal to 18"

def test_create_user_invalid_email():
    response = client.post(
        "/users",
        json={
            "name": "John Doe",
            "age": 30,
            "email": "invalid-email",
            "bio": "A short bio"
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid email address: An email address must have an @-sign."

def test_create_user_missing_fields():
    response = client.post(
        "/users",
        json={
            "age": 30,
            "email": "deepak@example.com"
        }
    )

    print(response.json())
    assert response.status_code == 422
    errors = response.json()["detail"]
    
    assert any(
        error["loc"] == ["body", "name"] and error["type"] == "missing"
        for error in errors
    )

def test_create_user_bio_too_long():
    response = client.post(
        "/users",
        json={
            "name": "John Doe",
            "age": 30,
            "email": "deepak@example.com",
            "bio": "a" * 201,
        }
    )

    assert response.status_code == 422

def test_create_user_name_only_digits():
    response = client.post(
       "/users",
        json={
            "name": "12345",
            "age": 30,
            "email": "deepak@example.com",
            "bio": "A short bio"
        }
    )

    assert response.status_code == 422
    errors = response.json()["detail"]

    assert any(
        error["loc"] == ["body", "name"] and error["msg"] == "Value error, Name cannot contain only digits"
        for error in errors
    )

def test_create_username_is_trimmed():
    response = client.post("/users", json={
        "name": "   John Doe   ",
        "age": 30,
        "email": "deepak@example.com",
        "bio": "A short bio"
    })

    assert response.status_code == 200
    assert response.json()["data"]["name"] == "John Doe"