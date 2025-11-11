"""
References: backend/__docs__/useCases/article/UseCase_DeleteArticle.md

Test Scenarios:
1. Successful deletion of an existing article.
   - Expect DELETE /api/articles/<article_id> to return 200 with a success message.
   - Subsequent GET /api/articles/<article_id> should return 404.
2. Attempting to delete a non-existent article returns a 404 error.
"""

import unittest
from app import create_app
from app.config import Config
from pymongo import MongoClient

class TestDeleteArticle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Enable testing and create the app and test client.
        Config.TESTING = True
        cls.app = create_app()
        cls.client = cls.app.test_client()
        
        # Connect to the test database.
        cls.mongo_client = MongoClient(Config.MONGO_URI)
        cls.test_db = cls.mongo_client[Config.MONGO_DB_NAME]
        # Clear previous data.
        cls.test_db.users.delete_many({})
        cls.test_db.articles.delete_many({})

        # Register a moderator (authorized to delete articles).
        moderator = {
            "username": "moduser",
            "email": "mod@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=moderator)
        cls.test_db.users.update_one({"username": "moduser"}, {"$set": {"role": "moderator"}})
        # Verify role was set correctly
        mod_user = cls.test_db.users.find_one({"username": "moduser"})
        if not mod_user or mod_user.get("role") != "moderator":
            raise Exception(f"Failed to set moderator role. User: {mod_user}")

        # Register an admin user.
        admin = {
            "username": "adminuser",
            "email": "admin@example.com",
            "password": "password123"
        }
        cls.client.post("/api/register", json=admin)
        cls.test_db.users.update_one({"username": "adminuser"}, {"$set": {"role": "admin"}})
        # Verify role was set correctly
        admin_user = cls.test_db.users.find_one({"username": "adminuser"})
        if not admin_user or admin_user.get("role") != "admin":
            raise Exception(f"Failed to set admin role. User: {admin_user}")

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
        
        # Log in as the moderator.
        login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "moduser", "password": "password123"}
        )
        if login_resp.status_code != 200:
            raise Exception(f"Login failed with status {login_resp.status_code}")
        login_data = login_resp.get_json()
        cls.moderator_token = login_data["access_token"]
        # Verify JWT token contains moderator role
        import jwt
        decoded = jwt.decode(cls.moderator_token, options={"verify_signature": False})
        if decoded.get("role") != "moderator":
            raise Exception(f"JWT token does not have moderator role. Token claims: {decoded}")

        # Log in as admin.
        admin_login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "adminuser", "password": "password123"}
        )
        if admin_login_resp.status_code != 200:
            raise Exception(f"Login failed for admin with status {admin_login_resp.status_code}")
        admin_login_data = admin_login_resp.get_json()
        cls.admin_token = admin_login_data["access_token"]

        # Log in as author.
        author_login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "authoruser", "password": "password123"}
        )
        if author_login_resp.status_code != 200:
            raise Exception(f"Login failed for author with status {author_login_resp.status_code}")
        author_login_data = author_login_resp.get_json()
        cls.author_token = author_login_data["access_token"]

        # Log in as regular user.
        regular_login_resp = cls.client.post(
            "/api/login",
            json={"username_or_email": "regularuser", "password": "password123"}
        )
        if regular_login_resp.status_code != 200:
            raise Exception(f"Login failed for regular user with status {regular_login_resp.status_code}")
        regular_login_data = regular_login_resp.get_json()
        cls.regular_token = regular_login_data["access_token"]

        # Create an article as moderator, but set author to authoruser for RBAC testing.
        article_data = {
            "title": "Delete Test Article",
            "content": "Content of article to be deleted."
        }
        # Use set_cookie instead of headers for proper cookie handling
        cls.client.set_cookie("access_token", cls.moderator_token, domain="localhost")
        create_resp = cls.client.post("/api/articles", json=article_data)
        if create_resp.status_code != 201:
            raise Exception(f"Article creation failed with status {create_resp.status_code}")
        create_data = create_resp.get_json()
        cls.article_id = create_data["article_id"]
        
        # Manually set author to authoruser for RBAC testing
        from bson import ObjectId
        cls.test_db.articles.update_one(
            {"_id": ObjectId(cls.article_id)},
            {"$set": {"author": "authoruser"}}
        )

    def test_delete_article_success_moderator(self):
        # Ensure article exists (recreate if needed for test isolation)
        article_data = {
            "title": "Delete Test Article Moderator",
            "content": "Content of article to be deleted by moderator."
        }
        self.client.set_cookie("access_token", self.moderator_token, domain="localhost")
        create_resp = self.client.post("/api/articles", json=article_data)
        if create_resp.status_code != 201:
            raise Exception(f"Article creation failed with status {create_resp.status_code}")
        create_data = create_resp.get_json()
        article_id = create_data["article_id"]
        from bson import ObjectId
        self.test_db.articles.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"author": "authoruser"}}
        )
        
        # Delete the article as moderator.
        resp = self.client.delete(f"/api/articles/{article_id}")
        self.assertEqual(resp.status_code, 200, "Expected 200 status when moderator deletes article")
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article deleted successfully")
        
        # Recreate article for next tests
        article_data = {
            "title": "Delete Test Article 2",
            "content": "Content of article to be deleted."
        }
        self.client.set_cookie("access_token", self.moderator_token, domain="localhost")
        create_resp = self.client.post("/api/articles", json=article_data)
        if create_resp.status_code != 201:
            raise Exception(f"Article recreation failed with status {create_resp.status_code}")
        create_data = create_resp.get_json()
        self.article_id = create_data["article_id"]
        from bson import ObjectId
        self.test_db.articles.update_one(
            {"_id": ObjectId(self.article_id)},
            {"$set": {"author": "authoruser"}}
        )

    def test_delete_article_success_admin(self):
        self.client.set_cookie("access_token", self.admin_token, domain="localhost")
        # Delete the article as admin.
        resp = self.client.delete(f"/api/articles/{self.article_id}")
        self.assertEqual(resp.status_code, 200, "Expected 200 status when admin deletes article")
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article deleted successfully")
        
        # Recreate article for next test
        article_data = {
            "title": "Delete Test Article 3",
            "content": "Content of article to be deleted."
        }
        self.client.set_cookie("access_token", self.moderator_token, domain="localhost")
        create_resp = self.client.post("/api/articles", json=article_data)
        if create_resp.status_code != 201:
            raise Exception(f"Article recreation failed with status {create_resp.status_code}")
        create_data = create_resp.get_json()
        self.article_id = create_data["article_id"]
        from bson import ObjectId
        self.test_db.articles.update_one(
            {"_id": ObjectId(self.article_id)},
            {"$set": {"author": "authoruser"}}
        )

    def test_delete_article_success_author(self):
        # Recreate article for this test (it was deleted by previous test)
        article_data = {
            "title": "Delete Test Article Author",
            "content": "Content of article to be deleted by author."
        }
        self.client.set_cookie("access_token", self.moderator_token, domain="localhost")
        create_resp = self.client.post("/api/articles", json=article_data)
        if create_resp.status_code != 201:
            raise Exception(f"Article recreation failed with status {create_resp.status_code}")
        create_data = create_resp.get_json()
        article_id = create_data["article_id"]
        from bson import ObjectId
        self.test_db.articles.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"author": "authoruser"}}
        )
        
        # Delete the article as author.
        self.client.set_cookie("access_token", self.author_token, domain="localhost")
        resp = self.client.delete(f"/api/articles/{article_id}")
        self.assertEqual(resp.status_code, 200, "Expected 200 status when author deletes own article")
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Article deleted successfully")
        
        # Verify that retrieving the deleted article returns 404.
        get_resp = self.client.get(f"/api/articles/{article_id}")
        self.assertEqual(get_resp.status_code, 404, "Expected 404 status after article deletion")

    def test_delete_article_unauthorized_regular_user(self):
        # Recreate article for this test
        article_data = {
            "title": "Delete Test Article 4",
            "content": "Content of article to be deleted."
        }
        self.client.set_cookie("access_token", self.moderator_token, domain="localhost")
        create_resp = self.client.post("/api/articles", json=article_data)
        if create_resp.status_code != 201:
            raise Exception(f"Article recreation failed with status {create_resp.status_code}")
        create_data = create_resp.get_json()
        article_id = create_data["article_id"]
        from bson import ObjectId
        self.test_db.articles.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"author": "authoruser"}}
        )
        
        # Regular user cannot delete article they didn't create.
        self.client.set_cookie("access_token", self.regular_token, domain="localhost")
        resp = self.client.delete(f"/api/articles/{article_id}")
        self.assertEqual(resp.status_code, 403, "Expected 403 Forbidden when regular user tries to delete article")
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("not authorized", data["error"].lower())

    def test_delete_article_not_found(self):
        self.client.set_cookie("access_token", self.moderator_token, domain="localhost")
        # Attempt to delete a non-existent article.
        resp = self.client.delete("/api/articles/000000000000000000000000")
        self.assertEqual(resp.status_code, 404, "Expected 404 status for non-existent article deletion")
        data = resp.get_json()
        self.assertIn("error", data)
        # Check error message case-insensitively.
        self.assertIn("not found", data["error"].lower())

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(Config.MONGO_DB_NAME)
        cls.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
