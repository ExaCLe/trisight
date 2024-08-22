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


def insert_test_config_to_db():
    # Helper function to insert a test config and return its ID
    item_config_ids = []
    for _ in range(2):
        response = insert_item_config_to_db()
        item_config_ids.append(response.json()["id"])

    test_config_data = {
        "name": "Test Config 1",
        "item_config_ids": item_config_ids
    }
    return client.post("/api/test_configs/", json=test_config_data)


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


def insert_test_config_result_to_db():
    response = insert_test_config_to_db()
    test_config_id = response.json()["id"]

    item_config_result_ids = []
    for _ in range(2):
        item_config_response = insert_item_config_to_db()
        item_config_id = item_config_response.json()["id"]
        item_config_result_data = {
            "item_config_id": item_config_id,
            "correct": True,
            "reaction_time_ms": 100,
            "response": "N"
        }
        item_config_result_response = client.post("/api/item_config_results/", json=item_config_result_data)
        item_config_result_ids.append(item_config_result_response.json()["id"])

    test_config_result_data = {
        "test_config_id": test_config_id,
        "correct_answers": 2,
        "wrong_answers": 0,
        "item_config_result_ids": item_config_result_ids,
        "time": "2024-01-01T00:00:00"
    }
    return client.post("/api/test_config_results/", json=test_config_result_data)


def test_create_test_config_result(setup_database):
    response = insert_test_config_result_to_db()
    assert response.status_code == 200
    data = response.json()
    assert data["test_config_id"] is not None
    assert data["correct_answers"] == 2
    assert data["wrong_answers"] == 0
    assert len(data["item_config_results"]) == 2
    assert data["time"] == "2024-01-01T00:00:00"


def test_create_test_config_result_invalid_data(setup_database):
    response = insert_test_config_to_db()
    test_config_id = response.json()["id"]
    test_config_result_data = {
        "test_config_id": test_config_id,
        "correct_answers": 2,
        "wrong_answers": 0,
        "item_config_result_ids": "invalid_id",  # Invalid data
        "time": "2024-01-01T00:00:00"
    }
    response = client.post("/api/test_config_results/", json=test_config_result_data)
    assert response.status_code == 422


def test_insert_test_config_result_with_invalid_test_config_id(setup_database):
    test_config_result_data = {
        "test_config_id": 928289238,
        "correct_answers": 2,
        "wrong_answers": 0,
        "item_config_result_ids": [],
        "time": "2024-01-01T00:00:00"
    }
    response = client.post("/api/test_config_results/", json=test_config_result_data)
    assert response.status_code == 422
    assert "FOREIGN KEY constraint failed" in str(response.json()["detail"])


def test_read_all_test_config_results_for_test_config(setup_database):
    response = insert_test_config_result_to_db()
    test_config_id = response.json()["test_config_id"]

    response = client.get(f"/api/test_config_results/test_config/{test_config_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["test_config_id"] == test_config_id
    assert data[0]["correct_answers"] == 2
    assert len(data[0]["item_config_results"]) == 2


def test_read_test_config_result_by_id(setup_database):
    response = insert_test_config_result_to_db()
    test_config_result_id = response.json()["id"]
    response = client.get(f"/api/test_config_results/{test_config_result_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["test_config_id"] is not None
    assert data["correct_answers"] == 2
    assert data["wrong_answers"] == 0
    assert len(data["item_config_results"]) == 2
    assert data["time"] == "2024-01-01T00:00:00"


def test_read_test_config_result_by_invalid_id(setup_database):
    response = client.get("/api/test_config_results/928289238")
    assert response.status_code == 404


def test_update_test_config_result(setup_database):
    response = insert_test_config_result_to_db()
    test_config_result_id = response.json()["id"]

    update_data = {
        "test_config_id": response.json()["test_config_id"],
        "correct_answers": 1,
        "wrong_answers": 1,
        "item_config_result_ids": [item['id'] for item in response.json()["item_config_results"]],
        "time": "2024-01-01T12:00:00"
    }

    response = client.put(f"/api/test_config_results/{test_config_result_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["correct_answers"] == 1
    assert data["wrong_answers"] == 1
    assert data["time"] == "2024-01-01T12:00:00"


def test_update_test_config_result_invalid_id(setup_database):
    update_data = {
        "test_config_id": 1,  # Assuming this ID exists
        "correct_answers": 1,
        "wrong_answers": 1,
        "item_config_result_ids": [],
        "time": "2024-01-01T12:00:00"
    }

    response = client.put("/api/test_config_results/928289238", json=update_data)
    assert response.status_code == 404


def test_delete_test_config_result(setup_database):
    response = insert_test_config_result_to_db()
    test_config_result_id = response.json()["id"]

    response = client.delete(f"/api/test_config_results/{test_config_result_id}")
    assert response.status_code == 200

    # Ensure the test config result is deleted
    response = client.get(f"/api/test_config_results/{test_config_result_id}")
    assert response.status_code == 404


def test_delete_test_config_result_invalid_id(setup_database):
    response = client.delete("/api/test_config_results/928289238")
    assert response.status_code == 404
