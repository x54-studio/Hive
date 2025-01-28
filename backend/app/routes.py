from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return jsonify({"message": "Welcome to Hive!"})

@main.route("/api/articles", methods=["GET"])
def get_articles():
    articles = [{"id": 1, "title": "First News", "content": "This is the first article."}]
    return jsonify(articles)
