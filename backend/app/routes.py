import bcrypt
import json
from apscheduler.schedulers.background import BackgroundScheduler
from functools import wraps
from flask import Flask, request, Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import (
    JWTManager, 
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity, 
    get_jwt
)
from app.models import Article, User, users_collection, articles_collection
from pymongo.errors import PyMongoError
from datetime import datetime, timezone, timedelta
import time

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
    articles = Article.get_all_articles()
    result = jsonify(articles)
    print(f"'/api/articles', methods=['GET'] - {result}")
    return result

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


@main.route("/api/articlesOld0", methods=["POST"])
@jwt_required()
#@role_required(["admin"])
def create_article_old0():
    print("Create new article. 0")
    current_user = get_jwt_identity()
    if current_user["role"] not in ["admin"]:
        return jsonify({"error": "Unauthorized"}), 403

    print("Create new article.")
    data = request.json
    new_article = Article.create_article(data["title"], data["content"], current_user["username"])
    return jsonify(new_article), 201

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
        
        username = get_jwt_identity()  # Get username
        claims = get_jwt()  # Get full JWT payload (includes role)
        
        print("🆔 JWT Identity:", username, flush=True)
        print("🔑 JWT Claims:", claims, flush=True)

        if claims.get("role") != "admin":  # Use `get()` to avoid errors
            return jsonify({"error": "Unauthorized"}), 403

        # Proceed with deletion logic...
        print(f"🗑️ Deleting Article ID: {article_id}", flush=True)

        result = Article.delete_article(article_id)

        if result:
            return jsonify({"message": "Article deleted successfully"}), 200
        else:
            return jsonify({"error": "Article not found"}), 404

    except Exception as e:
        print("❌ Error deleting article:", str(e), flush=True)
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
    data = request.json

    try:
        if users_collection is None:  # Fix boolean check
            return jsonify({"error": "Database connection failed. Please try again later."}), 500

        user = User.find_user_by_email(data["email"])
        if user is None:
            return jsonify({"error": "Invalid credentials"}), 401

        if bcrypt.checkpw(data["password"].encode("utf-8"), user["password"]):
            # Store only `username` in `sub`, and store `role` in claims
            access_token = create_access_token(
                identity=user["username"],  # Only username in identity
                additional_claims={"role": user["role"]}
            )
            refresh_token = create_refresh_token(identity=user["username"])  # Issue refresh token

            return jsonify(access_token=access_token, refresh_token=refresh_token)

        return jsonify({"error": "Invalid credentials"}), 401

    except PyMongoError as e:
        print(f"MongoDB Error: {e}")
        return jsonify({"error": "Database error, please try again later."}), 500


@main.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    print("Refreshing access token")
    identity = get_jwt_identity()
    claims = get_jwt()
    new_access_token = create_access_token(identity=identity, additional_claims={"role": claims.get("role")})

    return jsonify(access_token=new_access_token)



@main.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello {current_user['username']}! You have {current_user['role']} access."})


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
