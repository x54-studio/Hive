import os
import bcrypt
import pymongo
from pymongo import MongoClient, errors
from .config import Config

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