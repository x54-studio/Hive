"""
References: backend/__docs__/useCases/user/UseCase_DeleteUser.md

Test Scenarios:
1. Successful deletion of an existing user.
   - Expect DELETE /api/users/<email> to return status 200 with
     {"message": "User deleted successfully"}.
   - A subsequent login attempt for the deleted user should fail.
2. Attempting to delete a non-existent user returns a 404 with an appropriate error.
"""

import unittest
import json
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestDeleteUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()
        
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        cls.test_db.users.delete_many({})  # Clean any pre-existing users

        # Register a test user that we will delete
        cls.client.post(
            "/api/register",
            json={
                "username": "deleteuser",
                "email": "deleteuser@example.com",
                "password": "password123"
            }
        )
        # Log in to get authentication cookie
        cls.login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "deleteuser", "password": "password123"}
        )
        
        # Extract cookies from login response (assuming tokens are set in cookies)
        cls.cookies = {}
        for header in cls.login_resp.headers.get_all("Set-Cookie"):
            cookie_pair = header.split(";")[0]
            key, value = cookie_pair.split("=")
            cls.cookies[key] = value

    def test_delete_user_success(self):
        # Issue DELETE request using the username (not email)
        resp = self.client.delete(
            "/api/users/deleteuser",
            headers={"Cookie": f"access_token={self.cookies.get('access_token')}"}
        )
        self.assertEqual(resp.status_code, 200, "Expected 200 status on successful deletion")
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "User deleted successfully")
    
        # Optionally, attempt to log in again and verify that it fails.
        login_again_resp = self.client.post(
            "/api/login",
            json={"username_or_email": "deleteuser", "password": "password123"}
        )
        self.assertNotEqual(login_again_resp.status_code, 200, "Deleted user should not be able to log in")

    def test_delete_user_not_found(self):
        # Attempt to delete a user that doesn't exist.
        resp = self.client.delete(
            "/api/users/nonexistent@example.com",
            headers={"Cookie": f"access_token={self.cookies.get('access_token')}"}
        )
        self.assertEqual(resp.status_code, 404, "Expected 404 status for non-existent user deletion")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("not found", data["error"].lower())


    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
