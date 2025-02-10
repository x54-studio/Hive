# article_service.py

from datetime import datetime, timezone
from repositories.article_repository import ArticleRepository

class ArticleService:
    def __init__(self, mongo_uri, db_name="hive_db"):
        self.article_repo = ArticleRepository(mongo_uri, db_name)

    def create_article(self, title, content, author):
        article_data = {
            "title": title,
            "content": content,
            "author": author,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        article_id = self.article_repo.create_article(article_data)
        return {"message": "Article created successfully", "article_id": article_id}

    def get_all_articles(self, page=1, limit=10):
        skip = (page - 1) * limit
        articles = self.article_repo.get_all_articles(skip=skip, limit=limit)
        return articles

    def get_article_by_id(self, article_id):
        article = self.article_repo.get_article_by_id(article_id)
        if article:
            return article
        else:
            return {"error": "Article not found"}

    def update_article(self, article_id, title=None, content=None):
        update_data = {}
        if title:
            update_data["title"] = title
        if content:
            update_data["content"] = content
        if not update_data:
            return {"error": "No update fields provided"}
        update_data["updated_at"] = datetime.now(timezone.utc)
        success = self.article_repo.update_article(article_id, update_data)
        if success:
            return {"message": "Article updated successfully"}
        else:
            return {"error": "Article not found or update failed"}

    def delete_article(self, article_id):
        success = self.article_repo.delete_article(article_id)
        if success:
            return {"message": "Article deleted successfully"}
        else:
            return {"error": "Article not found or deletion failed"}

    def close(self):
        self.article_repo.close()
