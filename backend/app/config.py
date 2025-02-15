import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()


class Config:

    # Production Database
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hive_db")

    # Test Database
    TEST_MONGO_URI = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017/")
    TEST_MONGO_DB_NAME = os.getenv("TEST_MONGO_DB_NAME", "hive_db_test")

    # Secret Keys
    SECRET_KEY = os.getenv("SECRET_KEY", "dupiarz_i_klockow_kupiacz_@#%^(32)")
    if SECRET_KEY == "your_secret_key":
        raise Exception("Please set a secure SECRET_KEY in your environment variables!")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_dupiarz_i_klockow_kupiacz_^&*(56)")
    if JWT_SECRET_KEY == "your_jwt_secret_key":
        raise Exception("Please set a secure JWT_SECRET_KEY in your environment variables!")

    # JWT configuration
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "1")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "3")))
    JWT_TOKEN_LOCATION = ["cookies"]

    # Secure cookie settings: use production settings if FLASK_ENV is production
    if os.getenv("FLASK_ENV") == "production":
        JWT_COOKIE_SECURE = True
        JWT_COOKIE_CSRF_PROTECT = True
    else:
        JWT_COOKIE_SECURE = False
        JWT_COOKIE_CSRF_PROTECT = False

    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"

    DEBUG = os.getenv("FLASK_ENV") != "production"
