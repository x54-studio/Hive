import os
import bcrypt
import pymongo
from pymongo import MongoClient, errors
from .config import Config
from datetime import datetime, timezone

# Global MongoDB client variable
client = None

def get_db_connection():
    global client
    if client is None:
        try:
            #print(Config.MONGO_URI)
            client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
            client.server_info()  # Trigger a connection error if MongoDB is unavailable
        except errors.ServerSelectionTimeoutError:
            print("MongoDB connection failed. Return None")
            return None
    return client.hive_db


db = get_db_connection()

users_collection = db.users if db is not None else None
articles_collection = db.articles if db is not None else None

class User:
    @staticmethod
    def create_user(username, email, password, role="regular"):
        if users_collection is None:  # Use explicit check
            print("Database unavailable - Cannot create user.")
            return {"error": "Database connection failed. Please try again later."}

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {"username": username, "email": email, "password": hashed_pw, "role": role}
        try:
            users_collection.insert_one(user_data)
            return {"message": "User registered successfully!"}
        except errors.PyMongoError as e:
            print(f"MongoDB Error: {e}")
            return {"error": "Database operation failed."}

    @staticmethod
    def find_user_by_email(email):
        if users_collection is None:  # Use explicit check
            print("Database unavailable - Cannot fetch user.")
            return None  # This ensures login fails when DB is down
        try:
            return users_collection.find_one({"email": email})
        except errors.PyMongoError as e:
            print(f"MongoDB Error: {e}")
            return None
        

class Article:
    @staticmethod
    def create_article(title, content, author):
        article_data = {
            "title": title,
            "content": content,
            "author": author,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        articles_collection.insert_one(article_data)
        return article_data

    @staticmethod
    def get_all_articles():
        return list(articles_collection.find({}, {"_id": 0}))

    @staticmethod
    def get_article_by_id(article_id):
        return articles_collection.find_one({"_id": article_id}, {"_id": 0})

    @staticmethod
    def update_article(article_id, content):
        return articles_collection.update_one({"_id": article_id}, {"$set": {"content": content, "updated_at": datetime.utcnow()}})

    @staticmethod
    def delete_article(article_id):
        return articles_collection.delete_one({"_id": article_id})