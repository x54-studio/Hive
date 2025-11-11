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
   MONGO_URI=mongodb://admin:hivepass123@localhost:27027/  # For local dev
   MONGO_DB_NAME=hive_db
   FLASK_ENV=development
   JWT_ACCESS_TOKEN_EXPIRES=900
   JWT_REFRESH_TOKEN_EXPIRES=604800
   TESTING=false
   ```

**Note:** When using Docker Compose, `MONGO_URI` is automatically set by `docker-compose.yml`, so you don't need it in `backend/.env` for Docker. Only include `MONGO_URI` if running Flask locally without Docker.

**Security Warning:**
- Never commit `.env` files containing real secrets
- Use strong, randomly generated secrets in production
- Rotate secrets regularly
- The application will fail to start if `SECRET_KEY` or `JWT_SECRET_KEY` are not set

### Docker Compose Setup

1. Create `backend/.env` file with required variables (see Environment Variables section above).

2. Start all services:
   ```bash
   docker-compose up
   ```

   Or run in detached mode:
   ```bash
   docker-compose up -d
   ```

3. The application will be available at:
   - Backend API: http://localhost:5000
   - Frontend: http://localhost:3000
   - MongoDB: localhost:27027

4. To stop services:
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

### Security Headers

The application includes security headers on all API responses:
- `Content-Security-Policy` - Restricts resource loading
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - Prevents MIME type sniffing

These headers are automatically applied to all routes via Flask's `@app.after_request` decorator.

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