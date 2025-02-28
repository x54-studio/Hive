import datetime
from datetime import timezone, timedelta
import bcrypt
import jwt
from utilities.logger import get_logger
from repositories.mongo_user_repository import MongoUserRepository


logger = get_logger(__name__)


class UserService:
    def __init__(self, config, repository=None):
        self.jwt_secret_key = config.JWT_SECRET_KEY
        self.jwt_algorithm = config.JWT_ALGORITHM
        self.jwt_access_expires = int(config.JWT_ACCESS_TOKEN_EXPIRES)
        self.jwt_refresh_expires = int(config.JWT_REFRESH_TOKEN_EXPIRES)
        self.repo = repository if repository is not None else MongoUserRepository()
        logger.info(
            "UserService initialized", extra={"jwt_algorithm": self.jwt_algorithm}
        )

    def register_user(self, username, email, password, role="regular"):
        if not username or not email or not password:
            return {"error": "Missing required fields"}

        # Check if user already exists
        if self.repo.find_by_username(username) or self.repo.find_by_email(email):
            return {"error": "User already exists"}

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_pw,
            "role": role
        }
        user_id = self.repo.create_user(user_data)

        return {"message": "User registered successfully!", "user_id": user_id}


    def login_user(self, username_or_email, password):
        # Decide if input is likely an email or a username
        if "@" in username_or_email:
            user = self.repo.find_by_email(username_or_email)
        else:
            user = self.repo.find_by_username(username_or_email)

        if not user:
            return {"error": "User not found"}

        # Check password
        if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return {"error": "Invalid credentials"}

        # Generate tokens if valid
        now = datetime.datetime.now(timezone.utc)
        access_payload = {
            "sub": user["username"],
            "email": user["email"],
            "role": user["role"],
            "iat": now.timestamp(),
            "exp": (now + datetime.timedelta(seconds=self.jwt_access_expires)).timestamp(),
        }
        access_token = jwt.encode(access_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

        refresh_payload = {
            "sub": user["username"],
            "email": user["email"],
            "iat": now.timestamp(),
            "exp": (now + datetime.timedelta(seconds=self.jwt_refresh_expires)).timestamp(),
        }
        refresh_token = jwt.encode(refresh_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

        # Hash and store the refresh token in DB
        hashed_refresh = bcrypt.hashpw(refresh_token.encode("utf-8"), bcrypt.gensalt())
        self.repo.store_refresh_token(user["username"], hashed_refresh)

        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def refresh_access_token(self, refresh_token):
        import datetime
        from datetime import timezone
        # Step 1: Decode without verifying signature/expiration to check token structure
        try:
            unverified_payload = jwt.decode(
                refresh_token, 
                options={"verify_signature": False, "verify_exp": False}
            )
        except Exception:
            return {"error": "Invalid refresh token"}

        if "sub" not in unverified_payload or "exp" not in unverified_payload:
            return {"error": "Invalid refresh token"}

        now_ts = datetime.datetime.now(timezone.utc).timestamp()
        try:
            token_exp = float(unverified_payload["exp"])
        except Exception as e:
            return {"error": "Invalid refresh token"}

        # Explicitly check: if current time is greater than token expiration, it's expired.
        if now_ts > token_exp:
            return {"error": "Refresh token expired"}

        # Step 3: Now verify signature and get the full payload
        try:
            payload = jwt.decode(refresh_token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])
            username = payload.get("sub")
        except jwt.InvalidTokenError:
            return {"error": "Invalid refresh token"}

        # Step 4: Verify stored token hash
        stored_hash = self.repo.get_refresh_token(username)
        if not stored_hash:
            return {"error": "Invalid refresh token"}
        stored_hash_bytes = stored_hash if isinstance(stored_hash, bytes) else stored_hash.encode("utf-8")
        if not bcrypt.checkpw(refresh_token.encode("utf-8"), stored_hash_bytes):
            return {"error": "Invalid refresh token"}

        # Step 5: Generate new tokens
        user = self.repo.find_by_username(username)
        if not user:
            return {"error": "User not found"}

        now = datetime.datetime.now(timezone.utc)
        access_payload = {
            "sub": user["username"],
            "email": user["email"],
            "role": user["role"],
            "iat": now.timestamp(),
            "exp": (now + datetime.timedelta(seconds=self.jwt_access_expires)).timestamp(),
        }
        new_access_token = jwt.encode(access_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

        new_refresh_payload = {
            "sub": user["username"],
            "email": user["email"],
            "iat": now.timestamp(),
            "exp": (now + datetime.timedelta(seconds=self.jwt_refresh_expires)).timestamp(),
        }
        new_refresh_token = jwt.encode(new_refresh_payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)
        new_hashed_refresh = bcrypt.hashpw(new_refresh_token.encode("utf-8"), bcrypt.gensalt())
        self.repo.store_refresh_token(user["username"], new_hashed_refresh)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "message": "Token refreshed successfully"
        }

    def update_user_role(self, email, new_role):
        success = self.repo.update_user_role(email, new_role)
        if success:
            logger.info(
                "User role updated", extra={"email": email, "new_role": new_role}
            )
            return {"message": "User role updated successfully"}
        logger.warning(
            "Failed to update user role", extra={"email": email, "new_role": new_role}
        )
        return {"error": "User not found or role update failed"}

    def delete_user(self, username):
        # Use the repository method to delete by username
        success = self.repo.delete_user(username)
        if success:
            logger.info("User deleted", extra={"username": username})
            return {"message": "User deleted successfully"}
        logger.warning("Failed to delete user", extra={"username": username})
        return {"error": "User not found"}
