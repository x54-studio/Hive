# tests/test_refresh.py
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from app import create_app  # Adjust import as needed

class RefreshTokenRotationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.jwt_secret_key = self.app.config["JWT_SECRET_KEY"]
        self.jwt_algorithm = self.app.config["JWT_ALGORITHM"]

        # Create a dummy refresh token for testing.
        self.username = "testuser"
        now = datetime.now(timezone.utc)
        self.dummy_refresh_token = jwt.encode(
            {
                "sub": self.username,
                "iat": now.timestamp(),
                "exp": (now + timedelta(days=7)).timestamp()
            },
            self.jwt_secret_key,
            algorithm=self.jwt_algorithm
        )
        # Hash the dummy refresh token.
        self.hashed_dummy_refresh = bcrypt.hashpw(
            self.dummy_refresh_token.encode("utf-8"), bcrypt.gensalt()
        )

    @patch("jwt.decode", return_value={"sub": "testuser"})
    @patch("repositories.mongo_user_repository.MongoUserRepository.find_by_username",
           return_value={"username": "testuser", "email": "testuser@example.com", "role": "admin"})
    @patch("repositories.mongo_user_repository.MongoUserRepository.get_refresh_token")
    @patch("repositories.mongo_user_repository.MongoUserRepository.store_refresh_token")
    def test_refresh_token_rotation_success(self, mock_store_refresh, mock_get_refresh, mock_find_by_username, mock_jwt_decode):
        # Setup: simulate that the stored refresh token hash matches our dummy.
        mock_get_refresh.return_value = self.hashed_dummy_refresh

        # Set the refresh token cookie.
        with self.app.test_request_context():
            self.client.set_cookie("refresh_token", self.dummy_refresh_token)

        # Call the refresh endpoint.
        response = self.client.post("/api/refresh")
        self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}: {response.data.decode()}")
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Token refreshed successfully")
        self.assertIn("access_token", data)
        self.assertIn("refresh_token", data)

        # Verify that store_refresh_token was called to rotate the refresh token.
        mock_store_refresh.assert_called_once_with(self.username, unittest.mock.ANY)

    @patch("repositories.mongo_user_repository.MongoUserRepository.get_refresh_token")
    def test_refresh_token_rotation_failure_invalid_token(self, mock_get_refresh):
        # Setup: simulate an invalid stored token.
        mock_get_refresh.return_value = None  # No token stored

        with self.app.test_request_context():
            self.client.set_cookie("refresh_token", self.dummy_refresh_token)

        # Call the refresh endpoint.
        response = self.client.post("/api/refresh")
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("Invalid refresh token", data["error"])

if __name__ == "__main__":
    unittest.main()
