"""
app/config.py

This module loads environment variables (if available) and defines the configuration
for the application including database connection, JWT settings, and debug mode.
"""

from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables from a .env file if present.
load_dotenv()

class Config:
    """
    Base configuration for the Flask application.
    """
    # Production Database
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hive_db")

    # Test Database
    TEST_MONGO_URI = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017/")
    TEST_MONGO_DB_NAME = os.getenv("TEST_MONGO_DB_NAME", "hive_db_test")

    
    # Flask secret key used for sessions and CSRF protection.
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    
    # JWT configuration.
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)   # Access token lifetime.
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=3)  # Refresh token lifetime.
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False           # Set True in production with HTTPS.
    JWT_COOKIE_CSRF_PROTECT = False     # Enable CSRF protection in production
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    
    DEBUG = True
