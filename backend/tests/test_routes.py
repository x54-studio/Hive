"""
tests/test_routes.py

Integration tests for API routes.
This file uses Flask's test client and forces the shared database instance to use
the test database ("hive_test_db").
"""

import unittest
import json
from app import create_app
from app.config import Config
from pymongo import MongoClient
import repositories.db as db_module

class TestRoutesIntegration(unittest.TestCase):
    def setUp(self):
        # Create the Flask app and test client.
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        
    def tearDown(self):
        # Clean up test collections.
        client = MongoClient(Config.TEST_MONGO_URI)
        test_db = client.get_database(Config.TEST_MONGO_DB_NAME)
        test_db.users.delete_many({})
        test_db.articles.delete_many({})
        client.close()

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get("message"), "Welcome to Hive!")

    def test_register_route_missing_fields(self):
        response = self.client.post("/api/register", json={"username": "test"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

if __name__ == '__main__':
    unittest.main()
