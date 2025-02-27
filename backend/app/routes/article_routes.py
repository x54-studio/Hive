# app/routes/article_routes.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

article_routes = Blueprint("article_routes", __name__)

@article_routes.route("/api/articles", methods=["GET"])
def get_articles():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    articles = current_app.article_service.get_all_articles(page=page, limit=limit)
    return jsonify(articles)

@article_routes.route("/api/articles", methods=["POST"])
@jwt_required()
def create_article():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data or not all(k in data for k in ("title", "content")):
        return jsonify({"error": "Missing title or content"}), 400
    result = current_app.article_service.create_article(data["title"], data["content"], current_user)
    status_code = 201 if "message" in result else 500
    return jsonify(result), status_code

@article_routes.route("/api/articles/<article_id>", methods=["GET"])
def get_article(article_id):
    result = current_app.article_service.get_article_by_id(article_id)
    if result is None:
        return jsonify({"error": "Article not found"}), 404
    return jsonify(result)

@article_routes.route("/api/articles/<article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400
    result = current_app.article_service.update_article(
        article_id, title=data.get("title"), content=data.get("content")
    )
    status_code = 200 if "message" in result else 404
    return jsonify(result), status_code

@article_routes.route("/api/articles/<article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    result = current_app.article_service.delete_article(article_id)
    status_code = 200 if "message" in result else 404
    return jsonify(result), status_code
