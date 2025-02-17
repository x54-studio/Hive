# repositories/db.py
import os
from utilities.logger import get_logger
from pymongo import MongoClient


logger = get_logger(__name__)


def init_db():
    is_testing = os.getenv("TESTING", "false").lower() == "true"
    if is_testing:
        mongo_uri = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017/")
        mongo_db_name = os.getenv("TEST_MONGO_DB_NAME", "hive_db_test")
    else:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        mongo_db_name = os.getenv("MONGO_DB_NAME", "hive_db")
    logger.info("is_testing: %s", is_testing)
    client = MongoClient(mongo_uri)
    return client[mongo_db_name]


db = init_db()

print(f"Connected to database: {db.name}")
logger.info("Connected to database: %s", db.name)
