from fastapi.testclient import TestClient
from main import app  # Importing your FastAPI app

client = TestClient(app)  # Create a test client

def test_read_root():
    response = client.get("/")  # Simulating a GET request to "/"
    assert response.status_code == 200  # Checking if it returns a 200 OK status
    assert response.json() == {"message": "Hello, FastAPI is running!"}  # Checking the response content