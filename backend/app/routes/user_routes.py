# app/routes/user_routes.py
from flask import Blueprint, request, jsonify, make_response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.user_service import UserService
from app.config import Config

user_routes = Blueprint("user_routes", __name__)
user_service = UserService(Config)

@user_routes.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400
    result = user_service.register_user(
        data["username"], data["email"], data["password"]
    )
    status_code = 201 if "message" in result else 500
    return jsonify(result), status_code

@user_routes.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Missing email or password"}), 400
    result = user_service.login_user(data["email"], data["password"])
    if "error" in result:
        return jsonify(result), 401
    response_data = {"message": result["message"]}
    if current_app.config.get("TESTING", False):
        response_data["access_token"] = result["access_token"]
        response_data["refresh_token"] = result["refresh_token"]
    response = make_response(jsonify(response_data))
    response.set_cookie(
        "access_token",
        result["access_token"],
        httponly=True,
        max_age=int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
    )
    response.set_cookie(
        "refresh_token",
        result["refresh_token"],
        httponly=True,
        max_age=int(Config.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()),
    )
    return response

@user_routes.route("/api/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

@user_routes.route("/api/refresh", methods=["POST"])
def refresh():
    # Lazy import to break circular dependency if needed.
    from services.article_service import ArticleService  # or use user_service.refresh_access_token if refactored
    # For consistency, we'll use user_service from the user_routes context.
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 401
    result = user_service.refresh_access_token(refresh_token)
    if "error" in result:
        return jsonify(result), 401
    response = make_response(jsonify(result))
    secure = current_app.config.get("FLASK_ENV") == "production"
    response.set_cookie("access_token", result["access_token"], httponly=True, secure=secure)
    response.set_cookie("refresh_token", result["refresh_token"], httponly=True, secure=secure)
    return response

@user_routes.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    jwt_claims = get_jwt()
    return jsonify({"username": identity, "claims": jwt_claims})
