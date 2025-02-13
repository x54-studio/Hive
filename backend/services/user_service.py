"""
services/user_service.py

Service layer for handling user-related business logic.
This service uses a repository (by default, MongoUserRepository) to perform operations
such as registration, login, token refresh, role updates, and deletion.
"""

import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from repositories.mongo_user_repository import MongoUserRepository

class UserService:
    def __init__(self, jwt_secret_key="", jwt_algorithm="HS256",
                 jwt_access_expires=60, jwt_refresh_expires=180, repository=None):
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm
        self.jwt_access_expires = jwt_access_expires
        self.jwt_refresh_expires = jwt_refresh_expires
        # Allow dependency injection: use the provided repository or default to MongoUserRepository.
        self.repo = repository or MongoUserRepository()

    def register_user(self, username, email, password, role="regular"):
        if self.repo.find_by_email(email):
            return {"error": "User already exists"}
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_pw,
            "role": role,
            "created_at": datetime.now(timezone.utc)
        }
        user_id = self.repo.create_user(user_data)
        return {"message": "User registered successfully!", "user_id": user_id}

    def login_user(self, email, password):
        user = self.repo.find_by_email(email)
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

        # Include email in refresh payload for proper lookup.
        refresh_payload = {
            "sub": user["username"],
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=self.jwt_refresh_expires)
        }
        refresh_token = jwt.encode(refresh_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

        hashed_refresh = bcrypt.hashpw(refresh_token.encode("utf-8"), bcrypt.gensalt())
        self.repo.store_refresh_token(user["username"], hashed_refresh)

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
    
        if not username:
            return {"error": "Username not found in token"}
    
        stored_hash = self.repo.get_refresh_token(username)
        # If stored_hash is a string, encode it; if it's bytes, use it as-is.
        if stored_hash:
            stored_hash_bytes = stored_hash if isinstance(stored_hash, bytes) else stored_hash.encode("utf-8")
        else:
            stored_hash_bytes = None
    
        if not stored_hash_bytes or not bcrypt.checkpw(refresh_token.encode("utf-8"), stored_hash_bytes):
            return {"error": "Invalid refresh token"}
    
        user = self.repo.find_by_username(username)
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
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=self.jwt_refresh_expires)
        }
        new_refresh_token = jwt.encode(new_refresh_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)
        new_hashed_refresh = bcrypt.hashpw(new_refresh_token.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.repo.store_refresh_token(user["username"], new_hashed_refresh)
    
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "message": "Token refreshed successfully"
        }


    def update_user_role(self, email, new_role):
        success = self.repo.update_user_role(email, new_role)
        if success:
            return {"message": "User role updated successfully"}
        else:
            return {"error": "User not found or role update failed"}

    def delete_user(self, email):
        success = self.repo.delete_user(email)
        if success:
            return {"message": "User deleted successfully"}
        else:
            return {"error": "User not found"}
