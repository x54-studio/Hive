"""
References: backend/__docs__/useCases/user/UseCase_LogoutUser.md

Test Scenarios:
1. Successful logout: After login, calling POST /api/logout clears the access and refresh tokens.
   - Expect a 200 status code.
   - Expect the JSON response to include a "Logged out successfully" message.
   - Expect the response headers to contain Set-Cookie directives that clear the tokens.
"""

import unittest
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestLogoutUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()

        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        cls.test_db.users.delete_many({})  # clear any pre-existing users

        # Register and log in a test user for logout test.
        cls.client.post(
            "/api/register",
            json={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "password123"
            }
        )
        cls.login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "testuser", "password": "password123"}
        )

    def test_logout_user(self):
        # Ensure login was successful and cookies were set.
        self.assertEqual(self.login_resp.status_code, 200)
        set_cookie_headers = self.login_resp.headers.get_all("Set-Cookie")
        cookies = {}
        for header in set_cookie_headers:
            cookie_pair = header.split(";")[0]
            key, value = cookie_pair.split("=")
            cookies[key] = value
        self.assertIn("access_token", cookies)
        self.assertIn("refresh_token", cookies)
        
        # Now, call the logout endpoint.
        resp = self.client.post("/api/logout")
        self.assertEqual(resp.status_code, 200, "Logout should return status 200")
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Logged out successfully")
        
        # Check that logout response includes headers to clear cookies.
        logout_set_cookie_headers = resp.headers.get_all("Set-Cookie")
        self.assertTrue(
            any("access_token=" in header and ("Max-Age=0" in header or "expires=" in header)
                for header in logout_set_cookie_headers),
            "Expected access_token cookie to be cleared"
        )
        self.assertTrue(
            any("refresh_token=" in header and ("Max-Age=0" in header or "expires=" in header)
                for header in logout_set_cookie_headers),
            "Expected refresh_token cookie to be cleared"
        )

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
