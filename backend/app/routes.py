from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Blueprint, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from .models import articles_collection

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


@main.route("/api/login", methods=["POST"])
def login():
    """
    Endpoint for user login.
    Validates the username and password, and generates a JWT access token.
    Note: This is a dummy implementation. Replace with real authentication logic.
    Returns:
        JSON response with the access token if successful,
        or an error message if credentials are invalid.
    """
    # Extract username and password from request body
    username = request.json.get("username")
    password = request.json.get("password")

    # Simple validation for demo purposes
    if username == "admin" and password == "password":
        # Create a JWT access token for the user
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    # Return error for invalid credentials
    return jsonify({"error": "Invalid credentials"}), 401


@main.route("/api/protected", methods=["GET"])
@jwt_required()  # Protect this endpoint with JWT authentication
def protected():
    """
    Example of a protected endpoint.
    Only accessible to authenticated users with a valid JWT token.
    Returns:
        JSON message confirming access.
    """
    return jsonify(message="You have access!"), 200


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
