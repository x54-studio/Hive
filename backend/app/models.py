"""
app/models.py

Defines the data models used within the application as simple data classes.
These models represent the domain entities such as User and Article.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """
    Data model for a user.
    """
    username: str
    email: str
    role: str
    created_at: datetime
    refresh_token: Optional[str] = None


@dataclass
class Article:
    """
    Data model for an article.
    """
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: datetime
