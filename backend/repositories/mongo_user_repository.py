# repositories/mongo_user_repository.py
from utilities.logger import get_logger
from utilities.custom_exceptions import RepositoryError
from pymongo import errors
from .base_user_repository import BaseUserRepository
from .db import db


logger = get_logger(__name__)


class MongoUserRepository(BaseUserRepository):
    def __init__(self):
        self.users = db.users

    def find_by_email(self, email):
        try:
            user = self.users.find_one({"email": email})
            return user
        except errors.PyMongoError as e:
            logger.error(
                "Error finding user by email", extra={"email": email, "error": str(e)}
            )
            raise RepositoryError(f"Error finding user by email: {str(e)}") from e

    def find_by_username(self, username):
        try:
            return self.users.find_one({"username": username})
        except errors.PyMongoError as e:
            logger.error(
                "Error finding user by username",
                extra={"username": username, "error": str(e)},
            )
            raise RepositoryError(f"Error finding user by username: {str(e)}") from e

    def create_user(self, user_data):
        try:
            result = self.users.insert_one(user_data)
            return str(result.inserted_id)
        except errors.PyMongoError as e:
            logger.error(
                "Error creating user", extra={"user_data": user_data, "error": str(e)}
            )
            raise RepositoryError(f"Error creating user: {str(e)}") from e

    def update_user_role(self, email, new_role):
        try:
            result = self.users.update_one(
                {"email": email}, {"$set": {"role": new_role}}
            )
            return result.modified_count > 0
        except errors.PyMongoError as e:
            logger.error(
                "Error updating user role",
                extra={"email": email, "new_role": new_role, "error": str(e)},
            )
            raise RepositoryError(f"Error updating user role: {str(e)}") from e

    def delete_user(self, email):
        try:
            result = self.users.delete_one({"email": email})
            return result.deleted_count > 0
        except errors.PyMongoError as e:
            logger.error("Error deleting user", extra={"email": email, "error": str(e)})
            raise RepositoryError(f"Error deleting user: {str(e)}") from e

    def store_refresh_token(self, username, hashed_refresh):
        try:
            self.users.update_one(
                {"username": username}, {"$set": {"refresh_token": hashed_refresh}}
            )
        except errors.PyMongoError as e:
            logger.error(
                "Error storing refresh token",
                extra={"username": username, "error": str(e)},
            )
            raise RepositoryError(f"Error storing refresh token: {str(e)}") from e

    def get_refresh_token(self, username):
        try:
            user = self.users.find_one({"username": username})
            if user:
                return user.get("refresh_token")
            return None
        except errors.PyMongoError as e:
            logger.error(
                "Error retrieving refresh token",
                extra={"username": username, "error": str(e)},
            )
            raise RepositoryError(f"Error retrieving refresh token: {str(e)}") from e
