
# Hive Backend

Hive is a news platform backend built with Flask and MongoDB. This repository contains the API, business logic, data access layers, and supporting utilities for the Hive system.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings (loads environment variables)
│   ├── error_handlers.py    # Centralized error handling
│   ├── routes/
│   │   ├── __init__.py      # Route registration
│   │   ├── article_routes.py  # API endpoints for articles
│   │   ├── main_routes.py     # Home route
│   │   └── user_routes.py     # API endpoints for user actions (register, login, logout, refresh)
├── repositories/
│   ├── base_article_repository.py
│   ├── base_user_repository.py
│   ├── db.py                # Database initialization
│   ├── mongo_article_repository.py
│   └── mongo_user_repository.py
├── services/
│   ├── article_service.py   # Business logic for articles
│   └── user_service.py      # Business logic for user authentication and management
├── utilities/
│   ├── custom_exceptions.py
│   └── logger.py            # Centralized logging
├── __docs__/                # Documentation folder
│   ├── useCases/
│   │   ├── article/
│   │   │   ├── UseCase_CreateArticle.md
│   │   │   ├── UseCase_UpdateArticle.md
│   │   │   ├── UseCase_GetArticle.md
│   │   │   ├── UseCase_ListArticles.md
│   │   │   ├── UseCase_DeleteArticle.md
│   │   │   └── UseCase_SearchArticles.md
│   │   └── user/
│   │       ├── UseCase_RegisterUser.md
│   │       ├── UseCase_LoginUser.md
│   │       ├── UseCase_RefreshToken.md
│   │       ├── UseCase_LogoutUser.md
│   │       └── UseCase_DeleteUser.md
├── __tests__/               # Updated test suite
│   ├── article/
│   │   ├── test_create_article.py
│   │   ├── test_delete_article.py
│   │   ├── test_get_article.py
│   │   ├── test_list_articles.py
│   │   ├── test_search_articles.py
│   │   └── test_update_article.py
│   └── user/
│       ├── test_delete_user.py
│       ├── test_login_user.py
│       ├── test_logout_user.py
│       ├── test_refresh_token.py
│       └── test_register_user.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Getting Started

### Prerequisites

- **Python 3.11** or higher  
- **MongoDB** (local instance or MongoDB Atlas)  
- **Docker** (optional, for containerized deployment)

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/hive-backend.git
   cd hive-backend
   ```

2. **Create Environment Variables:**

   Create a `.env` file in the backend folder with variables similar to:

   ```dotenv
   SECRET_KEY=your_secret_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   MONGO_URI=mongodb://localhost:27017/
   MONGO_DB_NAME=hive_db
   TEST_MONGO_URI=mongodb://localhost:27017/
   TEST_MONGO_DB_NAME=hive_db_test
   FLASK_ENV=development
   TESTING=true
   LOG_LEVEL=WARNING
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   Or using Docker:
   ```bash
   docker build -t hive-backend .
   docker run -p 5000:5000 hive-backend
   ```

## API Documentation

Access the Swagger UI at:
```
http://localhost:5000/api/docs
```

## Testing & Documentation

### Test Directory Structure

All tests have been reorganized under the `__tests__` directory with subdirectories for different domains:

```
backend/
└── __tests__/
    ├── article/
    │   ├── test_create_article.py
    │   ├── test_delete_article.py
    │   ├── test_get_article.py
    │   ├── test_list_articles.py
    │   ├── test_search_articles.py
    │   └── test_update_article.py
    └── user/
        ├── test_delete_user.py
        ├── test_login_user.py
        ├── test_logout_user.py
        ├── test_refresh_token.py
        └── test_register_user.py
```

Older tests (e.g. integration_seeder.py, test_article_service.py, test_integration_api.py, test_refresh.py, test_routes.py, test_ser_service.py) have been replaced by these updated tests and are available in version control if needed.

### Documentation

All use-case documentation is located in the `__docs__/useCases` folder. For example:
- **Article use cases:** `__docs__/useCases/article/UseCase_CreateArticle.md`, `UseCase_UpdateArticle.md`, etc.
- **User use cases:** `__docs__/useCases/user/UseCase_RegisterUser.md`, `UseCase_LoginUser.md`, etc.

### Running the Tests

To run tests using PowerShell, follow these steps:

1. Open PowerShell in the project root directory.
2. Set the required environment variables:
   ```powershell
   PS> clear
   PS> $env:LOG_LEVEL="WARNING"
   PS> $env:TESTING="true"
   ```
3. Run the tests with coverage:
   ```powershell
   PS> coverage run --source=. -m unittest discover -s __tests__ --failfast
   PS> coverage report -m
   ```

### Continuous Integration

CI/CD pipeline to be implemented. Future integration will include:
- Automated test execution from the `__tests__` directory
- Environment variable configuration (e.g., `TESTING`, `LOG_LEVEL`)
- Code coverage reporting and enforcement
- Automated deployment workflows

## License

[Specify your license here]

## Technology Stack

The backend stack for Hive includes:

- **Python 3.8+ / 3.11:** The programming language used.
- **Flask:** The web framework that powers the RESTful API.
- **Flask-CORS:** To handle cross-origin resource sharing.
- **Flask-JWT-Extended & PyJWT:** For JWT-based authentication.
- **Flask-Limiter:** For rate limiting API endpoints.
- **Flask-Swagger-UI:** For interactive API documentation.
- **Pydantic:** For request validation and data modeling.
- **PyMongo:** For interacting with MongoDB.
- **python-dotenv:** For managing environment variables.
- **bcrypt:** For secure password hashing.
- **Docker:** For containerizing and deploying the application.
- **Linting & Testing:** Using tools like Flake8, Pylint, and unittest for code quality and testing.

---
