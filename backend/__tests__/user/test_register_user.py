"""
References: backend/docs/useCases/user/UseCase_RegisterUser.md

This TDD test checks:
1. Successful registration with valid data
2. Failure if required fields are missing
3. Failure if user (email or username) already exists
"""

import unittest
from app import create_app
from app.config import Config
from services.user_service import UserService
from pymongo import MongoClient

class TestRegisterUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure we use the testing environment
        Config.TESTING = True  
        cls.app = create_app()
        cls.client = cls.app.test_client()
        # Connect to the test DB
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]

        # Clean up any existing test data
        cls.test_db.users.delete_many({})

        # Create an instance of the UserService (or use mock)
        cls.user_service = UserService(Config)

    def tearDown(self):
        # After each test, clear the users collection
        self.test_db.users.delete_many({})

    def test_register_user_success(self):
        """
        Main Flow:
        1. Provide username, email, password
        2. Expect 201 + success message
        """
        response = self.client.post(
            "/api/register",
            json={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "password123"
            }
        )
        self.assertEqual(response.status_code, 201, "Should return 201 for successful registration")
        data = response.get_json()
        self.assertIn("message", data)
        self.assertIn("user_id", data)

    def test_register_user_missing_fields(self):
        """
        Alternate Flow:
        Missing 'email' -> expect 400
        """
        response = self.client.post(
            "/api/register",
            json={
                "username": "no_email_here",
                # "email": "missing!",
                "password": "password123"
            }
        )
        self.assertEqual(response.status_code, 400, "Should return 400 if required fields are missing")
        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("Missing required fields", data["error"])

    def test_register_user_duplicate(self):
        """
        Alternate Flow:
        Duplicate email or username -> expect error
        """
        # First registration
        self.client.post(
            "/api/register",
            json={
                "username": "duplicateuser",
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        # Second registration with same username/email
        response = self.client.post(
            "/api/register",
            json={
                "username": "duplicateuser",
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        self.assertIn(response.status_code, [400, 409], "Should return 400 or 409 if user already exists")
        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("User already exists", data["error"])

    @classmethod
    def tearDownClass(cls):
        # Drop the entire test DB (optional)
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()


if __name__ == "__main__":
    unittest.main()
