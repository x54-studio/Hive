# backend/tests/test_article_service.py
import os
import unittest
from pymongo import MongoClient
from services.article_service import ArticleService
from repositories.mongo_article_repository import MongoArticleRepository
from app.config import Config

class TestArticleService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["TESTING"] = "true"
        cls.config = Config()
        # Use the global client from Config for test setup.
        cls.mongo_client = MongoClient(cls.config.MONGO_URI)
        cls.test_db = cls.mongo_client.get_database(cls.config.MONGO_DB_NAME)

    def setUp(self):
        self.repo = MongoArticleRepository()
        self.service = ArticleService(repository=self.repo)
        self.author = "test_author"
        self.repo.articles.delete_many({})

    def tearDown(self):
        self.repo.articles.delete_many({})

    def test_create_article_success(self):
        result = self.service.create_article("Test Title", "Test Content", self.author)
        self.assertIn("message", result)
        self.assertIn("article_id", result)
        article = self.service.get_article_by_id(result["article_id"])
        self.assertIsNotNone(article)
        self.assertIn("title", article)
        self.assertEqual(article["title"], "Test Title")

    def test_create_article_failure(self):
        result = self.service.create_article("fail", "Test Content", self.author)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Error creating article")

    def test_get_all_articles(self):
        self.service.create_article("Title1", "Content1", self.author)
        self.service.create_article("Title2", "Content2", self.author)
        articles = self.service.get_all_articles()
        self.assertGreaterEqual(len(articles), 2)

    def test_get_article_by_id_success(self):
        result = self.service.create_article("Title", "Content", self.author)
        article_id = result["article_id"]
        article = self.service.get_article_by_id(article_id)
        self.assertIsNotNone(article)
        self.assertIn("title", article)
        self.assertEqual(article["title"], "Title")

    def test_get_article_by_id_not_found(self):
        article = self.service.get_article_by_id("000000000000000000000000")
        self.assertIsNone(article)

    def test_update_article_success(self):
        result = self.service.create_article("Old Title", "Old Content", self.author)
        article_id = result["article_id"]
        update_result = self.service.update_article(
            article_id, title="New Title", content="New Content"
        )
        self.assertIn("message", update_result)
        article = self.service.get_article_by_id(article_id)
        self.assertIsNotNone(article)
        self.assertIn("title", article)
        self.assertEqual(article["title"], "New Title")
        self.assertEqual(article["content"], "New Content")

    def test_update_article_no_fields(self):
        result = self.service.create_article("Title", "Content", self.author)
        article_id = result["article_id"]
        update_result = self.service.update_article(article_id)
        self.assertIn("error", update_result)
        self.assertEqual(update_result["error"], "No update fields provided")

    def test_update_article_failure(self):
        update_result = self.service.update_article(
            "000000000000000000000000", title="New Title"
        )
        self.assertIn("error", update_result)
        self.assertEqual(update_result["error"], "Article not found or update failed")

    def test_delete_article_success(self):
        result = self.service.create_article("Title", "Content", self.author)
        article_id = result["article_id"]
        delete_result = self.service.delete_article(article_id)
        self.assertIn("message", delete_result)
        article = self.service.get_article_by_id(article_id)
        self.assertIsNone(article)

    def test_delete_article_failure(self):
        delete_result = self.service.delete_article("000000000000000000000000")
        self.assertIn("error", delete_result)
        self.assertEqual(delete_result["error"], "Article not found or deletion failed")

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(cls.config.MONGO_DB_NAME)
        cls.mongo_client.close()
        # Removed extra client.close() call since cls.mongo_client is our client.

if __name__ == "__main__":
    unittest.main()
