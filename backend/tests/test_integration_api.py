import os
import unittest
import json
from pymongo import MongoClient
from app import create_app
from app.config import Config
from tests.integration_seeder import seed_users, seed_articles


class IntegrationAPITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["TESTING"] = "true"
        cls.config = Config()
        cls.mongo_client = MongoClient(cls.config.TEST_MONGO_URI)
        cls.test_db = cls.mongo_client.get_database(cls.config.TEST_MONGO_DB_NAME)
        # Seed the test database with initial data
        seed_users()
        seed_articles()
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def get_auth_cookie_header(self, user_email, user_password, username="adminuser"):
        # Register user
        register_data = {
            "username": username,
            "email": user_email,
            "password": user_password
        }
        reg_response = self.client.post("/api/register", json=register_data)
        self.assertEqual(reg_response.status_code, 201)

        # Login user and extract cookies
        login_data = {
            "email": user_email,
            "password": user_password
        }
        login_response = self.client.post("/api/login", json=login_data)
        self.assertEqual(login_response.status_code, 200)
        cookies = {}
        for header in login_response.headers.get_all("Set-Cookie"):
            key_value = header.split(";")[0]
            key, value = key_value.split("=")
            cookies[key] = value
        self.assertIn("access_token", cookies)
        self.assertIn("refresh_token", cookies)
        return f"access_token={cookies['access_token']}; refresh_token={cookies['refresh_token']}"

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("message", data)

    def test_register_and_login_workflow(self):
        register_data = {
            "username": "newadmin",
            "email": "newadmin@example.com",
            "password": "password123"
        }
        response = self.client.post("/api/register", json=register_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertIn("user_id", data)

        login_data = {
            "email": "newadmin@example.com",
            "password": "password123"
        }
        response = self.client.post("/api/login", json=login_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)
        self.assertIn("refresh_token", data)
        self.assertIn("message", data)

    def test_token_refresh_and_protected_endpoint(self):
        # Register and login a user for token refresh testing
        register_data = {
            "username": "refreshtester",
            "email": "refreshtester@example.com",
            "password": "password123"
        }
        self.client.post("/api/register", json=register_data)
        login_data = {
            "email": "refreshtester@example.com",
            "password": "password123"
        }
        login_response = self.client.post("/api/login", json=login_data)
        self.assertEqual(login_response.status_code, 200)

        # Extract refresh token from cookies
        refresh_token = None
        for cookie in login_response.headers.get_all("Set-Cookie"):
            if "refresh_token=" in cookie:
                parts = cookie.split(";")[0].split("=")
                if len(parts) == 2:
                    refresh_token = parts[1]
                break
        self.assertIsNotNone(refresh_token, "Refresh token not found in cookies")

        refresh_response = self.client.post("/api/refresh")
        self.assertEqual(refresh_response.status_code, 200)
        refresh_data = json.loads(refresh_response.data)
        self.assertIn("access_token", refresh_data)
        self.assertIn("refresh_token", refresh_data)

        cookie_header = (
            f"access_token={refresh_data['access_token']}; "
            f"refresh_token={refresh_data['refresh_token']}"
        )
        protected_response = self.client.get(
            "/api/protected",
            headers={"Cookie": cookie_header}
        )
        self.assertEqual(protected_response.status_code, 200)
        protected_data = json.loads(protected_response.data)
        self.assertIn("username", protected_data)
        self.assertIn("role", protected_data)

    def test_articles_crud(self):
        # Use helper to register and log in admin user and obtain auth header
        cookie_header = self.get_auth_cookie_header("adminuser@example.com", "adminpass")

        # Create Article
        article_data = {
            "title": "Integration Test Article",
            "content": "This is a test article content."
        }
        create_response = self.client.post(
            "/api/articles", json=article_data, headers={"Cookie": cookie_header}
        )
        self.assertEqual(create_response.status_code, 201)
        create_data = json.loads(create_response.data)
        self.assertIn("article_id", create_data)
        article_id = create_data["article_id"]

        # Get Article by ID
        get_response = self.client.get(f"/api/articles/{article_id}")
        self.assertEqual(get_response.status_code, 200)
        get_data = json.loads(get_response.data)
        self.assertEqual(get_data.get("title"), "Integration Test Article")

        # Update Article
        update_data = {"title": "Updated Integration Article"}
        update_response = self.client.put(
            f"/api/articles/{article_id}", json=update_data, headers={"Cookie": cookie_header}
        )
        self.assertEqual(update_response.status_code, 200)
        update_resp_data = json.loads(update_response.data)
        self.assertIn("message", update_resp_data)

        # Verify Update
        get_response = self.client.get(f"/api/articles/{article_id}")
        self.assertEqual(get_response.status_code, 200)
        get_data = json.loads(get_response.data)
        self.assertEqual(get_data.get("title"), "Updated Integration Article")

        # Delete Article
        delete_response = self.client.delete(
            f"/api/articles/{article_id}", headers={"Cookie": cookie_header}
        )
        self.assertEqual(delete_response.status_code, 200)
        delete_data = json.loads(delete_response.data)
        self.assertIn("message", delete_data)

        # Verify Deletion
        get_response = self.client.get(f"/api/articles/{article_id}")
        self.assertEqual(get_response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(cls.config.TEST_MONGO_DB_NAME)
        cls.mongo_client.close()


if __name__ == "__main__":
    unittest.main()
