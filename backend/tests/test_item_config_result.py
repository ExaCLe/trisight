# test_item_config_results.py
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


def insert_item_config_to_db(token):
    """
    Inserts an Item Configuration into the database.

    :param token: Bearer token for authentication.
    :return: Response object from the API call.
    """
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


def insert_item_config_result_to_db(
    token, item_config_id, correct=True, reaction_time_ms=100, response="N"
):
    """
    Inserts an Item Configuration Result into the database.

    :param token: Bearer token for authentication.
    :param item_config_id: ID of the associated Item Configuration.
    :param correct: Boolean indicating if the answer was correct.
    :param reaction_time_ms: Reaction time in milliseconds.
    :param response: User's response.
    :return: Response object from the API call.
    """
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": correct,
        "reaction_time_ms": reaction_time_ms,
        "response": response,
    }
    return client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )


def test_create_item_config_result(setup_database):
    token, user_id = get_user_id_and_token(client)
    # Insert Item Configuration
    response = insert_item_config_to_db(token)
    assert response.status_code == 200
    item_config = response.json()
    item_config_id = item_config["id"]

    # Insert Item Configuration Result
    result_response = insert_item_config_result_to_db(token, item_config_id)
    assert result_response.status_code == 200
    data = result_response.json()
    assert data["item_config_id"] == item_config_id
    assert data["correct"] == True
    assert data["reaction_time_ms"] == 100
    assert data["response"] == "N"
    assert data["user_id"] == user_id


def test_create_item_config_unauthorized(setup_database):
    token, user_id = get_user_id_and_token(client)
    # Insert Item Configuration
    response = insert_item_config_to_db(token)
    assert response.status_code == 200
    item_config_id = response.json()["id"]

    # Attempt to insert Item Configuration Result with invalid token
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    response = client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer thisisnotavalidtoken"},
    )
    assert response.status_code == 401


def test_create_item_config_result_invalid_data(setup_database):
    token, user_id = get_user_id_and_token(client)
    # Insert Item Configuration
    response = insert_item_config_to_db(token)
    assert response.status_code == 200
    item_config_id = response.json()["id"]

    # Attempt to insert Item Configuration Result with invalid data
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": "invalid",  # Invalid data type
        "response": "N",
    }
    response = client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
    assert "Input should be a valid integer" in str(response.json()["detail"])


def test_insert_item_config_result_with_invalid_item_config_id(setup_database):
    token, user_id = get_user_id_and_token(client)
    # Attempt to insert Item Configuration Result with invalid Item Config ID
    item_config_result_data = {
        "item_config_id": 928289238,  # Assuming this ID does not exist
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    response = client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
    assert "Constraint error" in str(response.json()["detail"])


def test_read_all_item_config_results_for_item_config(setup_database):
    token, user_id = get_user_id_and_token(client)
    # Insert Item Configuration
    response = insert_item_config_to_db(token)
    assert response.status_code == 200
    item_config_id = response.json()["id"]

    # Insert two Item Configuration Results
    result1 = insert_item_config_result_to_db(token, item_config_id, correct=True)
    result2 = insert_item_config_result_to_db(token, item_config_id, correct=False)
    assert result1.status_code == 200
    assert result2.status_code == 200

    # Retrieve all Item Configuration Results for the Item Config
    response = client.get(
        f"/api/item_config_results/item_config/{item_config_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["item_config_id"] == item_config_id
    assert data[1]["item_config_id"] == item_config_id
    assert data[0]["correct"] == True
    assert data[1]["correct"] == False
    assert data[0]["reaction_time_ms"] == 100
    assert data[1]["reaction_time_ms"] == 100
    assert data[0]["response"] == "N"
    assert data[1]["response"] == "N"
    assert data[0]["user_id"] == user_id
    assert data[1]["user_id"] == user_id


def test_read_all_item_config_results_for_item_config_unauthorized(setup_database):
    token, user_id = get_user_id_and_token(client)
    # Insert Item Configuration
    response = insert_item_config_to_db(token)
    assert response.status_code == 200
    item_config_id = response.json()["id"]

    # Insert two Item Configuration Results
    insert_item_config_result_to_db(token, item_config_id)
    insert_item_config_result_to_db(token, item_config_id)

    # Attempt to retrieve with unauthorized token
    response = client.get(
        f"/api/item_config_results/item_config/{item_config_id}",
        headers={"Authorization": f"Bearer unauthorizedtoken"},
    )
    assert response.status_code == 401


def test_read_all_item_config_results_for_item_config_only_own_results(setup_database):
    token, user_id = get_user_id_and_token(client)
    token2, user_id2 = get_user_id_and_token(client, "testuser2")

    # Insert Item Configuration by User 1
    response = insert_item_config_to_db(token)
    assert response.status_code == 200
    item_config_id = response.json()["id"]

    # User 1 inserts two Item Configuration Results
    insert_item_config_result_to_db(token, item_config_id, correct=True)
    insert_item_config_result_to_db(token, item_config_id, correct=False)

    # User 2 inserts one Item Configuration Result
    insert_item_config_result_to_db(token2, item_config_id, correct=True)

    # User 1 retrieves their Item Configuration Results
    response = client.get(
        f"/api/item_config_results/item_config/{item_config_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Only User 1's results
    for item in data:
        assert item["user_id"] == user_id


def test_read_item_config_results(setup_database):
    token, user_id = get_user_id_and_token(client)
    # Insert Item Configuration
    response = insert_item_config_to_db(token)
    assert response.status_code == 200
    item_config_id = response.json()["id"]

    # Insert Item Configuration Result
    result_response = insert_item_config_result_to_db(token, item_config_id)
    assert result_response.status_code == 200
    result_id = result_response.json()["id"]

    # Retrieve Item Configuration Result by ID
    response = client.get(
        f"/api/item_config_results/{result_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["item_config_id"] == item_config_id
    assert data["correct"] == True
    assert data["reaction_time_ms"] == 100
    assert data["response"] == "N"
    assert data["user_id"] == user_id


def test_read_item_config_results_unauthorized(setup_database):
    token, user_id = get_user_id_and_token(client)
    token2, user_id2 = get_user_id_and_token(client, "testuser2")

    # Insert Item Configuration
    response = insert_item_config_to_db(token)
    assert response.status_code == 200
    item_config_id = response.json()["id"]

    # Insert Item Configuration Result by User 1
    result_response = insert_item_config_result_to_db(token, item_config_id)
    assert result_response.status_code == 200
    result_id = result_response.json()["id"]

    # Attempt to retrieve by User 2
    response = client.get(
        f"/api/item_config_results/{result_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 401


# New Tests for the /user endpoint


def test_read_all_item_config_results_for_user(setup_database):
    token, user_id = get_user_id_and_token(client)
    # Insert multiple Item Configurations and Results
    for _ in range(5):
        response = insert_item_config_to_db(token)
        assert response.status_code == 200
        item_config_id = response.json()["id"]
        insert_item_config_result_to_db(token, item_config_id, correct=True)

    # Retrieve all Item Configuration Results for the user
    response = client.get(
        "/api/item_config_results/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for item in data:
        assert item["user_id"] == user_id
        assert "item_config_id" in item
        assert "correct" in item
        assert "reaction_time_ms" in item
        assert "response" in item


def test_read_all_item_config_results_for_user_unauthorized(setup_database):
    # Attempt to retrieve without a valid token
    response = client.get(
        "/api/item_config_results/user",
        headers={"Authorization": f"Bearer invalid_token"},
    )
    assert response.status_code == 401


def test_read_all_item_config_results_for_user_only_own_results(setup_database):
    token, user_id = get_user_id_and_token(client)
    token2, user_id2 = get_user_id_and_token(client, "testuser2")

    # User 1 inserts 3 Item Configurations and Results
    for _ in range(3):
        response = insert_item_config_to_db(token)
        assert response.status_code == 200
        item_config_id = response.json()["id"]
        insert_item_config_result_to_db(token, item_config_id, correct=True)

    # User 2 inserts 2 Item Configurations and Results
    for _ in range(2):
        response = insert_item_config_to_db(token2)
        assert response.status_code == 200
        item_config_id = response.json()["id"]
        insert_item_config_result_to_db(token2, item_config_id, correct=False)

    # User 1 retrieves their Item Configuration Results
    response = client.get(
        "/api/item_config_results/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for item in data:
        assert item["user_id"] == user_id

    # User 2 retrieves their Item Configuration Results
    response = client.get(
        "/api/item_config_results/user",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for item in data:
        assert item["user_id"] == user_id2
