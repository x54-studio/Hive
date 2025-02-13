"""
repositories/mongo_article_repository.py

Concrete implementation of the BaseArticleRepository interface using MongoDB.
This implementation uses the globally shared database instance from repositories/db.py.
"""

from pymongo import errors
from bson import ObjectId
from repositories.base_article_repository import BaseArticleRepository
from repositories.db import db

class MongoArticleRepository(BaseArticleRepository):
    def __init__(self):
        # Use the shared database instance.
        self.articles = db.articles

    def create_article(self, article_data):
        try:
            result = self.articles.insert_one(article_data)
            return str(result.inserted_id)
        except errors.PyMongoError as e:
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
            raise Exception(f"Error retrieving articles: {str(e)}")

    def get_article_by_id(self, article_id):
        try:
            article = self.articles.find_one({"_id": ObjectId(article_id)})
            if article:
                article["_id"] = str(article["_id"])
                return article
            return None
        except errors.PyMongoError as e:
            raise Exception(f"Error retrieving article by ID: {str(e)}")

    def update_article(self, article_id, update_data):
        try:
            result = self.articles.update_one({"_id": ObjectId(article_id)}, {"$set": update_data})
            return result.modified_count > 0
        except errors.PyMongoError as e:
            raise Exception(f"Error updating article: {str(e)}")

    def delete_article(self, article_id):
        try:
            result = self.articles.delete_one({"_id": ObjectId(article_id)})
            return result.deleted_count > 0
        except errors.PyMongoError as e:
            raise Exception(f"Error deleting article: {str(e)}")
