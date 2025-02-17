# backend/tests/test_article_service.py
import unittest
from services.article_service import ArticleService
from utilities.logger import get_logger

logger = get_logger(__name__)


class FakeArticleRepository:
    def __init__(self):
        self.articles = {}
        self.counter = 1

    def create_article(self, article_data):
        article_id = str(self.counter)
        self.counter += 1
        self.articles[article_id] = article_data.copy()
        self.articles[article_id]["_id"] = article_id
        return article_id

    def get_all_articles(self, skip=0, limit=10):
        articles = list(self.articles.values())
        return articles[skip:skip + limit]

    def get_article_by_id(self, article_id):
        return self.articles.get(article_id)

    def update_article(self, article_id, update_data):
        if article_id in self.articles:
            self.articles[article_id].update(update_data)
            return True
        return False

    def delete_article(self, article_id):
        if article_id in self.articles:
            del self.articles[article_id]
            return True
        return False


class TestArticleService(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up the ArticleService tests.")
        self.fake_repo = FakeArticleRepository()
        self.service = ArticleService(repository=self.fake_repo)
        self.author = "test_author"

    def test_create_article(self):
        result = self.service.create_article("Test Title", "Test Content", self.author)
        self.assertIn("message", result)
        self.assertIn("article_id", result)
        article_id = result["article_id"]
        article = self.fake_repo.get_article_by_id(article_id)
        self.assertIsNotNone(article)
        self.assertEqual(article["title"], "Test Title")
        self.assertEqual(article["author"], self.author)

    def test_get_all_articles(self):
        self.service.create_article("Title1", "Content1", self.author)
        self.service.create_article("Title2", "Content2", self.author)
        articles = self.service.get_all_articles()
        self.assertIsInstance(articles, list)
        self.assertGreaterEqual(len(articles), 2)

    def test_get_article_by_id(self):
        create_result = self.service.create_article("Title", "Content", self.author)
        article_id = create_result["article_id"]
        article = self.service.get_article_by_id(article_id)
        self.assertIsInstance(article, dict)
        self.assertEqual(article["title"], "Title")

    def test_update_article_success(self):
        create_result = self.service.create_article("Old Title", "Old Content", self.author)
        article_id = create_result["article_id"]
        update_result = self.service.update_article(
            article_id, title="New Title", content="New Content"
        )
        self.assertIn("message", update_result)
        article = self.fake_repo.get_article_by_id(article_id)
        self.assertEqual(article["title"], "New Title")
        self.assertEqual(article["content"], "New Content")

    def test_update_article_no_fields(self):
        create_result = self.service.create_article("Title", "Content", self.author)
        article_id = create_result["article_id"]
        update_result = self.service.update_article(article_id)
        self.assertIn("error", update_result)
        self.assertEqual(update_result["error"], "No update fields provided")

    def test_update_article_failure(self):
        update_result = self.service.update_article("nonexistent_id", title="New Title")
        self.assertIn("error", update_result)
        self.assertEqual(update_result["error"], "Article not found or update failed")

    def test_delete_article_success(self):
        create_result = self.service.create_article("Title", "Content", self.author)
        article_id = create_result["article_id"]
        delete_result = self.service.delete_article(article_id)
        self.assertIn("message", delete_result)
        self.assertIsNone(self.fake_repo.get_article_by_id(article_id))

    def test_delete_article_failure(self):
        delete_result = self.service.delete_article("nonexistent_id")
        self.assertIn("error", delete_result)
        self.assertEqual(delete_result["error"], "Article not found or deletion failed")


if __name__ == '__main__':
    unittest.main()
