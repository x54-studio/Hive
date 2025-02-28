"""
References: backend/__docs__/useCases/article/UseCase_DeleteArticle.md

Test Scenarios:
1. Successful deletion of an existing article.
   - Expect DELETE /api/articles/<article_id> to return 200 with a success message.
   - Subsequent GET /api/articles/<article_id> should return 404.
2. Attempting to delete a non-existent article returns a 404 error.
"""

import unittest
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestDeleteArticle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Enable testing and create the app and test client.
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()
        
        # Connect to the test database.
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        # Clear previous data.
        cls.test_db.users.delete_many({})
        cls.test_db.articles.delete_many({})

        # Register a moderator (authorized to delete articles).
        moderator = {
            "username": "moduser",
            "email": "mod@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=moderator)
        # Force the role to "moderator" if not set by default.
        cls.test_db.users.update_one({"username": "moduser"}, {"$set": {"role": "moderator"}})
        
        # Log in as the moderator.
        login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "moduser", "password": "password123"}
        )
        if login_resp.status_code != 200:
            raise Exception(f"Login failed with status {login_resp.status_code}")
        login_data = login_resp.get_json()
        cls.access_token = login_data["access_token"]

        # Create an article to delete.
        article_data = {
            "title": "Delete Test Article",
            "content": "Content of article to be deleted."
        }
        headers = {"Cookie": f"access_token={cls.access_token}"}
        create_resp = cls.client.post("/api/articles", json=article_data, headers=headers)
        if create_resp.status_code != 201:
            raise Exception(f"Article creation failed with status {create_resp.status_code}")
        create_data = create_resp.get_json()
        cls.article_id = create_data["article_id"]

    def test_delete_article_success(self):
        headers = {"Cookie": f"access_token={self.access_token}"}
        # Delete the article.
        resp = self.client.delete(f"/api/articles/{self.article_id}", headers=headers)
        self.assertEqual(resp.status_code, 200, "Expected 200 status on successful deletion")
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article deleted successfully")
        
        # Verify that retrieving the deleted article returns 404.
        get_resp = self.client.get(f"/api/articles/{self.article_id}")
        self.assertEqual(get_resp.status_code, 404, "Expected 404 status after article deletion")

    def test_delete_article_not_found(self):
        headers = {"Cookie": f"access_token={self.access_token}"}
        # Attempt to delete a non-existent article.
        resp = self.client.delete("/api/articles/000000000000000000000000", headers=headers)
        self.assertEqual(resp.status_code, 404, "Expected 404 status for non-existent article deletion")
        data = resp.get_json()
        self.assertIn("error", data)
        # Check error message case-insensitively.
        self.assertIn("not found", data["error"].lower())

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
