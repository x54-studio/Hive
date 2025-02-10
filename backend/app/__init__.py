# __init__.py

import signal
import sys
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from .routes import main  # our Blueprint with routes
from .config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for requests from the frontend (adjust origins as needed)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"], resources={r"/*": {"origins": "*"}})
    jwt.init_app(app)

    # Set up Swagger UI for API documentation
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

    # Register the main blueprint containing our API routes
    app.register_blueprint(main)

    # Optional: Graceful shutdown handler
    def shutdown_handler(signum, frame):
        print("Shutdown initiated...")
        # Here you could close database connections, stop background jobs, etc.
        print("Backend shutdown complete.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    return app
