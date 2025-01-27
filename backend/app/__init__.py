from flask import Flask
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Import routes to attach them to the app
from app import routes
