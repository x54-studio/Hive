import bcrypt
import json
import jwt
import time
from apscheduler.schedulers.background import BackgroundScheduler
from bson import ObjectId
from functools import wraps
from flask import Flask, request, Blueprint, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import (
    JWTManager, 
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity, 
    set_access_cookies, 
    set_refresh_cookies, 
    get_jwt
)
from app.models import Article, User, users_collection, articles_collection
from app.config import Config
from pymongo.errors import PyMongoError
from datetime import datetime, timezone, timedelta


# Initialize the background scheduler
scheduler_iterator = 0
scheduler = BackgroundScheduler()


# Define the main Blueprint for routing
main = Blueprint('main', __name__)


def role_required(roles):
    """Decorator to enforce role-based access control"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = get_jwt_identity()
            if user["role"] not in roles:
                return jsonify({"error": "Unauthorized"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper



# -------------------------
# Routes
# -------------------------

@main.route("/")
def home():
    """
    Home route to verify the API is running.
    Returns a welcome message.
    """
    return jsonify({"message": "Welcome to Hive!"})


@main.route("/api/articles", methods=["GET"])
def get_articles():
    """
    Returns a paginated list of articles.
    Query parameters:
      - page: the page number (defaults to 1)
      - limit: number of articles per page (optional, default value)
    """
    default_value = 1
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1
    try:
        limit = int(request.args.get("limit", default_value))
    except ValueError:
        limit = default_value

    skip = (page - 1) * limit

    # Sort articles by creation time (descending: newest first)
    articles_cursor = articles_collection.find({}).sort("created_at", -1).skip(skip).limit(limit)
    articles = []
    for article in articles_cursor:
        # Convert ObjectId to string so it can be JSON serialized
        article["_id"] = str(article["_id"])
        articles.append(article)

    return jsonify(articles)



@main.route("/api/articles", methods=["POST"])
@jwt_required()
def create_article():
    try:
        username = get_jwt_identity()  # ✅ Only returns the username
        claims = get_jwt()  # ✅ Get all JWT claims, including role

        print(f"🆔 JWT Identity: {username}", flush=True)
        print(f"🔑 JWT Claims: {claims}", flush=True)

        if claims.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()
        print("📥 Received Data:", data, flush=True)
        
        if not data or "title" not in data or "content" not in data:
            return jsonify({"error": "Missing title or content"}), 400
        
        new_article = Article.create_article(data["title"], data["content"], username)
        return jsonify({"message": "Article created successfully", "article": new_article}), 201

    except Exception as e:
        print("❌ Error creating article:", str(e), flush=True)
        return jsonify({"error": str(e)}), 500


@main.route("/api/articles/<article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    current_user = get_jwt_identity()
    if current_user["role"] not in ["admin", "moderator"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    Article.update_article(article_id, data["content"])
    return jsonify({"message": "Article updated successfully"}), 200

@main.route("/api/articles/<article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    try:
        if not article_id or article_id == "undefined":
            return jsonify({"error": "Missing article ID"}), 400

        result = Article.delete_article(article_id)
        if result.get("message"):
            return jsonify({"message": "Article deleted successfully"}), 200
        else:
            return jsonify({"error": "Article not found"}), 404
    except Exception as e:
        print("❌ Error deleting article:", str(e))
        return jsonify({"error": str(e)}), 500




@main.route("/api/register", methods=["POST"])
def register():
    data = request.json
    try:
        existing_user = User.find_user_by_email(data["email"])
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        result = User.create_user(data["username"], data["email"], data["password"])
        return jsonify(result), 201 if "message" in result else 500
    except PyMongoError:
        return jsonify({"error": "Database error, please try again later."}), 500


@main.route("/api/login", methods=["POST"])
def login():
    """Authenticate user and issue access & refresh tokens"""
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        user = User.find_user_by_email(email)
        if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return jsonify({"message": "Invalid credentials"}), 401

        # Generate tokens
        access_payload = {
            "sub": user["username"],
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES.seconds)
        }
        access_token = jwt.encode(access_payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

        refresh_payload = {
            "sub": user["username"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=Config.JWT_REFRESH_TOKEN_EXPIRES.seconds)
        }
        refresh_token = jwt.encode(refresh_payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

        # Hash refresh token before storing
        hashed_refresh = bcrypt.hashpw(refresh_token.encode("utf-8"), bcrypt.gensalt())
        User.store_refresh_token(user["username"], hashed_refresh)

        # Create response and set HTTP-only cookies.
        # For local development, 'secure' is set to False so cookies can be sent over HTTP.
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            secure=False,  # Change to False for development (only True in production with HTTPS)
            samesite="Lax",
            max_age=Config.JWT_ACCESS_TOKEN_EXPIRES.seconds
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=False,  # Change to False for development
            samesite="Lax",
            max_age=Config.JWT_REFRESH_TOKEN_EXPIRES.seconds
        )

        return response

    except Exception as e:
        print(f"❌ Login Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500



@main.route("/api/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return jsonify({"message": "Refresh token is missing"}), 401

    try:
        # Decode refresh token
        payload = jwt.decode(refresh_token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        username = payload.get("sub")
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid refresh token"}), 401

    stored_hash = User.get_refresh_token(username)
    if not stored_hash or not bcrypt.checkpw(refresh_token.encode("utf-8"), stored_hash):
        return jsonify({"message": "Invalid refresh token"}), 401

    # Query the database for the user document
    user_doc = users_collection.find_one({"username": username})
    if not user_doc:
        return jsonify({"message": "User not found"}), 404

    # Create new access token with role and email
    new_access_payload = {
        "sub": username,
        "email": user_doc["email"],
        "role": user_doc["role"],
        "exp": datetime.now(timezone.utc) + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES.seconds)
    }
    new_access_token = jwt.encode(new_access_payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

    # Create new refresh token (payload may be kept minimal)
    new_refresh_payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=Config.JWT_REFRESH_TOKEN_EXPIRES.seconds)
    }
    new_refresh_token = jwt.encode(new_refresh_payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    new_hashed_refresh = bcrypt.hashpw(new_refresh_token.encode("utf-8"), bcrypt.gensalt())
    User.store_refresh_token(username, new_hashed_refresh)

    # Set cookies with secure=False for development
    response = make_response(jsonify({"message": "Token refreshed"}))
    response.set_cookie(
        "access_token",
        new_access_token,
        httponly=True,
        secure=True,  # For development; use True in production with HTTPS
        samesite="Lax",
        max_age=Config.JWT_ACCESS_TOKEN_EXPIRES.seconds
    )
    response.set_cookie(
        "refresh_token",
        new_refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=Config.JWT_REFRESH_TOKEN_EXPIRES.seconds
    )
    return response




@main.route("/api/logout", methods=["POST"])
def logout():
    """
    Clear the access and refresh tokens by deleting the cookies.
    This endpoint does not require a valid JWT so that even if the token
    is missing or expired, logout can proceed.
    """
    try:
        response = make_response(jsonify({"message": "Logged out successfully"}))
        # Delete cookies using the same path (and domain if specified) as when they were set
        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/")
        return response, 200
    except Exception as e:
        print("❌ Logout Error:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


@main.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    # Retrieve the username from the JWT "sub" claim (stored as a string)
    username = get_jwt_identity()
    # Retrieve the full JWT claims (which include email and role)
    jwt_claims = get_jwt()
    
    # Construct a user details object
    user_details = {
        "username": username,
        "email": jwt_claims.get("email", "N/A"),
        "role": jwt_claims.get("role", "N/A")
    }
    
    return jsonify(user_details), 200


# -------------------------
# Background Scheduler Tasks
# -------------------------



def publish_news():
    global scheduler_iterator
    """
    Scheduled task to publish news.
    This function is called by the scheduler at regular intervals.
    Replace this placeholder logic with actual news publication logic.
    """    
    print("Publishing in:")
    scheduler_iterator += 1
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Publishing scheduled news... {scheduler_iterator}")


print("Add publish_news to schedular")
scheduler.add_job(publish_news, "interval", minutes=1)
scheduler.start()

# Maintain the main thread to allow the job to execute.
#try:
#    while True:
#        time.sleep(1)
#except (KeyboardInterrupt, SystemExit):
#    # Clean shutdown of the scheduler.
#    scheduler.shutdown()
#    print("Scheduler shut down successfully.")
