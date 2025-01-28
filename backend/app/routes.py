from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return jsonify({"message": "Welcome to Hive!"})

@main.route("/api/articles")
def get_articles():
    return jsonify({"articles": []})
