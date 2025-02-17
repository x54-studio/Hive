# Hive Backend

Hive is a news platform backend built with Flask and MongoDB. This repository contains the API, business logic, data access layers, and supporting utilities for the Hive system.

## Project Structure

```plaintext
backend/
├── app/
│   ├── __init__.py         # Application factory and main setup
│   ├── config.py           # Configuration (loads environment variables)
│   ├── routes.py           # API routes/endpoints
│   ├── error_handlers.py   # Centralized error handling
│   ├── logging_config.py   # Logging configuration (integrated with utilities)
│   └── static/
│       └── swagger.json    # Swagger API documentation
├── services/
│   ├── article_service.py  # Business logic for articles
│   └── user_service.py     # Business logic for user authentication and management
├── repositories/
│   ├── base_article_repository.py  # Abstract interface for article data access
│   ├── base_user_repository.py     # Abstract interface for user data access
│   ├── db.py                      # Database initialization
│   ├── mongo_article_repository.py  # MongoDB implementation for articles
│   └── mongo_user_repository.py     # MongoDB implementation for users
├── utilities/
│   ├── __init__.py         # Utilities package marker
│   ├── custom_exceptions.py  # Custom exception definitions (e.g., RepositoryError)
│   ├── logger.py           # Centralized logging utility
│   └── config_manager.py   # Configuration management
├── tests/
│   ├── test_article_service.py     # Unit tests for article service
│   ├── test_user_service.py        # Unit tests for user service
│   └── test_integration_api.py      # Integration tests covering API endpoints
└── README.md                # This file
```

## Getting Started

### Prerequisites

- **Python 3.11** or higher
- **MongoDB** (local or MongoDB Atlas)
- **Docker** (optional, for containerized deployment)

### Setup

1. Clone the repository.
2. Create a `.env` file in the `backend/` directory with the necessary environment variables. An example:
   ```dotenv
   SECRET_KEY=your_secret_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   MONGO_URI=mongodb://localhost:27017/
   MONGO_DB_NAME=hive_db
   TEST_MONGO_URI=mongodb://localhost:27017/
   TEST_MONGO_DB_NAME=hive_db_test
   FLASK_ENV=development
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To run the Flask application locally:
```bash
python app/__init__.py
```
Alternatively, you can use Docker by building and running the container:
```bash
docker build -t hive-backend .
docker run -p 5000:5000 hive-backend
```

### Testing

Run unit and integration tests with:
```bash
python -m unittest discover -s tests
```

### API Documentation

Access the Swagger UI at:
```
http://localhost:5000/api/docs
```

---
