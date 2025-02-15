import logging
from pymongo import errors
from repositories.base_user_repository import BaseUserRepository
from repositories.db import db

logger = logging.getLogger(__name__)


class MongoUserRepository(BaseUserRepository):
    def __init__(self):
        self.users = db.users

    def find_by_email(self, email):
        try:
            user = self.users.find_one({"email": email})
            return user
        except errors.PyMongoError as e:
            logger.error("Error finding user by email",
                         extra={"email": email, "error": str(e)})
            raise Exception(f"Error finding user by email: {str(e)}")

    def find_by_username(self, username):
        try:
            return self.users.find_one({"username": username})
        except errors.PyMongoError as e:
            logger.error("Error finding user by username",
                         extra={"username": username, "error": str(e)})
            raise Exception(f"Error finding user by username: {str(e)}")

    def create_user(self, user_data):
        try:
            result = self.users.insert_one(user_data)
            return str(result.inserted_id)
        except errors.PyMongoError as e:
            logger.error("Error creating user",
                         extra={"user_data": user_data, "error": str(e)})
            raise Exception(f"Error creating user: {str(e)}")

    def update_user_role(self, email, new_role):
        try:
            result = self.users.update_one({"email": email},
                                           {"$set": {"role": new_role}})
            return result.modified_count > 0
        except errors.PyMongoError as e:
            logger.error("Error updating user role",
                         extra={"email": email, "new_role": new_role, "error": str(e)})
            raise Exception(f"Error updating user role: {str(e)}")

    def delete_user(self, email):
        try:
            result = self.users.delete_one({"email": email})
            return result.deleted_count > 0
        except errors.PyMongoError as e:
            logger.error("Error deleting user",
                         extra={"email": email, "error": str(e)})
            raise Exception(f"Error deleting user: {str(e)}")

    def store_refresh_token(self, username, hashed_refresh):
        try:
            self.users.update_one({"username": username},
                                  {"$set": {"refresh_token": hashed_refresh}})
        except errors.PyMongoError as e:
            logger.error("Error storing refresh token",
                         extra={"username": username, "error": str(e)})
            raise Exception(f"Error storing refresh token: {str(e)}")

    def get_refresh_token(self, username):
        try:
            user = self.users.find_one({"username": username})
            if user:
                return user.get("refresh_token")
            return None
        except errors.PyMongoError as e:
            logger.error("Error retrieving refresh token",
                         extra={"username": username, "error": str(e)})
            raise Exception(f"Error retrieving refresh token: {str(e)}")
