from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log error details here if desired
        app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        response = {
            "error": "Internal Server Error",
            "message": str(e)
        }
        return jsonify(response), 500

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found."
            }), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "error": "Bad Request",
            "message": "The request is invalid or missing parameters."
            }), 400
