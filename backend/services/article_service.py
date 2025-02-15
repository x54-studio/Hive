import logging
from datetime import datetime, timezone
from repositories.mongo_article_repository import MongoArticleRepository

logger = logging.getLogger(__name__)


class ArticleService:
    def __init__(self, repository=None):
        self.repo = repository if repository is not None else MongoArticleRepository()
        logger.info("ArticleService initialized")

    def create_article(self, title, content, author):
        article_data = {
            "title": title,
            "content": content,
            "author": author,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        try:
            article_id = self.repo.create_article(article_data)
            logger.info("Article created", extra={"article_id": article_id, "author": author})
            return {"message": "Article created successfully", "article_id": article_id}
        except Exception as e:
            logger.error("Error creating article", extra={
                "error": str(e),
                "author": author
            })
            return {"error": "Error creating article"}

    def get_all_articles(self, page=1, limit=10):
        skip = (page - 1) * limit
        try:
            articles = self.repo.get_all_articles(skip=skip, limit=limit)
            logger.info("Fetched articles", extra={
                "page": page,
                "limit": limit,
                "count": len(articles)
            })
            return articles
        except Exception as e:
            logger.error("Error retrieving articles", extra={"error": str(e)})
            return {"error": "Error retrieving articles"}

    def get_article_by_id(self, article_id):
        try:
            article = self.repo.get_article_by_id(article_id)
            if article:
                logger.info("Article retrieved", extra={"article_id": article_id})
                return article
            logger.warning("Article not found", extra={"article_id": article_id})
            return {"error": "Article not found"}
        except Exception as e:
            logger.error("Error retrieving article by ID", extra={
                "error": str(e),
                "article_id": article_id
            })
            return {"error": "Error retrieving article"}

    def update_article(self, article_id, title=None, content=None):
        update_data = {}
        if title:
            update_data["title"] = title
        if content:
            update_data["content"] = content
        if not update_data:
            logger.warning("No update fields provided for article",
                           extra={"article_id": article_id})
            return {"error": "No update fields provided"}
        update_data["updated_at"] = datetime.now(timezone.utc)
        try:
            success = self.repo.update_article(article_id, update_data)
            if success:
                logger.info("Article updated", extra={"article_id": article_id})
                return {"message": "Article updated successfully"}
            else:
                logger.warning("Article update failed", extra={"article_id": article_id})
                return {"error": "Article not found or update failed"}
        except Exception as e:
            logger.error("Error updating article", extra={
                "error": str(e),
                "article_id": article_id
            })
            return {"error": "Error updating article"}

    def delete_article(self, article_id):
        try:
            success = self.repo.delete_article(article_id)
            if success:
                logger.info("Article deleted", extra={"article_id": article_id})
                return {"message": "Article deleted successfully"}
            else:
                logger.warning("Article deletion failed", extra={"article_id": article_id})
                return {"error": "Article not found or deletion failed"}
        except Exception as e:
            logger.error("Error deleting article", extra={
                "error": str(e),
                "article_id": article_id
            })
            return {"error": "Error deleting article"}
