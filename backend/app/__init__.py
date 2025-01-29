from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import articles_collection
from .routes import main

def initialize_articles():
    if articles_collection.count_documents({}) == 0:  # Check if collection is empty
        articles_collection.insert_many([
            {
                "title": "First News Article",
                "content": "This is the content of the first news article.",
                "author": "Admin",
                "created_at": "2025-01-28",
                "published_at": "2025-01-29",
                "status": "published"
            },
            {
                "title": "Second News Article",
                "content": "This is the content of the second news article.",
                "author": "Admin",
                "created_at": "2025-01-28",
                "published_at": "2025-01-30",
                "status": "draft"
            }
        ])
    
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Set your JWT secret key here
    CORS(app)
    jwt.init_app(app)  # Initialize JWTManager with the Flask app

    # Initialize data
    initialize_articles()

    with app.app_context():
        #from .routes import main # Import your routes
        app.register_blueprint(main)
        return app




