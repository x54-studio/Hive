"""
app/__init__.py

This module initializes the Flask application, sets up extensions (JWT, CORS, Swagger UI),
and registers API routes via a blueprint.
It loads configuration from app/config.py.
"""

import signal
import sys
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import main  # Import the blueprint with API routes
from app.config import Config

# Initialize JWT Manager globally.
jwt = JWTManager()

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup CORS: allow requests from the frontend.
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"],
         resources={r"/*": {"origins": "*"}})
    
    # Initialize JWT extension.
    jwt.init_app(app)
    
    # Setup Swagger UI for API documentation.
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)
    
    # Register the main blueprint containing API routes.
    app.register_blueprint(main)
    
    # Optionally, register a signal handler for graceful shutdown.
    def shutdown_handler(signum, frame):
        print("Shutdown initiated...")
        # If needed, perform additional cleanup here.
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    return app
