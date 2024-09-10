import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.models import Base
from backend.main import app
from backend.utils import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./temp_for_tests.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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


# Helper function to insert an ItemConfig and return its ID
def insert_item_config():
    item_config_data = {
        "triangle_size": 100,
        "triangle_color": "#FF0000",
        "circle_size": 50,
        "circle_color": "#00FF00",
        "time_visible_ms": 1000,
        "orientation": "N",
    }
    create_response = client.post("/api/item_configs/", json=item_config_data)
    return create_response.json()["id"]


def test_create_test_config_endpoint(setup_database):
    item_config_ids = [insert_item_config(), insert_item_config()]

    test_config_data = {"name": "Test Config 1", "item_config_ids": item_config_ids}
    response = client.post("/api/test_configs/", json=test_config_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_config_data["name"]
    assert len(data["item_configs"]) == len(test_config_data["item_config_ids"])


def test_create_test_config_endpoint_invalid_data(setup_database):
    test_config_data = {
        "name": "Test Config Invalid",
        "item_config_ids": ["invalid_id_1", "invalid_id_2"],
    }
    response = client.post("/api/test_configs/", json=test_config_data)
    assert response.status_code == 422


def test_read_test_configs_endpoint(setup_database):
    # First, create a test config
    item_config_ids = [insert_item_config()]

    test_config_data = {"name": "Test Config 2", "item_config_ids": item_config_ids}
    create_response = client.post("/api/test_configs/", json=test_config_data)
    assert create_response.status_code == 200

    # Now check that the test config is within the list of all test configs
    read_response = client.get("/api/test_configs/")
    assert read_response.status_code == 200
    data = read_response.json()
    # Check that the test config is in the list
    for test_config in data:
        if test_config["id"] == create_response.json()["id"]:
            assert test_config["name"] == test_config_data["name"]
            assert len(test_config["item_configs"]) == len(
                test_config_data["item_config_ids"]
            )
            break


def test_read_test_config_by_id_endpoint(setup_database):
    # First, create a test config
    item_config_ids = [insert_item_config()]

    test_config_data = {"name": "Test Config 3", "item_config_ids": item_config_ids}
    create_response = client.post("/api/test_configs/", json=test_config_data)
    assert create_response.status_code == 200
    test_config_id = create_response.json()["id"]

    # Now read the test config by ID
    read_response = client.get(f"/api/test_configs/{test_config_id}")
    assert read_response.status_code == 200
    data = read_response.json()
    assert data["name"] == test_config_data["name"]
    assert len(data["item_configs"]) == len(test_config_data["item_config_ids"])


def test_read_test_config_by_id_endpoint_invalid_id(setup_database):
    # Try to read a test config that doesn't exist
    invalid_id = 928289238
    read_response = client.get(f"/api/test_configs/{invalid_id}")
    assert read_response.status_code == 404


def test_update_test_config_endpoint(setup_database):
    # First, create a test config
    item_config_ids = [insert_item_config()]

    test_config_data = {"name": "Test Config 4", "item_config_ids": item_config_ids}
    create_response = client.post("/api/test_configs/", json=test_config_data)
    assert create_response.status_code == 200
    test_config_id = create_response.json()["id"]

    # Now update the test config
    update_data = {
        "name": "Updated Test Config 4",
        "item_config_ids": item_config_ids,  # Keeping the same item config IDs for simplicity
    }
    update_response = client.put(
        f"/api/test_configs/{test_config_id}", json=update_data
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == update_data["name"]
    assert len(data["item_configs"]) == len(update_data["item_config_ids"])


def test_update_test_config_endpoint_invalid_id(setup_database):
    # Try to update a test config with an invalid ID
    invalid_id = 928289238
    update_data = {"name": "Invalid Update", "item_config_ids": [insert_item_config()]}
    update_response = client.put(f"/api/test_configs/{invalid_id}", json=update_data)
    assert update_response.status_code == 404


def test_delete_test_config_endpoint(setup_database):
    # First, create a test config
    item_config_ids = [insert_item_config()]

    test_config_data = {"name": "Test Config 5", "item_config_ids": item_config_ids}
    create_response = client.post("/api/test_configs/", json=test_config_data)
    assert create_response.status_code == 200
    test_config_id = create_response.json()["id"]

    # Now delete the test config
    delete_response = client.delete(f"/api/test_configs/{test_config_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["name"] == test_config_data["name"]

    # assert that the test config was deleted
    read_response = client.get(f"/api/test_configs/{test_config_id}")
    assert read_response.status_code == 404


def test_delete_test_config_endpoint_invalid_id(setup_database):
    # Try to delete a test config with an invalid ID
    invalid_id = 928289238
    delete_response = client.delete(f"/api/test_configs/{invalid_id}")
    assert delete_response.status_code == 404
