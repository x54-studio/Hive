import os
import unittest
import jwt
from pymongo import MongoClient
from app.config import Config
from services.user_service import UserService
from repositories.mongo_user_repository import MongoUserRepository

class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["TESTING"] = "true"
        cls.config = Config()
        cls.mongo_client = MongoClient(cls.config.MONGO_URI)
        cls.test_db = cls.mongo_client[cls.config.MONGO_DB_NAME]

    def setUp(self):
        self.repo = MongoUserRepository()
        self.user_service = UserService(Config, repository=self.repo)
        # Clear test users collection before each test
        self.repo.users.delete_many({})

    def test_register_user_success(self):
        result = self.user_service.register_user("user1", "user1@example.com", "password")
        self.assertIn("message", result)
        self.assertEqual(result["message"], "User registered successfully!")
        self.assertIn("user_id", result)

    def test_register_user_duplicate(self):
        self.user_service.register_user("user1", "user1@example.com", "password")
        result = self.user_service.register_user("user1", "user1@example.com", "password")
        self.assertIn("error", result)

    def test_login_user_invalid(self):
        result = self.user_service.login_user("nonexistent@example.com", "password")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "User not found")

    def test_login_user_success(self):
        self.user_service.register_user("user2", "user2@example.com", "password")
        result = self.user_service.login_user("user2@example.com", "password")
        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)
        self.assertIn("message", result)
        access_payload = jwt.decode(
            result["access_token"],
            Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
        )
        self.assertEqual(access_payload.get("sub"), "user2")

    def test_update_user_role_success(self):
        self.user_service.register_user("user3", "user3@example.com", "password")
        result = self.user_service.update_user_role("user3@example.com", "admin")
        self.assertIn("message", result)
        user = self.repo.find_by_email("user3@example.com")
        self.assertEqual(user["role"], "admin")

    def test_delete_user_success(self):
        self.user_service.register_user("user4", "user4@example.com", "password")
        result = self.user_service.delete_user("user4@example.com")
        self.assertIn("message", result)
        self.assertIsNone(self.repo.find_by_email("user4@example.com"))

    def tearDown(self):
        # Clear test users collection after each test
        self.repo.users.delete_many({})

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(cls.config.MONGO_DB_NAME)
        cls.mongo_client.close()


if __name__ == "__main__":
    unittest.main()
