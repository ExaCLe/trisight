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
        "/api/users/login", data={"username": username, "password": "testpassword"}
    )
    token = login_response.json()["access_token"]

    return token, register_response.json()["id"]


def test_create_item_config_endpoint(setup_database):
    token, user_id = get_user_id_and_token()
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["triangle_size"] == item_config_data["triangle_size"]
    assert data["triangle_color"] == item_config_data["triangle_color"]
    assert data["circle_size"] == item_config_data["circle_size"]
    assert data["circle_color"] == item_config_data["circle_color"]
    assert data["time_visible_ms"] == item_config_data["time_visible_ms"]
    assert data["orientation"] == item_config_data["orientation"]
    assert data["user_id"] == user_id


def test_create_item_config_endpoint_unauthorized(setup_database):
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer invalidtoken"},
    )
    assert response.status_code == 401


def test_create_item_config_endpoint_invalid_data(setup_database):
    token, user_id = get_user_id_and_token()
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": "invalid",
        "orientation": "N",
    }
    response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_create_item_config_endpoint_invalid_orientation(setup_database):
    token, user_id = get_user_id_and_token()
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "invalid",
    }
    response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_create_item_config_endpoint_invalid_length(setup_database):
    token, user_id = get_user_id_and_token()
    item_config_data = {
        "triangle_size": -1,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422

    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": -1,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }

    response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_read_item_configs_endpoint(setup_database):
    token, user_id = get_user_id_and_token()
    # First, create an item config
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    create_response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 200

    # Now check that the item config is within the list of all item configs
    read_response = client.get("/api/item_configs/")
    assert read_response.status_code == 200
    data = read_response.json()
    # Check that the item config is in the list
    for item_config in data:
        if item_config["id"] == create_response.json()["id"]:
            assert item_config["triangle_size"] == item_config_data["triangle_size"]
            assert item_config["triangle_color"] == item_config_data["triangle_color"]
            assert item_config["circle_size"] == item_config_data["circle_size"]
            assert item_config["circle_color"] == item_config_data["circle_color"]
            assert item_config["time_visible_ms"] == item_config_data["time_visible_ms"]
            assert item_config["orientation"] == item_config_data["orientation"]
            assert item_config["user_id"] == user_id
            break


def test_read_item_config_by_id_endpoint(setup_database):
    token, user_id = get_user_id_and_token()
    # First, create an item config
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    create_response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 200
    item_config_id = create_response.json()["id"]

    # Now read the item config by ID
    read_response = client.get(f"/api/item_configs/{item_config_id}")
    assert read_response.status_code == 200
    data = read_response.json()
    assert data["triangle_size"] == item_config_data["triangle_size"]
    assert data["triangle_color"] == item_config_data["triangle_color"]
    assert data["circle_size"] == item_config_data["circle_size"]
    assert data["circle_color"] == item_config_data["circle_color"]
    assert data["time_visible_ms"] == item_config_data["time_visible_ms"]
    assert data["orientation"] == item_config_data["orientation"]
    assert data["user_id"] == user_id


def test_read_item_config_by_id_endpoint_invalid_id(setup_database):
    # Try to read an item config that doesn't exist
    read_response = client.get("/api/item_configs/999")
    assert read_response.status_code == 404


def test_update_item_config_endpoint(setup_database):
    token, user_id = get_user_id_and_token()
    # First, create an item config
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    create_response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 200
    item_config_id = create_response.json()["id"]

    # Now update the item config
    update_data = {
        "triangle_size": 200,
        "triangle_color": "#00FF00",
        "circle_size": 100,
        "circle_color": "#FF0000",
        "time_visible_ms": 2000,
        "orientation": "E",
    }
    update_response = client.put(
        f"/api/item_configs/{item_config_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["triangle_size"] == update_data["triangle_size"]
    assert data["triangle_color"] == update_data["triangle_color"]
    assert data["circle_size"] == update_data["circle_size"]
    assert data["circle_color"] == update_data["circle_color"]
    assert data["time_visible_ms"] == update_data["time_visible_ms"]
    assert data["orientation"] == update_data["orientation"]
    assert data["user_id"] == user_id


def test_update_item_config_endpoint_unauthorized(setup_database):
    token, user_id = get_user_id_and_token()
    token2, user_id2 = get_user_id_and_token("testuser2")
    # First, create an item config
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    create_response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 200
    item_config_id = create_response.json()["id"]

    # Now update the item config
    update_data = {
        "triangle_size": 200,
        "triangle_color": "#00FF00",
        "circle_size": 100,
        "circle_color": "#FF0000",
        "time_visible_ms": 2000,
        "orientation": "E",
    }
    update_response = client.put(
        f"/api/item_configs/{item_config_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert update_response.status_code == 401


def test_delete_item_config_endpoint(setup_database):
    token, user_id = get_user_id_and_token()
    # First, create an item config
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    create_response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 200
    item_config_id = create_response.json()["id"]

    # Now delete the item config
    delete_response = client.delete(
        f"/api/item_configs/{item_config_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["triangle_size"] == item_config_data["triangle_size"]
    assert data["triangle_color"] == item_config_data["triangle_color"]
    assert data["circle_size"] == item_config_data["circle_size"]
    assert data["circle_color"] == item_config_data["circle_color"]
    assert data["time_visible_ms"] == item_config_data["time_visible_ms"]
    assert data["orientation"] == item_config_data["orientation"]
    assert data["user_id"] == user_id

    # assert that the item config was deleted
    read_response = client.get(f"/api/item_configs/{item_config_id}")
    assert read_response.status_code == 404


def test_delete_item_config_endpoint_unauthorized(setup_database):
    token, user_id = get_user_id_and_token()
    token2, user_id2 = get_user_id_and_token("testuser2")
    # First, create an item config
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    create_response = client.post(
        "/api/item_configs/",
        json=item_config_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 200
    item_config_id = create_response.json()["id"]

    # Now delete the item config
    delete_response = client.delete(
        f"/api/item_configs/{item_config_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert delete_response.status_code == 401
