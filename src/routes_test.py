import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_openai_endpoint(client, httpx_mock):
    prompt = "Hello, OpenAI!"
    expected_response = {"choices": [{"message": {"content": "Hi there!"}}]}
    httpx_mock.add_response(
        url="https://api.openai.com/v1/chat/completions",
        method="POST",
        json=expected_response,
    )
    response = client.post("/openai", json={"prompt": prompt})
    assert response.status_code == 200
    assert response.json() == expected_response 