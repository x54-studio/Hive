import logging
import signal
import sys
import time
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from .routes import main, scheduler
from .models import client

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"], resources={r"/*": {"origins": "*"}})
    jwt.init_app(app)  # Initialize JWTManager with the Flask app

    # Ensure logs are sent to console immediately
    #handler = logging.StreamHandler(sys.stdout)
    #handler.setLevel(logging.DEBUG)
    #app.logger.addHandler(handler)
    #app.logger.setLevel(logging.DEBUG)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)


    with app.app_context():
        #from .routes import main # Import your routes
        app.register_blueprint(main)
        # Graceful shutdown handler
        def shutdown_handler(signum, frame):
            print("Shutdown initiated...")

            # Stop the scheduler
            if scheduler:
                print("Stopping scheduler...")
                scheduler.shutdown(wait=False)
                print("Scheduler stopped.")

            # Close MongoDB connection
            if client:
                print("Closing MongoDB connection...")
                client.close()
                print("MongoDB connection closed.")

            print("Backend shutdown complete.")
            sys.exit(0)

        # Handle termination signals (Ctrl+C, Docker Stop, etc.)
        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)
        return app


print("herehererer")
