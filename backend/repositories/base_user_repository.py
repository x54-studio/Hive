"""
repositories/base_user_repository.py

Abstract base class defining the interface for user repository operations.
All concrete implementations must implement these methods.
"""

from abc import ABC, abstractmethod


class BaseUserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email):
        """Find and return a user document by email."""
        pass

    @abstractmethod
    def find_by_username(self, username):
        """Find and return a user document by username."""
        pass

    @abstractmethod
    def create_user(self, user_data):
        """Create a new user document with the given data."""
        pass

    @abstractmethod
    def update_user_role(self, email, new_role):
        """Update the role of a user identified by email."""
        pass

    @abstractmethod
    def delete_user(self, email):
        """Delete the user document identified by email."""
        pass

    @abstractmethod
    def store_refresh_token(self, username, hashed_refresh):
        """Store the hashed refresh token for the specified user."""
        pass

    @abstractmethod
    def get_refresh_token(self, username):
        """Retrieve the stored refresh token for the specified user."""
        pass
