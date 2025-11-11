# app/routes/article_routes.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

article_routes = Blueprint("article_routes", __name__)

@article_routes.route("/api/articles", methods=["GET"])
def get_articles():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 2))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    # Call the service method with page and limit.
    articles = current_app.article_service.get_all_articles(page=page, limit=limit)
    return jsonify(articles)

@article_routes.route("/api/articles", methods=["POST"])
@jwt_required()
def create_article():
    # Retrieve the JWT claims
    claims = get_jwt()
    user_role = claims.get("role", "regular")  # Default to "regular" if not provided

    # Only allow moderators and admins to create articles
    if user_role not in ["moderator", "admin"]:
        return jsonify({"error": "User not authorized to create articles"}), 403

    data = request.get_json()
    if not data or not all(k in data for k in ("title", "content")):
        return jsonify({"error": "Missing title or content"}), 400

    # Use the current user's identity (username) as the author
    author = get_jwt_identity()
    result = current_app.article_service.create_article(data["title"], data["content"], author)
    status_code = 201 if "message" in result else 500
    return jsonify(result), status_code

@article_routes.route("/api/articles/<article_id>", methods=["GET"])
def get_article(article_id):
    result = current_app.article_service.get_article_by_id(article_id)
    if result is None:
        return jsonify({"error": "Article not found"}), 404
    # Rename _id to article_id in the response
    if "_id" in result:
        result["article_id"] = result.pop("_id")
    return jsonify(result)

@article_routes.route("/api/articles/<article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    # Retrieve the JWT claims and identity
    claims = get_jwt()
    user_role = claims.get("role", "regular")
    username = get_jwt_identity()
    
    # Get the article to check author
    article = current_app.article_service.get_article_by_id(article_id)
    if article is None:
        return jsonify({"error": "Article not found"}), 404
    
    # Check authorization: admin/moderator can update any article, author can update their own
    article_author = article.get("author")
    if user_role not in ["admin", "moderator"] and username != article_author:
        return jsonify({"error": "User not authorized to update this article"}), 403
    
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
    # Retrieve the JWT claims and identity
    claims = get_jwt()
    user_role = claims.get("role", "regular")
    username = get_jwt_identity()
    
    # Get the article to check author
    article = current_app.article_service.get_article_by_id(article_id)
    if article is None:
        return jsonify({"error": "Article not found"}), 404
    
    # Check authorization: admin/moderator can delete any article, author can delete their own
    article_author = article.get("author")
    if user_role not in ["admin", "moderator"] and username != article_author:
        return jsonify({"error": "User not authorized to delete this article"}), 403
    
    result = current_app.article_service.delete_article(article_id)
    status_code = 200 if "message" in result else 404
    return jsonify(result), status_code

@article_routes.route("/api/articles/search", methods=["GET"])
def search_articles():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing search query parameter"}), 400
    # Assume that article_service.search_articles(query) performs the search.
    results = current_app.article_service.search_articles(query)
    return jsonify(results), 200
