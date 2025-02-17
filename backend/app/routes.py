from flask import Blueprint, request, jsonify, make_response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.user_service import UserService
from services.article_service import ArticleService
from app.config import Config


main = Blueprint('main', __name__)

user_service = UserService(Config)
article_service = ArticleService()


@main.route("/")
def home():
    return jsonify({"message": "Welcome to Hive!"})


@main.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400
    result = user_service.register_user(data["username"], data["email"], data["password"])
    status_code = 201 if "message" in result else 500
    return jsonify(result), status_code


@main.route("/api/login", methods=["POST"])
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
    response.set_cookie("access_token", result["access_token"],
                        httponly=True,
                        max_age=int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()))
    response.set_cookie("refresh_token", result["refresh_token"],
                        httponly=True,
                        max_age=int(Config.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()))
    return response


# In app/routes.py, update the refresh endpoint as follows:
@main.route("/api/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 401
    result = user_service.refresh_access_token(refresh_token)
    if "error" in result:
        return jsonify(result), 401

    response_data = {"message": result["message"]}
    # In testing mode, include tokens in the JSON response for verification
    if current_app.config.get("TESTING", False):
        response_data["access_token"] = result["access_token"]
        response_data["refresh_token"] = result["refresh_token"]

    response = make_response(jsonify(response_data))
    response.set_cookie("access_token", result["access_token"],
                        httponly=True,
                        max_age=int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()))
    response.set_cookie("refresh_token", result["refresh_token"],
                        httponly=True,
                        max_age=int(Config.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()))
    return response


@main.route("/api/articles", methods=["GET"])
def get_articles():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    articles = article_service.get_all_articles(page=page, limit=limit)
    return jsonify(articles)


@main.route("/api/articles", methods=["POST"])
@jwt_required()
def create_article():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data or not all(k in data for k in ("title", "content")):
        return jsonify({"error": "Missing title or content"}), 400
    result = article_service.create_article(data["title"], data["content"], current_user)
    status_code = 201 if "message" in result else 500
    return jsonify(result), status_code


@main.route("/api/articles/<article_id>", methods=["GET"])
def get_article(article_id):
    result = article_service.get_article_by_id(article_id)
    if result is None:
        return jsonify({"error": "Article not found"}), 404
    return jsonify(result)


@main.route("/api/articles/<article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400
    result = article_service.update_article(
        article_id, title=data.get("title"), content=data.get("content")
    )
    status_code = 200 if "message" in result else 404
    return jsonify(result), status_code


@main.route("/api/articles/<article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    result = article_service.delete_article(article_id)
    status_code = 200 if "message" in result else 404
    return jsonify(result), status_code


@main.route("/api/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@main.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    jwt_claims = get_jwt()
    return jsonify({"username": identity, "role": jwt_claims["role"]})
