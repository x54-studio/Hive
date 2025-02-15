import signal
import os
import sys
import logging
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import main  # Blueprint with API routes
from app.config import Config
from app.error_handlers import register_error_handlers
from app.logging_config import setup_logging


jwt = JWTManager()


def create_app():
    # Setup structured logging
    is_testing = os.getenv("TESTING", "false").lower() == "true"
    setup_logging(logging.INFO if is_testing else logging.WARNING)

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True, origins=["http://localhost:3000"],
         resources={r"/*": {"origins": "*"}})

    jwt.init_app(app)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

    app.register_blueprint(main)

    # Register centralized error handlers
    register_error_handlers(app)

    # Add security headers
    @app.after_request
    def set_security_headers(response):
        # Relax CSP for Swagger UI endpoints (e.g. /api/docs and its subpaths)
        if request.path.startswith('/api/docs'):
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:;"
            )
        else:
            csp = "default-src 'self'"
        response.headers["Content-Security-Policy"] = csp
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    def shutdown_handler(signum, frame):
        app.logger.info("Shutdown initiated...", extra={"extra_data": {"signal": signum}})
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    return app
