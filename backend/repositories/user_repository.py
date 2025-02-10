# user_repository.py

from pymongo import MongoClient, errors

class UserRepository:
    def __init__(self, mongo_uri, db_name="hive_db"):
        self.client = MongoClient(mongo_uri)
        # Assumes that the default database is set in the URI or by the client.
        self.db = self.client.get_database(db_name)
        self.users = self.db.users

    def find_by_email(self, email):
        try:
            return self.users.find_one({"email": email})
        except errors.PyMongoError as e:
            raise Exception(f"Error finding user by email: {str(e)}")

    def find_by_username(self, username):
        try:
            return self.users.find_one({"username": username})
        except errors.PyMongoError as e:
            raise Exception(f"Error finding user by username: {str(e)}")

    def create_user(self, user_data):
        try:
            result = self.users.insert_one(user_data)
            return str(result.inserted_id)
        except errors.PyMongoError as e:
            raise Exception(f"Error creating user: {str(e)}")

    def update_user_role(self, email, new_role):
        try:
            result = self.users.update_one({"email": email}, {"$set": {"role": new_role}})
            return result.modified_count > 0
        except errors.PyMongoError as e:
            raise Exception(f"Error updating user role: {str(e)}")

    def delete_user(self, email):
        try:
            result = self.users.delete_one({"email": email})
            return result.deleted_count > 0
        except errors.PyMongoError as e:
            raise Exception(f"Error deleting user: {str(e)}")

    def store_refresh_token(self, username, hashed_refresh):
        try:
            self.users.update_one({"username": username}, {"$set": {"refresh_token": hashed_refresh}})
        except errors.PyMongoError as e:
            raise Exception(f"Error storing refresh token: {str(e)}")

    def get_refresh_token(self, username):
        try:
            user = self.find_by_username(username)
            if user:
                return user.get("refresh_token")
            return None
        except errors.PyMongoError as e:
            raise Exception(f"Error getting refresh token: {str(e)}")

    def close(self):
        self.client.close()
