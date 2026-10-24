from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_valid_email():
    response = client.post(
        "/validate/email",
        json={"email": "deepak@example.com"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Email is valid", "email": "deepak@example.com"}

def test_empty_email():
    response = client.post(
        "/validate/email",
        json={"email": ""}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email cannot be empty"}

def test_invalid_email():
    response = client.post(
        "/validate/email",
        json={"email": "deepak.com"}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email is not valid"}  

def test_missing_field_email():
    response = client.post(
        "/validate/email",
        json={}
    )

    assert response.status_code == 422

def test_valid_name():
    response = client.post(
        "/validate/name",
        json={"name": "Deepak"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Name is valid", "name": "Deepak"}

def test_empty_name():
    response = client.post(
        "/validate/name",
        json={"name": ""}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Name cannot be empty"}

def test_invalid_name():
    response = client.post(
        "/validate/name",
        json={"name": "123"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Name is valid", "name": "123"}

def test_missing_field_name():
    response = client.post(
        "/validate/name",
        json={}
    )

    assert response.status_code == 422  
