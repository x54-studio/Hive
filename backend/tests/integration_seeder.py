# backend/tests/integration_seeder.py
from pymongo import MongoClient
from app.config import Config


def get_test_db():
    config = Config()
    client = MongoClient(config.TEST_MONGO_URI)
    db = client[config.TEST_MONGO_DB_NAME]
    return db, client


def seed_users():
    db, client = get_test_db()
    users_collection = db.users
    users_collection.delete_many({})
    test_users = [
        {
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "hashedpassword1",  # Dummy hash for testing
            "role": "admin",
            "created_at": "2023-01-01T00:00:00Z",
        },
        {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "hashedpassword2",
            "role": "regular",
            "created_at": "2023-01-01T00:00:00Z",
        },
    ]
    users_collection.insert_many(test_users)
    client.close()
    print("Seeded users")


def seed_articles():
    db, client = get_test_db()
    articles_collection = db.articles
    articles_collection.delete_many({})
    test_articles = [
        {
            "title": "Test Article 1",
            "content": "Content for test article 1",
            "author": "testuser1",
            "created_at": "2023-01-02T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
        },
        {
            "title": "Test Article 2",
            "content": "Content for test article 2",
            "author": "testuser2",
            "created_at": "2023-01-03T00:00:00Z",
            "updated_at": "2023-01-03T00:00:00Z",
        },
    ]
    articles_collection.insert_many(test_articles)
    client.close()
    print("Seeded articles")


if __name__ == "__main__":
    seed_users()
    seed_articles()
