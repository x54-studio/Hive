from app import app  # Import the `app` object from `__init__.py`
from flask import jsonify

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})
