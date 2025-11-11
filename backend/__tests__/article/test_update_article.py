"""
References: backend/__docs__/useCases/article/UseCase_UpdateArticle.md

Test Scenarios:
1. Successful update of an existing article.
   - Expect PUT /api/articles/<article_id> with new title/content to return 200 and a success message.
   - Verify that the article's data is updated.
2. Failure when no update fields are provided.
   - Expect PUT /api/articles/<article_id> with an empty JSON body to return 400 with an appropriate error message.
"""

import unittest
import json
from app import create_app
from app.config import Config
from pymongo import MongoClient
from datetime import datetime

class TestUpdateArticle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()

        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        cls.test_db.users.delete_many({})
        cls.test_db.articles.delete_many({})

        # Register a moderator user.
        moderator = {
            "username": "moduser",
            "email": "mod@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=moderator)
        cls.test_db.users.update_one({"username": "moduser"}, {"$set": {"role": "moderator"}})

        # Register an admin user.
        admin = {
            "username": "adminuser",
            "email": "admin@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=admin)
        cls.test_db.users.update_one({"username": "adminuser"}, {"$set": {"role": "admin"}})

        # Register a regular user (author).
        author = {
            "username": "authoruser",
            "email": "author@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=author)

        # Register another regular user (not author).
        regular = {
            "username": "regularuser",
            "email": "regular@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=regular)

        # Log in as moderator to get an access token.
        login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "moduser", "password": "password123"}
        )
        if login_resp.status_code != 200:
            raise Exception(f"Login should succeed for moderator, got {login_resp.status_code}")
        login_data = login_resp.get_json()
        cls.moderator_token = login_data["access_token"]

        # Log in as author to create article.
        author_login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "authoruser", "password": "password123"}
        )
        if author_login_resp.status_code != 200:
            raise Exception(f"Login should succeed for author, got {author_login_resp.status_code}")
        author_login_data = author_login_resp.get_json()
        cls.author_token = author_login_data["access_token"]

        # Log in as admin.
        admin_login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "adminuser", "password": "password123"}
        )
        if admin_login_resp.status_code != 200:
            raise Exception(f"Login should succeed for admin, got {admin_login_resp.status_code}")
        admin_login_data = admin_login_resp.get_json()
        cls.admin_token = admin_login_data["access_token"]

        # Log in as regular user.
        regular_login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "regularuser", "password": "password123"}
        )
        if regular_login_resp.status_code != 200:
            raise Exception(f"Login should succeed for regular user, got {regular_login_resp.status_code}")
        regular_login_data = regular_login_resp.get_json()
        cls.regular_token = regular_login_data["access_token"]

        # Create an article as moderator, but set author to authoruser for RBAC testing.
        article_data = {
            "title": "Original Title",
            "content": "Original content."
        }
        cls.client.set_cookie("access_token", cls.moderator_token, domain="localhost")
        create_resp = cls.client.post("/api/articles", json=article_data)
        if create_resp.status_code != 201:
            raise Exception(f"Article creation should succeed, got {create_resp.status_code}")
        create_data = create_resp.get_json()
        cls.article_id = create_data.get("article_id")
        
        # Manually set author to authoruser for RBAC testing (simulating author created it)
        from bson import ObjectId
        cls.test_db.articles.update_one(
            {"_id": ObjectId(cls.article_id)},
            {"$set": {"author": "authoruser"}}
        )


    def test_update_article_success_moderator(self):
        # Moderator can update any article.
        update_data = {
            "title": "Updated by Moderator",
            "content": "Updated content by moderator."
        }
        self.client.set_cookie("access_token", self.moderator_token, domain="localhost")
        import time
        time.sleep(1)
        update_resp = self.client.put(f"/api/articles/{self.article_id}", json=update_data)
        self.assertEqual(update_resp.status_code, 200, "Expected 200 status when moderator updates article")
        data = update_resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article updated successfully")

    def test_update_article_success_admin(self):
        # Admin can update any article.
        update_data = {
            "title": "Updated by Admin",
            "content": "Updated content by admin."
        }
        self.client.set_cookie("access_token", self.admin_token, domain="localhost")
        import time
        time.sleep(1)
        update_resp = self.client.put(f"/api/articles/{self.article_id}", json=update_data)
        self.assertEqual(update_resp.status_code, 200, "Expected 200 status when admin updates article")
        data = update_resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article updated successfully")

    def test_update_article_success_author(self):
        # Author can update their own article.
        update_data = {
            "title": "Updated by Author",
            "content": "Updated content by author."
        }
        self.client.set_cookie("access_token", self.author_token, domain="localhost")
        import time
        time.sleep(1)
        update_resp = self.client.put(f"/api/articles/{self.article_id}", json=update_data)
        self.assertEqual(update_resp.status_code, 200, "Expected 200 status when author updates own article")
        data = update_resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article updated successfully")

    def test_update_article_unauthorized_regular_user(self):
        # Regular user cannot update article they didn't create.
        update_data = {
            "title": "Unauthorized Update",
            "content": "This should fail."
        }
        self.client.set_cookie("access_token", self.regular_token, domain="localhost")
        update_resp = self.client.put(f"/api/articles/{self.article_id}", json=update_data)
        self.assertEqual(update_resp.status_code, 403, "Expected 403 Forbidden when regular user tries to update article")
        data = update_resp.get_json()
        self.assertIn("error", data)
        self.assertIn("not authorized", data["error"].lower())

    def test_update_article_no_fields(self):
        # Attempt to update with an empty JSON body.
        self.client.set_cookie("access_token", self.moderator_token, domain="localhost")
        resp = self.client.put(f"/api/articles/{self.article_id}", json={})
        self.assertEqual(resp.status_code, 400, "Expected 400 status when no update fields are provided")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("no data provided for update", data["error"].lower())

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
