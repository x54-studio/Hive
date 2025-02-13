"""
tests/test_user_service.py

Unit tests for UserService.
This file uses a dedicated test database (Config.TEST_MONGO_DB_NAME) by overriding the global
database instance in repositories/db.py. It includes tests for:
  - User registration.
  - Login with invalid credentials.
  - Verifying password hashing.
  - Ensuring that login returns valid JWT tokens.
  - Verifying that the refresh endpoint issues new tokens.
"""

import unittest
from services.user_service import UserService
from app.config import Config
import bcrypt
from pymongo import MongoClient
import repositories.db as db_module
import jwt

class TestUserService(unittest.TestCase):
    def setUp(self):

        # Instantiate UserService with positional parameters.
        self.user_service = UserService(
            Config.JWT_SECRET_KEY,
            Config.JWT_ALGORITHM,  # NOTE: Avoid duplicate jwt_access_expires? Check parameters.
            60,    # jwt_access_expires in seconds
            180,   # jwt_refresh_expires in seconds
            None,  # repository: default MongoUserRepository
        )

    def tearDown(self):
        # Clean up the test collection after each test.
        client = MongoClient(Config.TEST_MONGO_URI)
        test_db = client.get_database(Config.TEST_MONGO_DB_NAME)
        test_db.users.delete_many({})
        client.close()
        
    def test_register_user(self):
        result = self.user_service.register_user("testuser", "testuser@example.com", "password123")
        self.assertIn("message", result)
        self.assertEqual(result["message"], "User registered successfully!")
    
    def test_login_user_invalid_credentials(self):
        result = self.user_service.login_user("nonexistent@example.com", "password")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "User not found")
    
    def test_password_hashing(self):
        result = self.user_service.register_user("hashuser", "hash@example.com", "secret")
        self.assertIn("message", result)
        # Retrieve user details directly using the repository.
        from repositories.mongo_user_repository import MongoUserRepository
        repo = MongoUserRepository()
        user = repo.find_by_email("hash@example.com")
        self.assertNotEqual(user["password"], "secret")
        self.assertTrue(bcrypt.checkpw("secret".encode("utf-8"), user["password"]))

    def test_login_returns_tokens(self):
        # Register a new user and then login to verify tokens.
        self.user_service.register_user("tokenuser", "tokenuser@example.com", "mypassword")
        login_result = self.user_service.login_user("tokenuser@example.com", "mypassword")
        self.assertIn("access_token", login_result)
        self.assertIn("refresh_token", login_result)
        self.assertIn("message", login_result)
        # Decode the access token to verify payload contents.
        access_payload = jwt.decode(login_result["access_token"], Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        self.assertEqual(access_payload.get("sub"), "tokenuser")
        self.assertEqual(access_payload.get("email"), "tokenuser@example.com")

    def test_refresh_tokens(self):
        # Register and login a user to obtain tokens.
        self.user_service.register_user("refreshuser", "refreshuser@example.com", "secretpass")
        login_result = self.user_service.login_user("refreshuser@example.com", "secretpass")
        refresh_token = login_result["refresh_token"]
        # Call the refresh method.
        refresh_result = self.user_service.refresh_access_token(refresh_token)
        self.assertIn("access_token", refresh_result)
        self.assertIn("refresh_token", refresh_result)
        self.assertIn("message", refresh_result)
        # Ensure the new tokens are different from the original tokens.
        self.assertNotEqual(refresh_result["access_token"], login_result["access_token"])
        self.assertNotEqual(refresh_result["refresh_token"], refresh_token)

if __name__ == '__main__':
    unittest.main()
