# backend/app/routes/user_routes.py
from flask import Blueprint, request, jsonify, make_response, current_app
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from bson import ObjectId
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
    if "error" in result:
        if "already exists" in result["error"]:
            return jsonify(result), 409
        return jsonify(result), 400
    return jsonify(result), 201

@user_routes.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("username_or_email", "password")):
        return jsonify({"error": "Missing email or password"}), 400
    result = user_service.login_user(data["username_or_email"], data["password"])
    if "error" in result:
        return jsonify(result), 401
    response_data = {"message": result["message"]}
    if Config.TESTING:
        response_data["access_token"] = result["access_token"]
        response_data["refresh_token"] = result["refresh_token"]
    resp = make_response(jsonify(response_data))
    resp.set_cookie("access_token", result["access_token"], httponly=True, max_age=int(Config.JWT_ACCESS_TOKEN_EXPIRES))
    resp.set_cookie("refresh_token", result["refresh_token"], httponly=True, max_age=int(Config.JWT_REFRESH_TOKEN_EXPIRES))
    return resp, 200

@user_routes.route("/api/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

@user_routes.route("/api/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token or not refresh_token.strip():
        return jsonify({"error": "Missing refresh token"}), 401
    result = user_service.refresh_access_token(refresh_token)
    if "error" in result:
        return jsonify(result), 401
    response_data = {"message": result["message"]}
    if Config.TESTING:
        response_data["access_token"] = result["access_token"]
        response_data["refresh_token"] = result["refresh_token"]
    resp = make_response(jsonify(response_data), 200)
    resp.set_cookie("access_token", result["access_token"], httponly=True)
    resp.set_cookie("refresh_token", result["refresh_token"], httponly=True)
    return resp

@user_routes.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    jwt_claims = get_jwt()
    return jsonify({"username": identity, "claims": jwt_claims})

# Admin User Management Endpoints

@user_routes.route("/api/users", methods=["POST"])
@jwt_required()
def create_user_admin():
    claims = get_jwt()
    if claims.get("role", "").lower() != "admin":
        return jsonify({"error": "User not authorized to create users"}), 403
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400
    result = user_service.register_user(
        data["username"], data["email"], data["password"]
    )
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 201

@user_routes.route("/api/users/<string:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    try:
        ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user id format"}), 400
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400
    claims = get_jwt()
    if claims.get("role", "").lower() != "admin":
        return jsonify({"error": "User not authorized to update users"}), 403
    result = user_service.update_user(user_id, data)
    if "error" in result:
        if "not found" in result["error"].strip().lower():
            return jsonify(result), 404
        return jsonify(result), 400
    return jsonify(result), 200

@user_routes.route("/api/users/<string:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Invalid user id format"}), 400
    claims = get_jwt()
    if claims.get("role", "").lower() != "admin":
        return jsonify({"error": "User not authorized to delete users"}), 403
    result = user_service.delete_user(user_id)
    if "message" in result:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

# New Route: List Users with Pagination
@user_routes.route("/api/users", methods=["GET"])
@jwt_required()
def list_users():
    claims = get_jwt()
    if claims.get("role", "").lower() != "admin":
        return jsonify({"error": "User not authorized to view users"}), 403
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 10))
        if page < 1 or size < 1:
            raise ValueError("Pagination parameters must be positive integers")
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    skip = (page - 1) * size
    cursor = user_service.repo.users.find({}).sort("username", 1).skip(skip).limit(size)
    users = []
    for user in cursor:
        # Remove sensitive fields and convert ObjectId to string.
        user["_id"] = str(user["_id"])
        if "password" in user:
            user.pop("password")
        if "refresh_token" in user:
            user.pop("refresh_token")
        users.append(user)
    return jsonify(users), 200
