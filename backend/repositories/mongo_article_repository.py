import logging
from pymongo import errors
from bson import ObjectId
from repositories.base_article_repository import BaseArticleRepository
from repositories.db import db

logger = logging.getLogger(__name__)


class MongoArticleRepository(BaseArticleRepository):
    def __init__(self):
        self.articles = db.articles

    def create_article(self, article_data):
        try:
            result = self.articles.insert_one(article_data)
            return str(result.inserted_id)
        except errors.PyMongoError as e:
            logger.error("Error creating article",
                         extra={"article_data": article_data, "error": str(e)})
            raise Exception(f"Error creating article: {str(e)}")

    def get_all_articles(self, skip=0, limit=10):
        try:
            cursor = self.articles.find({}).sort("created_at", -1).skip(skip).limit(limit)
            articles = []
            for article in cursor:
                article["_id"] = str(article["_id"])
                articles.append(article)
            return articles
        except errors.PyMongoError as e:
            logger.error("Error retrieving articles",
                         extra={"skip": skip, "limit": limit, "error": str(e)})
            raise Exception(f"Error retrieving articles: {str(e)}")

    def get_article_by_id(self, article_id):
        try:
            article = self.articles.find_one({"_id": ObjectId(article_id)})
            if article:
                article["_id"] = str(article["_id"])
                return article
            logger.warning("Article not found", extra={"article_id": article_id})
            return None
        except errors.PyMongoError as e:
            logger.error("Error retrieving article by ID",
                         extra={"article_id": article_id, "error": str(e)})
            raise Exception(f"Error retrieving article by ID: {str(e)}")

    def update_article(self, article_id, update_data):
        try:
            result = self.articles.update_one({"_id": ObjectId(article_id)},
                                              {"$set": update_data})
            return result.modified_count > 0
        except errors.PyMongoError as e:
            logger.error("Error updating article",
                         extra={"article_id": article_id, "update_data": update_data,
                                "error": str(e)})
            raise Exception(f"Error updating article: {str(e)}")

    def delete_article(self, article_id):
        try:
            result = self.articles.delete_one({"_id": ObjectId(article_id)})
            return result.deleted_count > 0
        except errors.PyMongoError as e:
            logger.error("Error deleting article",
                         extra={"article_id": article_id, "error": str(e)})
            raise Exception(f"Error deleting article: {str(e)}")
