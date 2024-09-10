import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base
from backend.main import app
from backend.utils import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./temp_for_tests.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


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


def get_user_id_and_token(username="testuser"):
    register_response = client.post(
        "/api/users/register",
        json={
            "username": username,
            "email": "test@test.de",
            "password": "testpassword",
        },
    )
    login_response = client.post(
        "/api/users/login", data={"username": "testuser", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]

    return token, register_response.json()["id"]


def test_create_item_config_result(setup_database):
    token, user_id = get_user_id_and_token()
    response = insert_item_config_to_db(token)
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    response = client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item_config_id"] == item_config_id
    assert data["correct"] == item_config_result_data["correct"]
    assert data["reaction_time_ms"] == item_config_result_data["reaction_time_ms"]
    assert data["response"] == item_config_result_data["response"]
    assert data["user_id"] == user_id


def test_create_item_config_unauthorized(setup_database):
    token, user_id = get_user_id_and_token()
    response = insert_item_config_to_db(token)
    item_config_id = response.json()["id"]
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
    token, user_id = get_user_id_and_token()
    response = insert_item_config_to_db(token)
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": "invalid",
        "response": "N",
    }
    response = client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
    assert "Input should be a valid integer" in str(response.json()["detail"])


def test_insert_with_invalid_item_config_id(setup_database):
    token, user_id = get_user_id_and_token()
    item_config_result_data = {
        "item_config_id": 98275982794,
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
    assert "FOREIGN KEY constraint failed" in str(response.json()["detail"])


def test_read_all_item_config_results_for_item_config(setup_database):
    token, user_id = get_user_id_and_token()
    response = insert_item_config_to_db(token)
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get(
        f"/api/item_config_results/item_config/{item_config_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
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
    assert data[0]["user_id"] == user_id
    assert data[1]["user_id"] == user_id


def test_read_all_item_config_results_for_item_config_unauthorized(setup_database):
    token, user_id = get_user_id_and_token()
    response = insert_item_config_to_db(token)
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get(
        f"/api/item_config_results/item_config/{item_config_id}",
        headers={"Authorization": f"Bearer unauthorizedtoken"},
    )
    assert response.status_code == 401


def test_read_all_item_config_results_for_item_config_only_own_results(setup_database):
    token, user_id = get_user_id_and_token()
    response = insert_item_config_to_db(token)
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    token2, user_id2 = get_user_id_and_token("testuser2")
    item_config_result_data2 = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    client.post(
        "/api/item_config_results/",
        json=item_config_result_data2,
        headers={"Authorization": f"Bearer {token2}"},
    )
    response = client.get(
        f"/api/item_config_results/item_config/{item_config_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
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
    assert data[0]["user_id"] == user_id
    assert data[1]["user_id"] == user_id


def test_read_item_config_results(setup_database):
    token, user_id = get_user_id_and_token()
    response = insert_item_config_to_db(token)
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    response = client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get(
        f"/api/item_config_results/{response.json()['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["item_config_id"] == item_config_id
    assert data["correct"] == item_config_result_data["correct"]
    assert data["reaction_time_ms"] == item_config_result_data["reaction_time_ms"]
    assert data["response"] == item_config_result_data["response"]
    assert data["user_id"] == user_id


def test_read_item_config_results_unauthorized(setup_database):
    token, user_id = get_user_id_and_token()
    token2, user_id2 = get_user_id_and_token("testuser2")
    response = insert_item_config_to_db(token)
    item_config_id = response.json()["id"]
    item_config_result_data = {
        "item_config_id": item_config_id,
        "correct": True,
        "reaction_time_ms": 100,
        "response": "N",
    }
    response = client.post(
        "/api/item_config_results/",
        json=item_config_result_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get(
        f"/api/item_config_results/{response.json()['id']}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert response.status_code == 401
