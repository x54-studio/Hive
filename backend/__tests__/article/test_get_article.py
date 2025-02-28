"""
References: backend/__docs__/useCases/article/UseCase_GetArticle.md

Test Scenarios:
1. Successful retrieval of an existing article.
   - Expect GET /api/articles/<article_id> to return 200 status with article details.
2. Retrieval of a non-existent article returns a 404 error.
"""

import unittest
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestGetArticle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Enable testing mode and create app
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Setup test database connection
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        cls.test_db.articles.delete_many({})  # Clear articles collection

        # Insert an article for testing
        article = {
            "title": "Sample Article",
            "content": "This is a sample article for testing.",
            "author": "test_author",
            # Using RFC1123 format for timestamps as stored by your app
            "created_at": "Fri, 28 Feb 2025 01:56:08 GMT",
            "updated_at": "Fri, 28 Feb 2025 01:56:08 GMT"
        }
        result = cls.test_db.articles.insert_one(article)
        cls.article_id = str(result.inserted_id)

    def test_get_article_success(self):
        resp = self.client.get(f"/api/articles/{self.article_id}")
        self.assertEqual(resp.status_code, 200, "Expected 200 status when retrieving an existing article")
        data = resp.get_json()
        # Check that all required keys are present and match expectations.
        self.assertIn("article_id", data)
        self.assertIn("title", data)
        self.assertIn("content", data)
        self.assertIn("author", data)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)
        self.assertEqual(data["article_id"], self.article_id)

    def test_get_article_not_found(self):
        # Use an ObjectId that is unlikely to exist
        resp = self.client.get("/api/articles/000000000000000000000000")
        self.assertEqual(resp.status_code, 404, "Expected 404 status for non-existent article")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("article not found", data["error"].lower())

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
