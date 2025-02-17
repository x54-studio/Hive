from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error("Unhandled Exception: %s", str(e), exc_info=True)
        response = {
            "error": "Internal Server Error",
            "message": str(e)
        }
        return jsonify(response), 500

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found."
        }), 404

    @app.errorhandler(400)
    def bad_request(_):
        return jsonify({
            "error": "Bad Request",
            "message": "The request is invalid or missing parameters."
        }), 400
