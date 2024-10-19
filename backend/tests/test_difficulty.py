import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_get_difficulty_endpoint_valid(difficulty):
    response = client.get(f"/api/difficulty/{difficulty}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) >= 5, "Should return at least 5 item configs"
    for item_config in data:
        assert "id" in item_config, "Item config should have an 'id' field"
        assert (
            "triangle_size" in item_config
        ), "Item config should have a 'triangle_size' field"
        assert (
            "triangle_color" in item_config
        ), "Item config should have a 'triangle_color' field"
        assert (
            "circle_size" in item_config
        ), "Item config should have a 'circle_size' field"
        assert (
            "circle_color" in item_config
        ), "Item config should have a 'circle_color' field"
        assert (
            "time_visible_ms" in item_config
        ), "Item config should have a 'time_visible_ms' field"
        assert (
            "orientation" in item_config
        ), "Item config should have an 'orientation' field"


@pytest.mark.parametrize("difficulty", ["easiest", "moderate", "hardest", "", "123"])
def test_get_difficulty_endpoint_invalid(difficulty):
    response = client.get(f"/api/difficulty/{difficulty}")
    assert response.status_code == 404, "Invalid difficulty levels should return 404"


def test_get_difficulty_endpoint_missing():
    response = client.get("/api/difficulty/")
    print(response.json())
    assert response.status_code == 404, "Missing difficulty level should return 404"
