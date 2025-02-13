"""
repositories/base_article_repository.py

Abstract base class defining the interface for article repository operations.
Any concrete implementation must implement these methods.
"""

from abc import ABC, abstractmethod

class BaseArticleRepository(ABC):
    @abstractmethod
    def create_article(self, article_data):
        """Create a new article document with the provided data."""
        pass

    @abstractmethod
    def get_all_articles(self, skip=0, limit=10):
        """Retrieve a list of article documents with pagination."""
        pass

    @abstractmethod
    def get_article_by_id(self, article_id):
        """Retrieve a single article document by its unique identifier."""
        pass

    @abstractmethod
    def update_article(self, article_id, update_data):
        """Update the article document identified by article_id with the given data."""
        pass

    @abstractmethod
    def delete_article(self, article_id):
        """Delete the article document identified by article_id."""
        pass
