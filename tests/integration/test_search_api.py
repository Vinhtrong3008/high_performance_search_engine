import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "High-Performance Web Crawler & Search Engine"

def test_search_api_validation():
    # Test gọi API search thiếu keyword hoặc size không hợp lệ
    response = client.get("/api/v1/search?size=100") # size vượt quá max=50
    assert response.status_code == 422