from dotenv import load_dotenv
from datetime import timedelta
import os

# Load the .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")

    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_ALGORITHM = "HS256"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=3)

    # Enable JWT tokens in cookies
    JWT_TOKEN_LOCATION = ["cookies"]  
    JWT_COOKIE_SECURE = False  # Set to True in production with HTTPS
    JWT_COOKIE_CSRF_PROTECT = False  # Disable CSRF for testing (enable in production)
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"

    DEBUG = True
