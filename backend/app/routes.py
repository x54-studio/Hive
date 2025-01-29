import bcrypt
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from .models import User, users_collection, articles_collection
from pymongo.errors import PyMongoError


# Initialize the background scheduler
scheduler = BackgroundScheduler()
scheduler.start()


# Define the main Blueprint for routing
main = Blueprint('main', __name__)

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
    Endpoint to retrieve all articles.
    Articles are fetched from the MongoDB 'articles_collection'.
    The '_id' field is excluded from the response for simplicity.
    Returns:
        JSON response containing a list of articles.
    """
    # Fetch all articles, exclude MongoDB's '_id' field
    articles = list(articles_collection.find({}, {"_id": 0}))
    return jsonify(articles)


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
            access_token = create_access_token(identity={"username": user["username"], "role": user["role"]})
            return jsonify(access_token=access_token)

        return jsonify({"error": "Invalid credentials"}), 401

    except PyMongoError as e:
        print(f"MongoDB Error: {e}")
        return jsonify({"error": "Database error, please try again later."}), 500

@main.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello {current_user['username']}! You have {current_user['role']} access."})


# -------------------------
# Background Scheduler Tasks
# -------------------------

def publish_news():
    """
    Scheduled task to publish news.
    This function is called by the scheduler at regular intervals.
    Replace this placeholder logic with actual news publication logic.
    """
    print("Publishing scheduled news...")


# Add a scheduled job to run the 'publish_news' function every minute
scheduler.add_job(publish_news, "interval", minutes=1)
