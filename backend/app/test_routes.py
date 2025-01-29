import pytest
from flask import Flask
from app import create_app  # Import your Flask app factory function
from flask_jwt_extended import create_access_token # type: ignore


@pytest.fixture
def client():
    """
    Fixture to create a test client for the Flask app.
    Returns:
        A Flask test client.
    """
    app = create_app()  # Create the app instance
    app.config["TESTING"] = True  # Enable testing mode
    with app.test_client() as client:
        yield client


def test_home(client):
    """
    Test the home route ("/").
    Verifies that the endpoint returns a welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to Hive!"}


def test_get_articles(client):
    """
    Test the /api/articles endpoint.
    Verifies that the response contains a list of articles.
    """
    response = client.get("/api/articles")
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Articles should be a list


def test_login_success(client):
    """
    Test the /api/login endpoint with valid credentials.
    Verifies that the response contains a valid access token.
    """
    payload = {"username": "admin", "password": "password"}
    response = client.post("/api/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_failure(client):
    """
    Test the /api/login endpoint with invalid credentials.
    Verifies that the response returns an error.
    """
    payload = {"username": "wrong_user", "password": "wrong_pass"}
    response = client.post("/api/login", json=payload)
    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}


def test_protected_route_without_token(client):
    """
    Test the /api/protected endpoint without a token.
    Verifies that access is denied.
    """
    response = client.get("/api/protected")
    assert response.status_code == 401  # Unauthorized


def test_protected_route_with_token(client):
    """
    Test the /api/protected endpoint with a valid token.
    Verifies that access is granted.
    """
    # Generate a valid JWT token
    with client.application.app_context():
        access_token = create_access_token(identity="admin")

    # Send the token in the Authorization header
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/protected", headers=headers)
    assert response.status_code == 200
    assert response.json == {"message": "You have access!"}
