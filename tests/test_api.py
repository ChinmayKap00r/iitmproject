from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_run_task():
    response = client.post("/run", json={"task": "install uv and run datagen.py"})
    assert response.status_code == 200
    assert "success" in response.json()

def test_read_file():
    response = client.get("/read", params={"path": "data/dates.txt"})
    assert response.status_code == 200
    assert "content" in response.json()
