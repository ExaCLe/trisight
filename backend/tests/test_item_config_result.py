import pytest
from fastapi.testclient import TestClient

from backend.database import Base, engine, SessionLocal
from backend.main import app
from backend.utils import get_db

# Create a TestClient using the FastAPI app
client = TestClient(app)


# Create the test database and tables before running tests
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Dependency override to use a fresh session for each test
def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def insert_item_config_to_db():
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N"
    }
    return client.post("/api/item_configs/", json=item_config_data)


def test_create_item_config_result(setup_database):
    response = insert_item_config_to_db()
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N"
    }
    response = client.post("/api/item_config_results/", json=item_config_result_data)
    assert response.status_code == 200
    data = response.json()
    assert data["item_config_id"] == item_config_id
    assert data["correct"] == item_config_result_data["correct"]
    assert data["reaction_time_ms"] == item_config_result_data["reaction_time_ms"]
    assert data["response"] == item_config_result_data["response"]
    assert data["user_id"] == None


def test_create_item_config_result_invalid_data(setup_database):
    response = insert_item_config_to_db()
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": "invalid",
        "response": "N"
    }
    response = client.post("/api/item_config_results/", json=item_config_result_data)
    assert response.status_code == 422
    assert "Input should be a valid integer" in str(response.json()["detail"])


def test_insert_with_invalid_item_config_id(setup_database):
    item_config_result_data = {
        "item_config_id": 98275982794,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N"
    }
    response = client.post("/api/item_config_results/", json=item_config_result_data)
    assert response.status_code == 422
    assert "FOREIGN KEY constraint failed" in str(response.json()["detail"])


def test_read_all_item_config_results_for_item_config(setup_database):
    response = insert_item_config_to_db()
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N"
    }
    client.post("/api/item_config_results/", json=item_config_result_data)
    client.post("/api/item_config_results/", json=item_config_result_data)
    response = client.get(f"/api/item_config_results/item_config/{item_config_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["item_config_id"] == item_config_id
    assert data[1]["item_config_id"] == item_config_id
    assert data[0]["correct"] == item_config_result_data["correct"]
    assert data[1]["correct"] == item_config_result_data["correct"]
    assert data[0]["reaction_time_ms"] == item_config_result_data["reaction_time_ms"]
    assert data[1]["reaction_time_ms"] == item_config_result_data["reaction_time_ms"]
    assert data[0]["response"] == item_config_result_data["response"]
    assert data[1]["response"] == item_config_result_data["response"]
    assert data[0]["user_id"] == None
    assert data[1]["user_id"] == None


def test_read_item_config_results(setup_database):
    response = insert_item_config_to_db()
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N"
    }
    response = client.post("/api/item_config_results/", json=item_config_result_data)
    response = client.get(f"/api/item_config_results/{response.json()['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["item_config_id"] == item_config_id
    assert data["correct"] == item_config_result_data["correct"]
    assert data["reaction_time_ms"] == item_config_result_data["reaction_time_ms"]
    assert data["response"] == item_config_result_data["response"]
    assert data["user_id"] == None
