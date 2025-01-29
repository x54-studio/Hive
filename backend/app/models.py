import bcrypt
from pymongo import MongoClient

client = MongoClient("mongodb+srv://CosmicToast:kwZgKXCGRIff2XTS@clusterm0.zrr90.mongodb.net/?retryWrites=true&w=majority&readPreference=primary&appName=ClusterM0")
db = client.hive_db
users_collection = db.users
articles_collection = db.articles

class User:
    @staticmethod
    def create_user(username, email, password, role="regular"):
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {"username": username, "email": email, "password": hashed_pw, "role": role}
        users_collection.insert_one(user_data)

    @staticmethod
    def find_user_by_email(email):
        return users_collection.find_one({"email": email})