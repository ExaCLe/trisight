import os
from datetime import timedelta, timezone, datetime
from unittest.mock import patch

import pytest
import jwt
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import models
from backend.models import Base
from backend.main import app
from backend.user.api_user import get_user
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


def test_forgot_password_email_sent(setup_database):
    # Create a test user
    create_test_user()

    # Mock the email sending function
    with patch("backend.user.api_user.send_password_reset_email") as mock_send_email:
        # Request password reset
        email = "testuser@example.com"
        response = client.post("/api/users/forgot-password", json={"email": email})

        # Check that the response is successful
        assert response.status_code == 200
        assert response.json() == {"msg": "Password reset email sent"}

        # Check that the email sending function was called once
        mock_send_email.assert_called_once_with(email, mock_send_email.call_args[0][1])


def test_forgot_password_user_not_found(setup_database):
    # Test requesting password reset for a non-existent user
    invalid_email = "nonexistent@example.com"
    response = client.post("/api/users/forgot-password", json={"email": invalid_email})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_reset_password_valid_token(setup_database):
    # Create a test user
    create_test_user()

    # Mock the email sending function
    with patch("backend.user.api_user.send_password_reset_email") as mock_send_email:
        # Request a password reset
        email = "testuser@example.com"
        forgot_response = client.post(
            "/api/users/forgot-password", json={"email": email}
        )
        assert forgot_response.status_code == 200

    # Retrieve the reset token from the database
    db = next(override_get_db())
    user = get_user(db, email)
    reset_token = (
        db.query(models.PasswordResetToken).filter_by(user_id=user.id).first().token
    )

    # Use the reset token to reset the password
    new_password = "newtestpassword"
    reset_response = client.post(
        "/api/users/reset-password",
        json={"token": reset_token, "new_password": new_password},
    )
    assert reset_response.status_code == 200
    assert reset_response.json() == {"msg": "Password has been reset"}

    # Log in with the new password
    login_data = {"username": "testuser@example.com", "password": new_password}
    login_response = client.post("/api/users/login", data=login_data)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_reset_password_invalid_token(setup_database):
    # Create a test user
    create_test_user()

    # Try to reset password with an invalid token
    new_password = "newtestpassword"
    invalid_token = "invalid_token"
    response = client.post(
        "/api/users/reset-password",
        json={"token": invalid_token, "new_password": new_password},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or expired token"}


def test_reset_password_expired_token(setup_database, monkeypatch):
    # Create a test user
    create_test_user()

    # Mock the email sending function
    with patch("backend.user.api_user.send_password_reset_email") as mock_send_email:
        # Request a password reset
        email = "testuser@example.com"
        forgot_response = client.post(
            "/api/users/forgot-password", json={"email": email}
        )
        assert forgot_response.status_code == 200

    # Retrieve the reset token from the database
    db = next(override_get_db())
    user = get_user(db, email)
    reset_token = db.query(models.PasswordResetToken).filter_by(user_id=user.id).first()
    reset_token.expires_at = datetime.utcnow() - timedelta(hours=1)
    db.commit()

    # Try to use the expired token to reset the password
    new_password = "newtestpassword"
    response = client.post(
        "/api/users/reset-password",
        json={"token": reset_token.token, "new_password": new_password},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or expired token"}
