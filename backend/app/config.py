from dotenv import load_dotenv
from datetime import timedelta
import os

# Load the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)  
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
    DEBUG = True
