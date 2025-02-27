# repositories/mongo_user_repository.py
from utilities.logger import get_logger
from pymongo import errors
from bson import ObjectId
from bson.errors import InvalidId
from .db import get_db  # Use the getter function instead of importing db directly

logger = get_logger(__name__)

class MongoUserRepository:
    def __init__(self):
        self.db = get_db()
        self.users = self.db.users

    def find_by_email(self, email):
        try:
            return self.users.find_one({"email": email})
        except errors.PyMongoError as e:
            logger.error("Error finding user by email", extra={"email": email, "error": str(e)})
            raise e

    def find_by_username(self, username):
        try:
            return self.users.find_one({"username": username})
        except errors.PyMongoError as e:
            logger.error("Error finding user by username", extra={"username": username, "error": str(e)})
            raise e

    def create_user(self, user_data):
        try:
            result = self.users.insert_one(user_data)
            return str(result.inserted_id)
        except errors.PyMongoError as e:
            logger.error("Error creating user", extra={"user_data": user_data, "error": str(e)})
            raise e

    def update_user_role(self, email, new_role):
        try:
            result = self.users.update_one(
                {"email": email},
                {"$set": {"role": new_role}}
            )
            return result.modified_count > 0
        except errors.PyMongoError as e:
            logger.error("Error updating user role", extra={"email": email, "new_role": new_role, "error": str(e)})
            raise e

    def delete_user(self, email):
        try:
            result = self.users.delete_one({"email": email})
            return result.deleted_count > 0
        except errors.PyMongoError as e:
            logger.error("Error deleting user", extra={"email": email, "error": str(e)})
            raise e

    def store_refresh_token(self, username, hashed_refresh):
        try:
            result = self.users.update_one(
                {"username": username},
                {"$set": {"refresh_token": hashed_refresh}},
                upsert=True
            )
            return result.modified_count > 0 or result.upserted_id is not None
        except errors.PyMongoError as e:
            logger.error("Error storing refresh token", extra={"username": username, "error": str(e)})
            raise e

    def get_refresh_token(self, username):
        try:
            user = self.users.find_one({"username": username})
            if user:
                return user.get("refresh_token")
            return None
        except errors.PyMongoError as e:
            logger.error("Error retrieving refresh token", extra={"username": username, "error": str(e)})
            raise e
