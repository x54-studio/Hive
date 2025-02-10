import os
import bcrypt
import pymongo
from pymongo import MongoClient, errors
from .config import Config
from bson import ObjectId
from datetime import datetime, timezone
from flask import request

# Global variables
client = None
db = None
articles_collection = None
users_collection = None


def init_db(mongo_uri):
    """Initialize the MongoDB connection"""
    global client, db, articles_collection, users_collection
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client.get_database()
        articles_collection = db.articles
        users_collection = db.users
        print("✅ MongoDB Atlas connection successful!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB Atlas: {e}")
        articles_collection = None  # Ensure it does not break if connection fails
        users_collection = None


def get_db_connection():
    global client
    if client is None:
        try:
            print(Config.MONGO_URI)
            client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=20000)
            client.server_info()  # Trigger a connection error if MongoDB is unavailable
        except errors.ServerSelectionTimeoutError:
            print("MongoDB connection failed. Returning None")
            return None
    return client.hive_db


db = get_db_connection()
users_collection = db.users if db is not None else None
articles_collection = db.articles if db is not None else None


### 📌 USER MODEL ###
class User:
    @staticmethod
    def create_user(username, email, password, role="regular"):
        if users_collection is None:
            print("Database unavailable - Cannot create user.")
            return {"error": "Database connection failed. Please try again later."}

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_pw,
            "role": role,
            "created_at": datetime.now(timezone.utc),
        }

        try:
            users_collection.insert_one(user_data)
            return {"message": "User registered successfully!"}
        except errors.PyMongoError as e:
            return {"error": f"Database error: {str(e)}"}

    @staticmethod
    def find_user_by_email(email):
        if users_collection is None:
            print("Database unavailable - Cannot fetch user.")
            return None
        try:
            return users_collection.find_one({"email": email})
        except errors.PyMongoError as e:
            print(f"MongoDB Error: {e}")
            return None

    @staticmethod
    def update_user_role(email, new_role):
        """Update the role of a user"""
        if users_collection is None:
            return {"error": "Database connection failed."}

        try:
            result = users_collection.update_one({"email": email}, {"$set": {"role": new_role}})
            return {"message": "User role updated successfully!"} if result.modified_count > 0 else {"error": "User not found."}
        except errors.PyMongoError as e:
            print(f"MongoDB Error: {e}")
            return {"error": "Database operation failed."}

    @staticmethod
    def delete_user(email):
        """Delete a user by email"""
        if users_collection is None:
            return {"error": "Database connection failed."}

        try:
            result = users_collection.delete_one({"email": email})
            return {"message": "User deleted successfully!"} if result.deleted_count > 0 else {"error": "User not found."}
        except errors.PyMongoError as e:
            print(f"MongoDB Error: {e}")
            return {"error": "Database operation failed."}
    
    @staticmethod
    def store_refresh_token(username, hashed_refresh):
        """Store hashed refresh token in the database"""
        users_collection.update_one(
            {"username": username},
            {"$set": {"refresh_token": hashed_refresh}}
        )

    @staticmethod
    def get_refresh_token(username):
        """Retrieve hashed refresh token from the database"""
        user = users_collection.find_one({"username": username})
        return user.get("refresh_token") if user else None


### 📌 ARTICLE MODEL ###
class Article:
    @staticmethod
    def create_article(title, content, author):
        """Create a new article"""
        if articles_collection is None:
            raise Exception("Database connection failed")

        article_data = {
            "title": title,
            "content": content,
            "author": author,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = articles_collection.insert_one(article_data)
        article_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
        return article_data

    @staticmethod
    def get_all_articles():
        """Retrieve all articles"""
        if articles_collection is None:
            raise Exception("Database connection failed")

        articles = articles_collection.find({})
        return [
            {
                "_id": str(article["_id"]),
                "title": article["title"],
                "content": article["content"],
                "author": article["author"],
                "created_at": article.get("created_at", datetime.now(timezone.utc)),  # ✅ Default to current time
                "updated_at": article.get("updated_at", article.get("created_at", datetime.now(timezone.utc))),  # ✅ Use created_at if missing
            }
            for article in articles
        ]

    @staticmethod
    def get_article_by_id(article_id):
        """Retrieve an article by ID"""
        if articles_collection is None:
            raise Exception("Database connection failed")

        try:
            article = articles_collection.find_one({"_id": ObjectId(article_id)})
            if article:
                article["_id"] = str(article["_id"])  # Convert ObjectId to string
                return article
            return None
        except errors.PyMongoError as e:
            print(f"MongoDB Error: {e}")
            return None

    @staticmethod
    def update_article(article_id, new_title=None, new_content=None):
        """Update an article's title or content"""
        if articles_collection is None:
            raise Exception("Database connection failed")

        update_data = {}
        if new_title:
            update_data["title"] = new_title
        if new_content:
            update_data["content"] = new_content

        if not update_data:
            return {"error": "No update fields provided."}

        update_data["updated_at"] = datetime.now(timezone.utc)

        try:
            result = articles_collection.update_one({"_id": ObjectId(article_id)}, {"$set": update_data})
            return {"message": "Article updated successfully!"} if result.modified_count > 0 else {"error": "Article not found."}
        except errors.PyMongoError as e:
            print(f"MongoDB Error: {e}")
            return {"error": "Database operation failed."}

    @staticmethod
    def delete_article(article_id):
        """Delete an article by ID"""
        if articles_collection is None:
            raise Exception("Database connection failed")

        try:
            result = articles_collection.delete_one({"_id": ObjectId(article_id)})
            return {"message": "Article deleted successfully!"} if result.deleted_count > 0 else {"error": "Article not found."}
        except errors.PyMongoError as e:
            print(f"MongoDB Error: {e}")
            return {"error": "Database operation failed."}
