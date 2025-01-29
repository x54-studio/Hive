from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from .models import articles_collection
from .routes import main

def initialize_articles():
    if articles_collection is None:
        print("MongoDB is not connected. Skipping article initialization.")
        return
    
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
    app.config.from_object("app.config.Config")
    CORS(app)
    jwt.init_app(app)  # Initialize JWTManager with the Flask app

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)


    # Initialize data
    initialize_articles()

    with app.app_context():
        #from .routes import main # Import your routes
        app.register_blueprint(main)
        return app




