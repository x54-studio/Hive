"""
References: backend/__docs__/useCases/article/UseCase_UpdateArticle.md

Test Scenarios:
1. Successful update of an existing article.
   - Expect PUT /api/articles/<article_id> with new title/content to return 200 and a success message.
   - Verify that the article's data is updated.
2. Failure when no update fields are provided.
   - Expect PUT /api/articles/<article_id> with an empty JSON body to return 400 with an appropriate error message.
"""

import unittest
import json
from app import create_app
from app.config import Config
from pymongo import MongoClient
from datetime import datetime

class TestUpdateArticle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()

        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        cls.test_db.users.delete_many({})
        cls.test_db.articles.delete_many({})

        # Register a moderator user.
        moderator = {
            "username": "moduser",
            "email": "mod@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=moderator)
        cls.test_db.users.update_one({"username": "moduser"}, {"$set": {"role": "moderator"}})

        # Log in as moderator to get an access token.
        login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "moduser", "password": "password123"}
        )
        if login_resp.status_code != 200:
            raise Exception(f"Login should succeed for moderator, got {login_resp.status_code}")
        login_data = login_resp.get_json()
        cls.access_token = login_data["access_token"]

        # Create an article to update.
        article_data = {
            "title": "Original Title",
            "content": "Original content."
        }
        headers = {"Cookie": f"access_token={cls.access_token}"}
        create_resp = cls.client.post("/api/articles", json=article_data, headers=headers)
        if create_resp.status_code != 201:
            raise Exception(f"Article creation should succeed, got {create_resp.status_code}")
        create_data = create_resp.get_json()
        cls.article_id = create_data.get("article_id")


    def test_update_article_success(self):
        # Prepare new data for update.
        update_data = {
            "title": "Updated Title",
            "content": "Updated content."
        }
        headers = {"Cookie": f"access_token={self.access_token}"}

        # Wait for 1 second to ensure updated_at will be later than created_at
        import time
        time.sleep(1)

        update_resp = self.client.put(f"/api/articles/{self.article_id}", json=update_data, headers=headers)
        self.assertEqual(update_resp.status_code, 200, "Expected 200 status on successful update")
        data = update_resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article updated successfully")

        # Now, retrieve the updated article using GET.
        get_resp = self.client.get(f"/api/articles/{self.article_id}")
        self.assertEqual(get_resp.status_code, 200, "Expected 200 status when retrieving the updated article")
        get_data = get_resp.get_json()
        self.assertEqual(get_data.get("title"), "Updated Title")
        self.assertEqual(get_data.get("content"), "Updated content.")

        # Optionally, check that updated_at is later than created_at.
        from email.utils import parsedate_to_datetime
        created_at = parsedate_to_datetime(get_data.get("created_at"))
        updated_at = parsedate_to_datetime(get_data.get("updated_at"))
        self.assertTrue(updated_at > created_at, "updated_at should be later than created_at")

    def test_update_article_no_fields(self):
        # Attempt to update with an empty JSON body.
        headers = {"Cookie": f"access_token={self.access_token}"}
        resp = self.client.put(f"/api/articles/{self.article_id}", json={}, headers=headers)
        self.assertEqual(resp.status_code, 400, "Expected 400 status when no update fields are provided")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("no data provided for update", data["error"].lower())

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
