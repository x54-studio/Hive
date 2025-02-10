# user_service.py

import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, mongo_uri, jwt_secret_key, jwt_algorithm="HS256", jwt_access_expires=60, jwt_refresh_expires=180, db_name="hive_db"):
        """
        :param mongo_uri: MongoDB connection string.
        :param jwt_secret_key: Secret key for signing JWTs.
        :param jwt_algorithm: Algorithm to sign JWT tokens.
        :param jwt_access_expires: Access token expiration in seconds.
        :param jwt_refresh_expires: Refresh token expiration in seconds.
        """
        self.user_repo = UserRepository(mongo_uri, db_name)
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm
        self.jwt_access_expires = jwt_access_expires  # e.g., 60 seconds
        self.jwt_refresh_expires = jwt_refresh_expires  # e.g., 180 seconds

    def register_user(self, username, email, password, role="regular"):
        if self.user_repo.find_by_email(email):
            return {"error": "User already exists"}
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_pw,
            "role": role,
            "created_at": datetime.now(timezone.utc)
        }
        user_id = self.user_repo.create_user(user_data)
        return {"message": "User registered successfully!", "user_id": user_id}

    def login_user(self, email, password):
        user = self.user_repo.find_by_email(email)
        if not user:
            return {"error": "User not found"}
        if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return {"error": "Invalid credentials"}

        access_payload = {
            "sub": user["username"],
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=self.jwt_access_expires)
        }
        access_token = jwt.encode(access_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

        refresh_payload = {
            "sub": user["username"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=self.jwt_refresh_expires)
        }
        refresh_token = jwt.encode(refresh_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

        hashed_refresh = bcrypt.hashpw(refresh_token.encode("utf-8"), bcrypt.gensalt())
        self.user_repo.store_refresh_token(user["username"], hashed_refresh)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Login successful"
        }

    def refresh_access_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])
            username = payload.get("sub")
        except jwt.ExpiredSignatureError:
            return {"error": "Refresh token expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid refresh token"}

        stored_hash = self.user_repo.get_refresh_token(username)
        if not stored_hash or not bcrypt.checkpw(refresh_token.encode("utf-8"), stored_hash):
            return {"error": "Invalid refresh token"}

        user = self.user_repo.find_by_username(username)
        if not user:
            return {"error": "User not found"}

        new_access_payload = {
            "sub": user["username"],
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=self.jwt_access_expires)
        }
        new_access_token = jwt.encode(new_access_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

        new_refresh_payload = {
            "sub": user["username"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=self.jwt_refresh_expires)
        }
        new_refresh_token = jwt.encode(new_refresh_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)
        new_hashed_refresh = bcrypt.hashpw(new_refresh_token.encode("utf-8"), bcrypt.gensalt())
        self.user_repo.store_refresh_token(user["username"], new_hashed_refresh)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "message": "Token refreshed successfully"
        }

    def update_user_role(self, email, new_role):
        success = self.user_repo.update_user_role(email, new_role)
        if success:
            return {"message": "User role updated successfully"}
        else:
            return {"error": "User not found or role update failed"}

    def delete_user(self, email):
        success = self.user_repo.delete_user(email)
        if success:
            return {"message": "User deleted successfully"}
        else:
            return {"error": "User not found"}

    def close(self):
        self.user_repo.close()
