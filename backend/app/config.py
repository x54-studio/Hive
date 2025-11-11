import os
from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()


class Config:
    """
    Application configuration settings.
    """

    # Determine if we're in testing mode.
    TESTING = os.getenv("TESTING", "false").lower() == "true"
    print(f"TESTING: {TESTING}")

    if TESTING:
        MONGO_URI = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017/")
        MONGO_DB_NAME = os.getenv("TEST_MONGO_DB_NAME", "hive_db_test")
    else:
        MONGO_URI = os.getenv("MONGO_URI", "mongodb://atlas:27017/")
        MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hive_db")

    # Secret Keys - REQUIRED: Must be set via environment variables
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError(
            "SECRET_KEY environment variable is required. "
            "Set it in your .env file or environment variables."
        )

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise ValueError(
            "JWT_SECRET_KEY environment variable is required. "
            "Set it in your .env file or environment variables."
        )

    # JWT configuration - Production values
    JWT_ALGORITHM = "HS256"
    # Access token expires in 15 minutes (900 seconds)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "900"))
    # Refresh token expires in 7 days (604800 seconds)
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "604800"))
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

    def as_dict(self):
        """
        Return configuration variables as a dictionary.
        """
        return {key: getattr(self, key) for key in dir(self) if key.isupper()}

    def get_jwt_config(self):
        """
        Return JWT configuration settings.
        """
        return {
            "JWT_SECRET_KEY": self.JWT_SECRET_KEY,
            "JWT_ALGORITHM": self.JWT_ALGORITHM,
            "JWT_ACCESS_TOKEN_EXPIRES": self.JWT_ACCESS_TOKEN_EXPIRES,
            "JWT_REFRESH_TOKEN_EXPIRES": self.JWT_REFRESH_TOKEN_EXPIRES,
        }
