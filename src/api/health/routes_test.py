import pytest
from fastapi.testclient import TestClient
from routes import router

# Create a test client for the health router
client = TestClient(router)

def test_health_check():
    """Test the general health check endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_llm_status_get():
    """Test the LLM status GET endpoint."""
    response = client.get("/llm")
    
    # This should work even if LLM services are not available
    assert response.status_code in [200, 500]  # 500 if LLM services are down

def test_llm_status_get_with_force_refresh():
    """Test the LLM status GET endpoint with force refresh."""
    response = client.get("/llm?force_refresh=true")
    
    # This should work even if LLM services are not available
    assert response.status_code in [200, 500]  # 500 if LLM services are down 