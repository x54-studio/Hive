"""
References: backend/__docs__/useCases/article/UseCase_ListArticles.md

Test Scenarios:
1. Successful retrieval of articles using default pagination (limit = 2).
   - With at least 3 articles, GET /api/articles should return 2 articles.
2. Successful retrieval using custom pagination parameters.
   - For example, GET /api/articles?page=2&limit=2 should return articles 3 and 4.
3. Handling of invalid pagination parameters.
   - Expect GET /api/articles?page=abc to return a 400 error.
"""

import unittest
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestListArticles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Connect to the test database
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        # Clear the articles collection
        cls.test_db.articles.delete_many({})

        # Insert multiple test articles (ensure at least 3 exist)
        articles = []
        for i in range(1, 6):  # Insert 5 articles
            articles.append({
                "title": f"Test Article {i}",
                "content": f"This is the content for article {i}.",
                "author": "test_author",
                "created_at": "Fri, 28 Feb 2025 01:56:08 GMT",
                "updated_at": "Fri, 28 Feb 2025 01:56:08 GMT"
            })
        result = cls.test_db.articles.insert_many(articles)
        cls.inserted_ids = [str(_id) for _id in result.inserted_ids]

    def test_list_articles_default(self):
        """Test retrieval with default pagination (limit = 2)."""
        resp = self.client.get("/api/articles")
        self.assertEqual(resp.status_code, 200, "Expected 200 status when listing articles")
        data = resp.get_json()
        self.assertIsInstance(data, list, "Response should be a list of articles")
        self.assertEqual(len(data), 2, "Should return the default limit of 2 articles")
        for article in data:
            self.assertIn("article_id", article)
            self.assertIn("title", article)
            self.assertIn("content", article)
            self.assertIn("author", article)
            self.assertIn("created_at", article)
            self.assertIn("updated_at", article)

    def test_list_articles_custom_pagination(self):
        """Test retrieval using custom pagination parameters."""
        # For page=2, limit=2, expected articles are the 3rd and 4th inserted ones.
        resp = self.client.get("/api/articles?page=2&limit=2")
        self.assertEqual(resp.status_code, 200, "Expected 200 status with custom pagination")
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2, "Should return 2 articles on page 2 with limit=2")
        expected_titles = ["Test Article 3", "Test Article 4"]
        returned_titles = [article["title"] for article in data]
        self.assertEqual(returned_titles, expected_titles, "Returned articles should match expected pagination")

    def test_list_articles_invalid_parameters(self):
        """Test that invalid pagination parameters result in a 400 error."""
        resp = self.client.get("/api/articles?page=abc")
        self.assertEqual(resp.status_code, 400, "Expected 400 status when pagination parameters are invalid")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("invalid pagination", data["error"].lower())

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
