import os
from datetime import timedelta, timezone, datetime

import pytest
import jwt
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


def create_test_user(
    username="testuser", password="testpassword", email="testuser@example.com"
):
    user_data = {"username": username, "password": password, "email": email}
    return client.post("/api/users/register", json=user_data)


def test_register_user(setup_database):
    # Test successful registration
    user_data = {
        "username": "newuser",
        "password": "newpassword",
        "email": "newuser@example.com",
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    # Check that the password is not returned
    assert "password" not in data and "hashed_password" not in data

    # Test registering an existing user
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

    # Test registering a user with a different username but the same email
    user_data["username"] = "anotheruser"
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_user(setup_database):
    # First, register a new user
    create_test_user()

    # Test successful login
    login_data = {"username": "testuser@example.com", "password": "testpassword"}
    response = client.post("/api/users/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Test login with incorrect credentials
    invalid_login_data = {
        "username": "testuser@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/api/users/login", data=invalid_login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_get_current_user(setup_database):
    # Register and log in a user
    create_test_user()
    login_data = {"username": "testuser@example.com", "password": "testpassword"}
    login_response = client.post("/api/users/login", data=login_data)
    token = login_response.json()["access_token"]

    # Test getting the current user
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

    # Test getting current user with invalid token
    response = client.get(
        "api/users/me", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_token_expiration(setup_database, monkeypatch):
    # Register and log in a user
    create_test_user()

    # Mock a token that expires in the past
    monkeypatch.setattr(
        "backend.user.api_user.create_access_token",
        lambda db, data: jwt.encode(
            {
                "sub": "testuser",
                "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
                "iat": datetime.now(timezone.utc),
            },
            os.getenv("SECRET_KEY"),
            algorithm="HS256",
        ),
    )

    login_data = {"username": "testuser@example.com", "password": "testpassword"}
    login_response = client.post("/api/users/login", data=login_data)
    expired_token = login_response.json()["access_token"]

    # Try to access the protected route with an expired token
    response = client.get(
        "api/users/me", headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_user_already_exists(setup_database):
    # Register a user
    create_test_user()

    response = client.get("/api/users/exists/testuser")
    assert response.status_code == 200
    assert response.json()["exists"] is True

    response = client.get("/api/users/exists/nonexistentuser")
    assert response.status_code == 200
    assert response.json()["exists"] is False


def test_logout(setup_database):
    # Register and log in a user
    create_test_user()
    login_data = {"username": "testuser@example.com", "password": "testpassword"}
    login_response = client.post("/api/users/login", data=login_data)
    token = login_response.json()["access_token"]

    # Test logging out
    response = client.post(
        "/api/users/logout", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Successfully logged out"}

    # Test logging out with an invalid token
    response = client.post(
        "/api/users/logout", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

    # Test that the token is no longer valid
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

    # Test logging out when not logged in
    response = client.post("/api/users/logout")
    assert response.status_code == 401
