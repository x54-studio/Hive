# Hive

Hive is a news platform built with a Flask backend and a React frontend. This repository contains the backend application along with supporting services, repositories, tests, and Docker configuration.

## Project Structure

```plaintext
backend/
├── app/
│   ├── __init__.py         # Application factory and main setup
│   ├── config.py           # Application configuration (loads .env)
│   ├── error_handlers.py   # Centralized error handling
│   ├── logging_config.py   # Structured logging setup
│   ├── models.py           # Data models (User, Article)
│   ├── routes.py           # API endpoints
│   └── static/
│       └── swagger.json    # Swagger API documentation
├── repositories/
│   ├── base_article_repository.py
│   ├── base_user_repository.py
│   ├── db.py               # Database initialization
│   ├── mongo_article_repository.py
│   ├── mongo_user_repository.py
│   └── proxy_user_repository.py
├── services/
│   ├── article_service.py
│   └── user_service.py
├── tests/                  # Unit and integration tests
│   ├── test_article_service.py
│   ├── test_cookie_set.py
│   ├── test_routes.py
│   └── test_user_service.py
├── .env                    # Environment variables (ignored in git)
├── Dockerfile              # Dockerfile for backend container
├── package.json            # Frontend and testing configuration
├── README.md               # This documentation
├── requirements.txt        # Python dependencies
└── run.py                  # Entry point for the Flask app
```

## Getting Started

### Prerequisites

- **Python 3.11** or higher  
- **Docker** (for containerized deployment)  
- **MongoDB Atlas** (or local MongoDB for development)  
- **Node.js** (if working with the React frontend)

### Environment Variables

Create a `.env` file in the root directory (this file is ignored by Git). Below is an example:

```dotenv
SECRET_KEY='your_secret_key_here'
MONGO_URI="mongodb+srv://user:your_password@clusterm0.zrr90.mongodb.net/?retryWrites=true&w=majority&tls=true&appName=ClusterM0"
TEST_MONGO_URI="mongodb://localhost:27017/"
MONGO_DB_NAME="hive_db"
TEST_MONGO_DB_NAME="hive_db_test"
JWT_ACCESS_TOKEN_EXPIRES=1
JWT_REFRESH_TOKEN_EXPIRES=3
FLASK_ENV=development
```

**SECRET_KEY**: Used for Flask sessions and CSRF protection.
**MONGO_URI**: Connection string for MongoDB Atlas in production.
**TEST_MONGO_URI**: Connection string for local testing.
**JWT_ACCESS_TOKEN_EXPIRES / JWT_REFRESH_TOKEN_EXPIRES**: Expiration times for tokens (in minutes).
**FLASK_ENV**: Set to production for production deployment; otherwise, use development.


## Testing

We use **unittest** for unit and integration tests. Our tests are organized in the `tests/` directory.

### Running Tests

To run all tests, execute:

```bash
python -m unittest discover -s tests
