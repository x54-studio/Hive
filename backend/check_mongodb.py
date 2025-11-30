#!/usr/bin/env python3
"""
Script to check MongoDB connection and verify data.
Run from backend directory: python check_mongodb.py

The script reads MONGO_URI from .env file or environment variables.
MONGO_URI should be configured in your .env file or environment variables.
Example format: mongodb://username:password@host:port/
"""

import os
from dotenv import load_dotenv

# Load .env file explicitly to ensure it's read
load_dotenv()

from app.config import Config
from utilities.logger import get_logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = get_logger(__name__)


def get_mongo_uri():
    """
    Get MongoDB URI, automatically converting Docker hostname to localhost for local runs.
    """
    mongo_uri = Config.MONGO_URI
    
    # If URI contains Docker hostname and we're not in Docker, convert to localhost
    if "mongodb:" in mongo_uri and "localhost" not in mongo_uri and "127.0.0.1" not in mongo_uri:
        # Check if we're likely running locally (not in Docker)
        # Docker detection: check for Docker-specific files/env vars
        is_docker = (
            os.path.exists("/.dockerenv") or 
            os.path.exists("/proc/self/cgroup") or
            os.environ.get("DOCKER_CONTAINER") == "true"
        )
        
        if not is_docker:
            # Replace Docker hostname with localhost
            # Handle both "mongodb:" and "@mongodb:" patterns
            mongo_uri = mongo_uri.replace("@mongodb:", "@localhost:")
            mongo_uri = mongo_uri.replace("mongodb://mongodb:", "mongodb://localhost:")
            logger.info(f"Converted Docker hostname to localhost: {mongo_uri}")
    
    return mongo_uri


def check_mongodb():
    """Check MongoDB connection and verify data."""
    try:
        # Use the adjusted MongoDB URI (converts Docker hostname to localhost if needed)
        mongo_uri = get_mongo_uri()
        
        print("=" * 60)
        print("MongoDB Connection Check")
        print("=" * 60)
        print(f"Database: {Config.MONGO_DB_NAME}")
        print(f"MongoDB URI: {mongo_uri}")
        print("-" * 60)
        
        # Create direct MongoDB connection
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = mongo_client[Config.MONGO_DB_NAME]
        
        # Test connection
        try:
            mongo_client.admin.command('ping')
            print("✓ MongoDB connection successful")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ MongoDB connection failed: {str(e)}")
            print("\n💡 TIP: Ensure MongoDB is running:")
            print("   - Docker: docker-compose up -d mongodb")
            print("   - Local: Check if MongoDB service is running")
            return False
        
        # List all collections
        collections = db.list_collection_names()
        print(f"\nCollections found: {len(collections)}")
        if collections:
            for collection in sorted(collections):
                print(f"  - {collection}")
        else:
            print("  (no collections)")
        
        # Check articles collection
        print("\n" + "-" * 60)
        print("Articles Collection")
        print("-" * 60)
        articles_collection = db.articles
        articles_count = articles_collection.count_documents({})
        print(f"Total articles: {articles_count}")
        
        if articles_count > 0:
            # Get sample article
            sample_article = articles_collection.find_one()
            if sample_article:
                print(f"\nSample article:")
                print(f"  ID: {sample_article.get('_id')}")
                print(f"  Title: {sample_article.get('title', 'N/A')}")
                print(f"  Author: {sample_article.get('author', 'N/A')}")
                print(f"  Created: {sample_article.get('created_at', 'N/A')}")
            
            # Get latest article
            latest_article = articles_collection.find_one(sort=[("created_at", -1)])
            if latest_article:
                print(f"\nLatest article:")
                print(f"  Title: {latest_article.get('title', 'N/A')}")
                print(f"  Created: {latest_article.get('created_at', 'N/A')}")
        else:
            print("  (no articles found)")
            print("\n💡 TIP: Run 'python seed_articles.py' to add sample articles")
        
        # Check users collection
        print("\n" + "-" * 60)
        print("Users Collection")
        print("-" * 60)
        users_collection = db.users
        users_count = users_collection.count_documents({})
        print(f"Total users: {users_count}")
        
        if users_count > 0:
            # Get sample user (without sensitive data)
            sample_user = users_collection.find_one({}, {"password": 0, "refresh_token": 0})
            if sample_user:
                print(f"\nSample user:")
                print(f"  ID: {sample_user.get('_id')}")
                print(f"  Username: {sample_user.get('username', 'N/A')}")
                print(f"  Email: {sample_user.get('email', 'N/A')}")
                print(f"  Role: {sample_user.get('role', 'N/A')}")
        else:
            print("  (no users found)")
        
        # Database statistics
        print("\n" + "-" * 60)
        print("Database Statistics")
        print("-" * 60)
        try:
            stats = db.command("dbStats")
            data_size = stats.get('dataSize', 0)
            storage_size = stats.get('storageSize', 0)
            indexes = stats.get('indexes', 0)
            index_size = stats.get('indexSize', 0)
            
            print(f"Data size: {data_size:,} bytes ({data_size / 1024 / 1024:.2f} MB)")
            print(f"Storage size: {storage_size:,} bytes ({storage_size / 1024 / 1024:.2f} MB)")
            print(f"Indexes: {indexes}")
            print(f"Index size: {index_size:,} bytes ({index_size / 1024:.2f} KB)")
        except Exception as e:
            logger.warning(f"Could not retrieve database stats: {str(e)}")
            print("  (stats unavailable)")
        
        # Collection indexes
        print("\n" + "-" * 60)
        print("Collection Indexes")
        print("-" * 60)
        for collection_name in sorted(collections):
            collection = db[collection_name]
            indexes = collection.list_indexes()
            index_list = list(indexes)
            if index_list:
                print(f"\n{collection_name}:")
                for idx in index_list:
                    idx_name = idx.get('name', 'N/A')
                    idx_keys = idx.get('key', {})
                    print(f"  - {idx_name}: {idx_keys}")
        
        # Close the connection
        mongo_client.close()
        
        print("\n" + "=" * 60)
        print("Check complete!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking MongoDB: {str(e)}")
        print(f"\n✗ Error: {str(e)}")
        print("\n💡 TIP: Ensure your .env file has MONGO_URI configured:")
        print("   MONGO_URI=mongodb://username:password@host:port/")
        print("\n   Or run MongoDB via Docker Compose and use the Docker hostname.")
        return False


if __name__ == "__main__":
    print("Starting MongoDB check...")
    print()
    
    # Get the adjusted URI (may convert Docker hostname to localhost)
    original_uri = Config.MONGO_URI
    adjusted_uri = get_mongo_uri()
    
    if original_uri != adjusted_uri:
        logger.info(f"Adjusted MongoDB URI: {adjusted_uri} (converted Docker hostname to localhost)")
    
    success = check_mongodb()
    
    if not success:
        exit(1)

