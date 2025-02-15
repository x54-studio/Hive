import logging
import os
from pymongo import MongoClient

logger = logging.getLogger(__name__)


def init_db():
    # Check if running in testing mode using an environment variable
    is_testing = os.getenv("TESTING", "false").lower() == "true"

    # Get connection details directly from environment variables
    if is_testing:
        mongo_uri = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017/")
        mongo_db_name = os.getenv("TEST_MONGO_DB_NAME", "hive_db_test")
    else:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        mongo_db_name = os.getenv("MONGO_DB_NAME", "hive_db")

    logger.info(f"is_testing: {is_testing}")

    client = MongoClient(mongo_uri)
    return client[mongo_db_name]


db = init_db()

print(f"Connected to database: {db.name}")
logger.info(f"Connected to database: {db.name}")
