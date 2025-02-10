# models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    username: str
    email: str
    role: str
    created_at: datetime
    refresh_token: Optional[str] = None

@dataclass
class Article:
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: datetime
