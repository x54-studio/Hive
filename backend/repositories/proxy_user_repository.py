"""
repositories/proxy_user_repository.py

Proxy implementation of the BaseUserRepository interface.
This class wraps a primary repository and optionally a fallback repository.
If the primary repository fails (e.g., due to database downtime), it can delegate to the fallback.
"""

from repositories.base_user_repository import BaseUserRepository
from repositories.mongo_user_repository import MongoUserRepository

class ProxyUserRepository(BaseUserRepository):
    def __init__(self, primary_repo=None, fallback_repo=None):
        # Use a primary repository; default is MongoUserRepository.
        self.primary_repo = primary_repo or MongoUserRepository()
        # Optional fallback repository.
        self.fallback_repo = fallback_repo

    def find_by_email(self, email):
        try:
            return self.primary_repo.find_by_email(email)
        except Exception as e:
            if self.fallback_repo:
                return self.fallback_repo.find_by_email(email)
            raise e

    def find_by_username(self, username):
        try:
            return self.primary_repo.find_by_username(username)
        except Exception as e:
            if self.fallback_repo:
                return self.fallback_repo.find_by_username(username)
            raise e

    def create_user(self, user_data):
        try:
            return self.primary_repo.create_user(user_data)
        except Exception as e:
            if self.fallback_repo:
                return self.fallback_repo.create_user(user_data)
            raise e

    def update_user_role(self, email, new_role):
        try:
            return self.primary_repo.update_user_role(email, new_role)
        except Exception as e:
            if self.fallback_repo:
                return self.fallback_repo.update_user_role(email, new_role)
            raise e

    def delete_user(self, email):
        try:
            return self.primary_repo.delete_user(email)
        except Exception as e:
            if self.fallback_repo:
                return self.fallback_repo.delete_user(email)
            raise e

    def store_refresh_token(self, username, hashed_refresh):
        try:
            return self.primary_repo.store_refresh_token(username, hashed_refresh)
        except Exception as e:
            if self.fallback_repo:
                return self.fallback_repo.store_refresh_token(username, hashed_refresh)
            raise e

    def get_refresh_token(self, username):
        try:
            return self.primary_repo.get_refresh_token(username)
        except Exception as e:
            if self.fallback_repo:
                return self.fallback_repo.get_refresh_token(username)
            raise e
