import os
import unittest
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestTokensInCookiesIfNotTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Force TESTING=False so we can verify that tokens
        are not in the JSON response in this mode.
        """
        # Backup the original TESTING setting
        cls.original_testing = Config.TESTING
        
        # Force TESTING=False
        Config.TESTING = False
        
        # Create app and test client
        cls.app = create_app()
        cls.client = cls.app.test_client()
        
        # Connect to test DB
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        
        # Clear existing users
        cls.test_db.users.delete_many({})
        
        # Register a test user
        user_data = {
            "username": "notTestingUser",
            "email": "notTesting@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=user_data)
        
    def test_tokens_in_cookies_if_not_testing(self):
        """
        Verifies that if Config.TESTING=False,
        the tokens are NOT included in JSON and
        are only set in HTTP-only cookies.
        """
        login_data = {
            "username_or_email": "notTesting@example.com",
            "password": "password123"
        }
        login_resp = self.client.post("/api/login", json=login_data)
        
        self.assertEqual(login_resp.status_code, 200, "Login should succeed when not testing.")
        
        json_data = login_resp.get_json()
        
        # Tokens should NOT appear in the JSON if TESTING=False
        self.assertNotIn("access_token", json_data, 
            "Should not include access_token in JSON when TESTING=False")
        self.assertNotIn("refresh_token", json_data, 
            "Should not include refresh_token in JSON when TESTING=False")
        
        # Check that tokens were set in cookies
        set_cookie_headers = login_resp.headers.get_all("Set-Cookie")
        self.assertTrue(any("access_token=" in h for h in set_cookie_headers),
            "Expected access_token cookie when TESTING=False")
        self.assertTrue(any("refresh_token=" in h for h in set_cookie_headers),
            "Expected refresh_token cookie when TESTING=False")

    @classmethod
    def tearDownClass(cls):
        # Restore the original TESTING value
        Config.TESTING = cls.original_testing
        
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
