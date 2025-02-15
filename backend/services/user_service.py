import logging
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from repositories.mongo_user_repository import MongoUserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, jwt_secret_key, jwt_algorithm, jwt_access_expires,
                 jwt_refresh_expires, repository=None):
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm
        self.jwt_access_expires = jwt_access_expires
        self.jwt_refresh_expires = jwt_refresh_expires
        self.repo = repository if repository is not None else MongoUserRepository()
        logger.info("UserService initialized",
                    extra={"jwt_algorithm": self.jwt_algorithm})

    def register_user(self, username, email, password, role="regular"):
        if self.repo.find_by_email(email):
            logger.warning("Attempted to register user with existing email",
                           extra={"email": email})
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
        logger.info("User registered successfully",
                    extra={"email": email, "user_id": user_id})
        return {"message": "User registered successfully!", "user_id": user_id}

    def login_user(self, email, password):
        user = self.repo.find_by_email(email)
        if not user:
            logger.warning("Login attempt for non-existent user", extra={"email": email})
            return {"error": "User not found"}
        if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            logger.warning("Invalid credentials for login", extra={"email": email})
            return {"error": "Invalid credentials"}

        now = datetime.now(timezone.utc)
        access_payload = {
            "sub": user["username"],
            "email": user["email"],
            "role": user["role"],
            "iat": now.timestamp(),
            "exp": (now + timedelta(seconds=self.jwt_access_expires)).timestamp()
        }
        access_token = jwt.encode(access_payload, self.jwt_secret_key,
                                  algorithm=self.jwt_algorithm)

        refresh_payload = {
            "sub": user["username"],
            "email": user["email"],
            "iat": now.timestamp(),
            "exp": (now + timedelta(seconds=self.jwt_refresh_expires)).timestamp()
        }
        refresh_token = jwt.encode(refresh_payload, self.jwt_secret_key,
                                   algorithm=self.jwt_algorithm)

        hashed_refresh = bcrypt.hashpw(refresh_token.encode("utf-8"),
                                       bcrypt.gensalt())
        self.repo.store_refresh_token(user["username"], hashed_refresh)
        logger.info("User logged in successfully", extra={"email": email})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Login successful"
        }

    def refresh_access_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.jwt_secret_key,
                                 algorithms=[self.jwt_algorithm])
            username = payload.get("sub")
        except jwt.ExpiredSignatureError:
            logger.warning("Refresh token expired", extra={})
            return {"error": "Refresh token expired"}
        except jwt.InvalidTokenError:
            logger.warning("Invalid refresh token", extra={})
            return {"error": "Invalid refresh token"}

        if not username:
            logger.error("Username not found in token payload",
                         extra={"refresh_token": refresh_token})
            return {"error": "Username not found in token"}

        stored_hash = self.repo.get_refresh_token(username)
        stored_hash_bytes = (stored_hash if isinstance(stored_hash, bytes)
                             else (stored_hash.encode("utf-8")
                                   if stored_hash else None))

        if not stored_hash_bytes or not bcrypt.checkpw(refresh_token.encode("utf-8"),
                                                       stored_hash_bytes):
            logger.warning("Refresh token mismatch", extra={"username": username})
            return {"error": "Invalid refresh token"}

        user = self.repo.find_by_username(username)
        if not user:
            logger.error("User not found during token refresh",
                         extra={"username": username})
            return {"error": "User not found"}

        now = datetime.now(timezone.utc)
        new_access_payload = {
            "sub": user["username"],
            "email": user["email"],
            "role": user["role"],
            "iat": now.timestamp(),
            "exp": (now + timedelta(seconds=self.jwt_access_expires)).timestamp()
        }
        new_access_token = jwt.encode(new_access_payload, self.jwt_secret_key,
                                      algorithm=self.jwt_algorithm)

        new_refresh_payload = {
            "sub": user["username"],
            "email": user["email"],
            "iat": now.timestamp(),
            "exp": (now + timedelta(seconds=self.jwt_refresh_expires)).timestamp()
        }
        new_refresh_token = jwt.encode(new_refresh_payload, self.jwt_secret_key,
                                       algorithm=self.jwt_algorithm)
        new_hashed_refresh = bcrypt.hashpw(new_refresh_token.encode("utf-8"),
                                           bcrypt.gensalt()).decode("utf-8")
        self.repo.store_refresh_token(user["username"], new_hashed_refresh)
        logger.info("Refreshed tokens for user", extra={"username": username})
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "message": "Token refreshed successfully"
        }

    def update_user_role(self, email, new_role):
        success = self.repo.update_user_role(email, new_role)
        if success:
            logger.info("User role updated",
                        extra={"email": email, "new_role": new_role})
            return {"message": "User role updated successfully"}
        else:
            logger.warning("Failed to update user role",
                           extra={"email": email, "new_role": new_role})
            return {"error": "User not found or role update failed"}

    def delete_user(self, email):
        success = self.repo.delete_user(email)
        if success:
            logger.info("User deleted", extra={"email": email})
            return {"message": "User deleted successfully"}
        else:
            logger.warning("Failed to delete user", extra={"email": email})
            return {"error": "User not found"}
