## HIVE PROJECT_ROOT

## Overview

Hive is a full-stack web application for article management with role-based access control (RBAC). The application provides a RESTful API backend built with Flask and MongoDB, and a React frontend with Redux for state management.

## Implemented Features

### Article Management
- **Article Listing**: Paginated list of articles with title, author, date, and preview
- **Article Viewing**: Full article detail view with all content and metadata
- **Article Creation**: Create new articles (admin/moderator only)
- **Article Editing**: Edit existing articles (admin/moderator or article author)
- **Article Deletion**: Delete articles (admin/moderator or article author)
- **Article Search**: Search articles by title with real-time results

### User Management
- **User Registration**: Public registration endpoint
- **User Authentication**: JWT-based authentication with refresh tokens
- **User Profile**: View user profile information (username, email, role)
- **Admin User Management**: Admin-only interface for managing users (create, update, delete, list)

### Security & Authorization
- **Role-Based Access Control (RBAC)**: Admin, Moderator, and Regular user roles
- **JWT Authentication**: Secure token-based authentication with HTTP-only cookies
- **Security Headers**: Content-Security-Policy, X-Frame-Options, X-Content-Type-Options
- **Environment-Based Configuration**: Required secrets via environment variables

### Testing
- **Backend Tests**: Comprehensive test suite for articles and users (unittest)
- **Frontend Tests**: Component and integration tests (Jest + React Testing Library)
- **Test Coverage**: Coverage reporting available for both backend and frontend

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker and Docker Compose (for containerized setup)
- MongoDB (if running locally without Docker)

### Environment Variables

**IMPORTANT:** This application requires environment variables to be set. Never commit your `.env` file to version control.

1. Create `backend/.env` file with the following **required** variables:
   ```bash
   SECRET_KEY=your_secret_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   ```

2. **Optional variables** (have defaults):
   ```bash
   MONGO_URI=mongodb://admin:your_mongo_password@localhost:27027/  # For local dev (replace with actual password)
   MONGO_DB_NAME=hive_db
   FLASK_ENV=development
   CORS_ORIGINS=http://localhost:3000  # Comma-separated list, REQUIRED in production
   JWT_ACCESS_TOKEN_EXPIRES=900
   JWT_REFRESH_TOKEN_EXPIRES=604800
   RATELIMIT_DEFAULT=100 per minute  # Global rate limit
   RATELIMIT_AUTH=5 per minute  # Rate limit for auth endpoints
   RATELIMIT_WRITE=20 per minute  # Rate limit for write endpoints
   RATELIMIT_STORAGE_URL=memory://  # Rate limit storage (use Redis URL for production)
   TESTING=false
   ```

**Note:** When using Docker Compose, `MONGO_URI` is automatically set by `docker-compose.yml` using environment variables. You must set the following environment variables for Docker Compose:
- `MONGO_ROOT_USERNAME` (defaults to "admin" if not set)
- `MONGO_ROOT_PASSWORD` (required - no default)
- `MONGO_DB_NAME` (defaults to "hive_db" if not set)

Create a `.env` file in the project root with these variables, or export them in your shell before running `docker-compose up`.

**Security Warning:**
- Never commit `.env` files containing real secrets
- Use strong, randomly generated secrets in production
- Rotate secrets regularly
- The application will fail to start if `SECRET_KEY` or `JWT_SECRET_KEY` are not set

### Docker Compose Setup

1. Create a `.env` file in the project root by copying `env.docker.example`:
   ```bash
   cp env.docker.example .env
   ```
   Then edit `.env` and set your MongoDB credentials:
   ```bash
   MONGO_ROOT_USERNAME=admin
   MONGO_ROOT_PASSWORD=your_secure_password_here
   MONGO_DB_NAME=hive_db
   ```

2. Create `backend/.env` file with required Flask variables (see Environment Variables section above).
   You can use `backend/env.example` as a template:
   ```bash
   cp backend/env.example backend/.env
   ```
   Then edit `backend/.env` and set your `SECRET_KEY` and `JWT_SECRET_KEY`.

3. Start all services:
   ```bash
   docker-compose up
   ```

   Or run in detached mode:
   ```bash
   docker-compose up -d
   ```

4. The application will be available at:
   - Backend API: http://localhost:5000
   - Frontend: http://localhost:3000
   - MongoDB: localhost:27027

5. To stop services:
   ```bash
   docker-compose down
   ```

   To stop and remove volumes (clears database):
   ```bash
   docker-compose down -v
   ```

### Local Development Setup

#### Backend
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure `.env` file exists with required variables (see Environment Variables section)

5. Run the application:
   ```bash
   python app.py
   ```

#### Frontend
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   ```

### Security Features

**Security Headers:**
The application includes security headers on all API responses:
- `Content-Security-Policy` - Restricts resource loading
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - Prevents MIME type sniffing

These headers are automatically applied to all routes via Flask's `@app.after_request` decorator.

**CORS Configuration:**
- CORS is configured via the `CORS_ORIGINS` environment variable (comma-separated list)
- Defaults to `http://localhost:3000` in development
- **Required** in production - must be explicitly set
- Wildcard origins (`*`) are not allowed for security

**Rate Limiting:**
- Global rate limit: 100 requests/minute per IP (configurable via `RATELIMIT_DEFAULT`)
- Authentication endpoints (`/api/login`, `/api/register`): 5 requests/minute (configurable via `RATELIMIT_AUTH`)
- Write endpoints (POST, PUT, DELETE): 20 requests/minute (configurable via `RATELIMIT_WRITE`)
- Rate limits are configurable via environment variables

**Input Validation:**
- All API endpoints use Pydantic schemas for request validation
- Validation errors return HTTP 422 with detailed error messages
- Validates data types, required fields, length constraints, and format (e.g., email)

## Testing

### Backend Tests

Run backend tests with coverage:

```bash
cd backend
coverage run --source=. -m unittest discover -s __tests__ --failfast
coverage report -m
```

### Frontend Tests

Run frontend tests:

```bash
cd frontend
npm test
```

Run frontend tests with coverage:

```bash
cd frontend
npm run test:coverage
```

## Planned Features

The following features are planned but not yet implemented:
- Profile editing (requires backend endpoints)
- Article categories/filtering
- Rich text editor for article content
- Image upload for articles
- Infinite scroll pagination (currently page-based)