"""
References: backend/docs/useCases/user/UseCase_RefreshToken.md

Tests:
1. Successful refresh with a valid refresh token in HTTP-only cookie
2. Missing refresh token cookie -> expect 401
3. Invalid refresh token -> expect 401
4. Expired refresh token -> expect 401
"""
import os
os.environ["JWT_REFRESH_TOKEN_EXPIRES"] = "-1"  # Force refresh tokens to expire immediately for this test

import unittest
import time
import datetime
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
from app import create_app
from app.config import Config
from services.user_service import UserService
from pymongo import MongoClient

class TestRefreshToken(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Override refresh token TTL for testing purposes
        #import os
        #os.environ["JWT_REFRESH_TOKEN_EXPIRES"] = "1"  # Token expires in 1 second
        #os.environ["TESTING"] = "true"
        #cls.config = Config()

        # Enable testing
        # Config.JWT_ACCESS_TOKEN_EXPIRES = 1
        # Config.JWT_REFRESH_TOKEN_EXPIRES = 2
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # DB setup
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        cls.test_db.users.delete_many({})  # Clear existing data

        # Set up user service & create a test user
        cls.user_service = UserService(Config)
        cls.user_service.register_user(
            username="refreshtester",
            email="refreshtester@example.com",
            password="password123"
        )

        # Log in the user to get valid tokens
        login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "refreshtester", "password": "password123"}
        )
        # Use a simple assert statement here:
        assert login_resp.status_code == 200, "Login should succeed for setup"

        data = login_resp.get_json()
        cls.access_token = data["access_token"]
        cls.refresh_token = data["refresh_token"]

        # Also extract cookies from the login response
        cls.cookies = {}
        for header in login_resp.headers.get_all("Set-Cookie"):
            # e.g. "refresh_token=abc123; Path=/; HttpOnly"
            cookie_pair = header.split(";")[0]
            key, value = cookie_pair.split("=")
            cls.cookies[key] = value


    def tearDown(self):
        # Clean up anything needed after each test
        # (Optional, depends on how you want to isolate data)
        pass

    def test_refresh_success(self):
        import os
        # Override TTL for this test so the token remains valid
        os.environ["JWT_REFRESH_TOKEN_EXPIRES"] = "60"  # Set TTL to 60 seconds for this test

        # Create a fresh app instance so that the new TTL is applied
        fresh_app = create_app()
        fresh_client = fresh_app.test_client()

        # Optionally, register the test user if not already registered.
        # For example:
        fresh_client.post(
            "/api/register",
            json={"username": "refreshtester", "email": "refreshtester@example.com", "password": "password123"}
        )

        login_resp = fresh_client.post(
            "/api/login",
            json={"username_or_email": "refreshtester", "password": "password123"}
        )
        self.assertEqual(login_resp.status_code, 200, "Login should succeed for valid token test")
        data = login_resp.get_json()
        self.assertIn("refresh_token", data)
        valid_refresh_token = data["refresh_token"]

        # Clear any existing refresh token cookie and set the one we just received
        fresh_client.delete_cookie("refresh_token", domain="localhost")
        fresh_client.set_cookie("refresh_token", valid_refresh_token, domain="localhost")

        resp = fresh_client.post("/api/refresh")
        # Expect 200 since token is still valid (TTL is now 60 sec)
        self.assertEqual(resp.status_code, 200, "Should succeed with valid refresh token")
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Token refreshed successfully")


    def test_refresh_missing_cookie(self):
        """
        Alternate Flow:
        No refresh_token cookie -> 401
        """
        # Remove any existing refresh cookie from the client
        self.client.delete_cookie("refresh_token", domain="localhost")

        resp = self.client.post("/api/refresh")  # No Cookie header
        self.assertEqual(resp.status_code, 401)
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("Missing refresh token", data["error"])

    def test_refresh_invalid_token(self):
        """
        Alternate Flow:
        Provide a token that is not expired but is signed with a wrong key.
        Expect the refresh logic to return a 401 with "Invalid refresh token".
        """
        from datetime import datetime, timedelta, timezone
        # Create a token that is valid (expiration in the future) but sign it with a wrong secret.
        now = datetime.now(timezone.utc)
        invalid_payload = {
            "sub": "refreshtester",
            "email": "refreshtester@example.com",
            "iat": now.timestamp(),
            "exp": (now + timedelta(seconds=100)).timestamp(),  # valid in future
        }
        # Sign with an incorrect key ("wrong_secret") instead of Config.JWT_SECRET_KEY.
        invalid_token = jwt.encode(invalid_payload, "wrong_secret", algorithm=Config.JWT_ALGORITHM)
        
        # Ensure no valid token cookie is lingering.
        self.client.delete_cookie("refresh_token", domain="localhost")
        self.client.set_cookie("refresh_token", invalid_token, domain="localhost")
        
        resp = self.client.post("/api/refresh")
        self.assertEqual(resp.status_code, 401)
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("Invalid refresh token", data["error"])


    def test_refresh_expired_token(self):
        from datetime import datetime, timedelta, timezone
        # Remove any existing refresh cookie from the client
        self.client.delete_cookie("refresh_token", domain="localhost")

        now = datetime.now(timezone.utc)
        expired_payload = {
            "sub": "refreshtester",
            "email": "refreshtester@example.com",
            "iat": (now - timedelta(seconds=200)).timestamp(),  # issued 200 sec ago
            "exp": (now - timedelta(seconds=100)).timestamp(),  # expired 100 sec ago
        }
        expired_token = jwt.encode(expired_payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

        # Set the expired token cookie on the client
        self.client.set_cookie("refresh_token", expired_token, domain="localhost")

        resp = self.client.post("/api/refresh")
        self.assertEqual(resp.status_code, 401)
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("expired", data["error"].lower())


        @classmethod
        def tearDownClass(cls):
            cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
            cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
