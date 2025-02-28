"""
References: backend/__docs__/useCases/article/UseCase_CreateArticle.md

Test Scenarios:
1. Successful creation of an article by a moderator or admin.
2. Failure when required fields are missing.
3. Unauthorized creation attempt by a user with a role of regular.
"""

import unittest
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestCreateArticle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        # Clear collections.
        cls.test_db.users.delete_many({})
        cls.test_db.articles.delete_many({})

        # Register a moderator.
        moderator = {
            "username": "moduser",
            "email": "mod@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=moderator)
        # Force role update to moderator
        cls.test_db.users.update_one({"username": "moduser"}, {"$set": {"role": "moderator"}})

        # Register a regular user.
        regular = {
            "username": "regularuser",
            "email": "regular@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=regular)

    def get_access_token(self, username_or_email, password):
        """Helper to log in a user and return the access token from JSON."""
        resp = self.client.post(
            "/api/login",
            json={"username_or_email": username_or_email, "password": password}
        )
        self.assertEqual(resp.status_code, 200, "Login should succeed")
        data = resp.get_json()
        self.assertIn("access_token", data)
        return data["access_token"]

    def test_create_article_success(self):
        # Log in as moderator.
        access_token = self.get_access_token("moduser", "password123")
        article_data = {
            "title": "Test Article",
            "content": "This is the content of the test article."
        }
        headers = {"Cookie": f"access_token={access_token}"}
        resp = self.client.post("/api/articles", json=article_data, headers=headers)
        self.assertEqual(resp.status_code, 201, "Expected 201 status on successful creation")
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article created successfully")
        self.assertIn("article_id", data)

    def test_create_article_missing_fields(self):
        # Log in as moderator.
        access_token = self.get_access_token("moduser", "password123")
        # Provide article data missing the "title"
        article_data = {
            "content": "Content without a title."
        }
        headers = {"Cookie": f"access_token={access_token}"}
        resp = self.client.post("/api/articles", json=article_data, headers=headers)
        self.assertEqual(resp.status_code, 400, "Expected 400 status when required fields are missing")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("Missing title or content", data["error"])

    def test_create_article_unauthorized(self):
        # Log in as regular user (unauthorized to create articles)
        access_token = self.get_access_token("regularuser", "password123")
        article_data = {
            "title": "Unauthorized Article",
            "content": "This content should not be allowed for regular users."
        }
        headers = {"Cookie": f"access_token={access_token}"}
        resp = self.client.post("/api/articles", json=article_data, headers=headers)
        self.assertEqual(resp.status_code, 403, "Expected 403 Forbidden for unauthorized article creation")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("not authorized", data["error"].lower())

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
