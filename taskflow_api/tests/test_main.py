from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root():
    resposne = client.get("/")
    assert resposne.status_code == 200
    assert resposne.json() == {"message": "Taskflow API is running"}

