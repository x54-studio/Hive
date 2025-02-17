import signal
import sys
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import main  # Blueprint with API routes
from app.config import Config
from app.error_handlers import register_error_handlers


jwt = JWTManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True, origins=["http://localhost:3000"],
         resources={r"/*": {"origins": "*"}})

    jwt.init_app(app)

    swagger_url = '/api/docs'
    api_url = '/static/swagger.json'
    swagger_ui = get_swaggerui_blueprint(swagger_url, api_url)
    app.register_blueprint(swagger_ui, url_prefix=swagger_url)

    app.register_blueprint(main)

    register_error_handlers(app)

    @app.after_request
    def set_security_headers(response):
        if request.path.startswith('/api/docs'):
            csp = (
                "default-src 'self'; script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
            )
        else:
            csp = "default-src 'self'"
        response.headers["Content-Security-Policy"] = csp
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    def shutdown_handler(signum, _):
        app.logger.info("Shutdown initiated...", extra={"extra_data": {"signal": signum}})
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    return app
