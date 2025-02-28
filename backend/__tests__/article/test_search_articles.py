"""
References: backend/__docs__/useCases/article/UseCase_SearchArticles.md

Test Scenarios:
1. Successful search: Given a search query that matches one or more articles, 
   expect GET /api/articles/search?query=... to return a 200 status and a non-empty array of articles.
2. No matches: Given a search query that matches no articles, expect a 200 status with an empty array.
3. Invalid parameters: If the search query is missing (or invalid), expect a 400 error with an appropriate message.
"""

import unittest
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestSearchArticles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()
        
        # Connect to test DB
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        # Clear articles collection
        cls.test_db.articles.delete_many({})

        # Insert several test articles.
        articles = [
            {
                "title": "Breaking News: Python Takes Over",
                "content": "Python is now the world's most popular programming language.",
                "author": "reporter1",
                "created_at": "Fri, 28 Feb 2025 01:56:08 GMT",
                "updated_at": "Fri, 28 Feb 2025 01:56:08 GMT"
            },
            {
                "title": "Flask vs Django: A Comparative Analysis",
                "content": "An in-depth comparison of Flask and Django frameworks.",
                "author": "reporter2",
                "created_at": "Fri, 28 Feb 2025 02:00:00 GMT",
                "updated_at": "Fri, 28 Feb 2025 02:00:00 GMT"
            },
            {
                "title": "Local News: Community Garden Flourishes",
                "content": "The community garden project shows great promise.",
                "author": "reporter3",
                "created_at": "Fri, 28 Feb 2025 02:10:00 GMT",
                "updated_at": "Fri, 28 Feb 2025 02:10:00 GMT"
            },
            {
                "title": "Tech Insights: AI Revolution",
                "content": "The AI revolution is transforming industries.",
                "author": "reporter4",
                "created_at": "Fri, 28 Feb 2025 02:15:00 GMT",
                "updated_at": "Fri, 28 Feb 2025 02:15:00 GMT"
            }
        ]
        result = cls.test_db.articles.insert_many(articles)
        cls.inserted_ids = [str(_id) for _id in result.inserted_ids]

    def test_search_articles_success(self):
        """Test that a valid search query returns matching articles."""
        # Search for articles containing the keyword "Python"
        resp = self.client.get("/api/articles/search?query=Python")
        self.assertEqual(resp.status_code, 200, "Expected 200 status for valid search")
        data = resp.get_json()
        self.assertIsInstance(data, list, "Expected a list of articles")
        # Expect at least one article that mentions Python
        self.assertTrue(any("Python" in article["title"] or "Python" in article["content"]
                            for article in data), "Expected at least one matching article")

    def test_search_articles_no_matches(self):
        """Test that a search query with no matching articles returns an empty list."""
        resp = self.client.get("/api/articles/search?query=nonexistentkeyword")
        self.assertEqual(resp.status_code, 200, "Expected 200 status even when no matches")
        data = resp.get_json()
        self.assertIsInstance(data, list, "Expected a list of articles")
        self.assertEqual(len(data), 0, "Expected an empty list for a query with no matches")

    def test_search_articles_invalid_parameters(self):
        """Test that a missing query parameter results in a 400 error."""
        resp = self.client.get("/api/articles/search")
        self.assertEqual(resp.status_code, 400, "Expected 400 status when query parameter is missing")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("missing", data["error"].lower())


    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
