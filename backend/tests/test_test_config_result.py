import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base
from backend.main import app
from backend.tests.utils import get_user_id_and_token
from backend.utils import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./temp_for_tests.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def insert_test_config_to_db(token):
    # Helper function to insert a test config and return its ID
    item_config_ids = []
    for _ in range(2):
        response = insert_item_config_to_db(token)
        item_config_ids.append(response.json()["id"])

    test_config_data = {"name": "Test Config 1", "item_config_ids": item_config_ids}
    return client.post(
        "/api/test_configs/",
        json=test_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )


def insert_item_config_to_db(token):
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    return client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )


def insert_test_config_result_to_db(token):
    response = insert_test_config_to_db(token)
    test_config_id = response.json()["id"]

    item_config_result_ids = []
    for _ in range(2):
        item_config_response = insert_item_config_to_db(token)
        item_config_id = item_config_response.json()["id"]
        item_config_result_data = {
            "item_config_id": item_config_id,
            "correct": True,
            "reaction_time_ms": 100,
            "response": "N",
        }
        item_config_result_response = client.post(
            "/api/item_config_results/",
            json=item_config_result_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        item_config_result_ids.append(item_config_result_response.json()["id"])

    test_config_result_data = {
        "test_config_id": test_config_id,
        "correct_answers": 2,
        "wrong_answers": 0,
        "item_config_result_ids": item_config_result_ids,
        "time": "2024-01-01T00:00:00",
    }
    return client.post(
        "/api/test_config_results/",
        json=test_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )


def test_create_test_config_result(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_result_to_db(token)
    assert response.status_code == 200
    data = response.json()
    assert data["test_config_id"] is not None
    assert data["correct_answers"] == 2
    assert data["wrong_answers"] == 0
    assert len(data["item_config_results"]) == 2
    assert data["time"] == "2024-01-01T00:00:00"
    assert data["user_id"] == user_id


def test_create_test_config_result_unauthorized(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_to_db(token)
    test_config_id = response.json()["id"]
    test_config_result_data = {
        "test_config_id": test_config_id,
        "correct_answers": 2,
        "wrong_answers": 0,
        "item_config_result_ids": [],
        "time": "2024-01-01T00:00:00",
    }
    response = client.post(
        "/api/test_config_results/",
        json=test_config_result_data,
        headers={"Authorization": f"Bearer invalid_token"},
    )
    assert response.status_code == 401


def test_create_test_config_result_invalid_data(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_to_db(token)
    test_config_id = response.json()["id"]
    test_config_result_data = {
        "test_config_id": test_config_id,
        "correct_answers": 2,
        "wrong_answers": 0,
        "item_config_result_ids": "invalid_id",  # Invalid data
        "time": "2024-01-01T00:00:00",
    }
    response = client.post(
        "/api/test_config_results/",
        json=test_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_insert_test_config_result_with_invalid_test_config_id(setup_database):
    token, user_id = get_user_id_and_token(client)
    test_config_result_data = {
        "test_config_id": 928289238,
        "correct_answers": 2,
        "wrong_answers": 0,
        "item_config_result_ids": [],
        "time": "2024-01-01T00:00:00",
    }
    response = client.post(
        "/api/test_config_results/",
        json=test_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
    assert "FOREIGN KEY constraint failed" in str(response.json()["detail"])


def test_read_all_test_config_results_for_test_config(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_result_to_db(token)
    test_config_id = response.json()["test_config_id"]

    response = client.get(
        f"/api/test_config_results/test_config/{test_config_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["test_config_id"] == test_config_id
    assert data[0]["correct_answers"] == 2
    assert data[0]["wrong_answers"] == 0
    assert data[0]["user_id"] == user_id
    assert len(data[0]["item_config_results"]) == 2


def test_read_all_test_config_results_for_test_config_only_own_results(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_result_to_db(token)
    test_config_id = response.json()["test_config_id"]

    # Insert a test config result for a different user
    token2, user_id2 = get_user_id_and_token(client, "testuser2")
    test_config_results_data = {
        "test_config_id": test_config_id,
        "correct_answers": 2,
        "wrong_answers": 0,
        "item_config_result_ids": [],
        "time": "2024-01-01T00:00:00",
    }
    response = client.post(
        "/api/test_config_results/",
        json=test_config_results_data,
        headers={"Authorization": f"Bearer {token2}"},
    )

    response = client.get(
        f"/api/test_config_results/test_config/{test_config_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["test_config_id"] == test_config_id
    assert data[0]["correct_answers"] == 2
    assert data[0]["wrong_answers"] == 0
    assert data[0]["user_id"] == user_id
    assert len(data[0]["item_config_results"]) == 2


def test_read_all_test_config_results_for_test_config_unauthorized(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_result_to_db(token)
    test_config_id = response.json()["test_config_id"]

    response = client.get(
        f"/api/test_config_results/test_config/{test_config_id}",
        headers={"Authorization": f"Bearer invalid_token"},
    )
    assert response.status_code == 401


def test_read_test_config_result_by_id(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_result_to_db(token)
    test_config_result_id = response.json()["id"]
    response = client.get(
        f"/api/test_config_results/{test_config_result_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["test_config_id"] is not None
    assert data["correct_answers"] == 2
    assert data["wrong_answers"] == 0
    assert data["user_id"] == user_id
    assert len(data["item_config_results"]) == 2
    assert data["time"] == "2024-01-01T00:00:00"


def test_read_test_config_result_by_id_unauthorized(setup_database):
    token, user_id = get_user_id_and_token(client)
    token2, user_id2 = get_user_id_and_token(client, "testuser2")
    response = insert_test_config_result_to_db(token)
    test_config_result_id = response.json()["id"]
    response = client.get(
        f"/api/test_config_results/{test_config_result_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 401


def test_read_test_config_result_by_invalid_id(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = client.get(
        "/api/test_config_results/928289238",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_update_test_config_result(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_result_to_db(token)
    test_config_result_id = response.json()["id"]

    update_data = {
        "test_config_id": response.json()["test_config_id"],
        "correct_answers": 1,
        "wrong_answers": 1,
        "item_config_result_ids": [
            item["id"] for item in response.json()["item_config_results"]
        ],
        "time": "2024-01-01T12:00:00",
    }

    response = client.put(
        f"/api/test_config_results/{test_config_result_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["correct_answers"] == 1
    assert data["wrong_answers"] == 1
    assert data["time"] == "2024-01-01T12:00:00"
    assert data["user_id"] == user_id


def test_update_test_config_result_unauthorized(setup_database):
    token, user_id = get_user_id_and_token(client)
    token2, user_id2 = get_user_id_and_token(client, "testuser2")
    response = insert_test_config_result_to_db(token)
    test_config_result_id = response.json()["id"]

    update_data = {
        "test_config_id": response.json()["test_config_id"],
        "correct_answers": 1,
        "wrong_answers": 1,
        "item_config_result_ids": [
            item["id"] for item in response.json()["item_config_results"]
        ],
        "time": "2024-01-01T12:00:00",
    }

    response = client.put(
        f"/api/test_config_results/{test_config_result_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 401


def test_update_test_config_result_invalid_id(setup_database):
    token, user_id = get_user_id_and_token(client)
    update_data = {
        "test_config_id": 1,  # Assuming this ID exists
        "correct_answers": 1,
        "wrong_answers": 1,
        "item_config_result_ids": [],
        "time": "2024-01-01T12:00:00",
    }

    response = client.put(
        "/api/test_config_results/928289238",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_delete_test_config_result(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = insert_test_config_result_to_db(token)
    test_config_result_id = response.json()["id"]

    response = client.delete(
        f"/api/test_config_results/{test_config_result_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Ensure the test config result is deleted
    response = client.get(
        f"/api/test_config_results/{test_config_result_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_delete_test_config_result_unauthorized(setup_database):
    token, user_id = get_user_id_and_token(client)
    token2, user_id2 = get_user_id_and_token(client, "testuser2")
    response = insert_test_config_result_to_db(token)
    test_config_result_id = response.json()["id"]

    response = client.delete(
        f"/api/test_config_results/{test_config_result_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 401


def test_delete_test_config_result_invalid_id(setup_database):
    token, user_id = get_user_id_and_token(client)
    response = client.delete(
        "/api/test_config_results/928289238",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
