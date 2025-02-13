from pymongo import MongoClient
from app.config import Config
import atexit
import os

# Check if running in test mode
is_testing = os.getenv("TESTING", "false").lower() == "true"

# Select the appropriate database URI and name based on the environment
mongo_uri = Config.TEST_MONGO_URI if is_testing else Config.MONGO_URI
mongo_db_name = Config.TEST_MONGO_DB_NAME if is_testing else Config.MONGO_DB_NAME

# Create a global MongoClient instance using connection pooling
client = MongoClient(mongo_uri)
# Retrieve the shared database instance
db = client.get_database(mongo_db_name)

print(f"Connected to database: '{mongo_db_name}'")

# Register an exit handler to close the client when the process ends.
atexit.register(client.close)
