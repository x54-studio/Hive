from flask import Blueprint, jsonify

main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/")
def home():
    return jsonify({"message": "Welcome to Hive!"}), 200


@main_routes.route("/home")
def home_alt():
    return jsonify({"message": "Welcome to Hive!"}), 200
