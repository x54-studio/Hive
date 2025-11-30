# Hive: Secure RBAC & Article Management System

## Overview

**Hive** is a technical demonstration of a secure, production-grade web application architecture. While functional as an article management platform, its primary purpose is to showcase advanced security implementations, Role-Based Access Control (RBAC), and scalable full-stack patterns.

Built with **Flask (Python)** and **React (Redux Toolkit)**, Hive implements industry best practices for authentication, session management, and secure data handling.

## 🔐 Security & Architecture Highlights

This project prioritizes security and architectural rigor over feature quantity.

### Authentication & Authorization
- **Dual-Token System**: Short-lived JWT access tokens (15m) + long-lived refresh tokens (7 days).
- **HttpOnly Cookies**: Tokens are stored in `HttpOnly`, `Secure`, `SameSite` cookies to prevent XSS.
- **Role-Based Access Control (RBAC)**: Granular permissions for `Admin`, `Moderator`, and `Regular` users.
- **Automatic Token Refresh**: Silent token rotation via Axios interceptors and proactive frontend logic.
- **Session Management**: Multi-tab coordination, page visibility handling, and secure logout.

### Backend Security (Flask)
- **Input Validation**: Strict Pydantic schemas for all request payloads.
- **Security Headers**: Automated `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`.
- **Rate Limiting**: Configurable rate limits per endpoint (e.g., strict limits on auth routes).
- **Error Handling**: Centralized error handlers with consistent, safe response formats (no leaking internals).
- **Clean Architecture**: Strict separation of concerns (Routes → Services → Repositories).

### Frontend Architecture (React)
- **Redux Toolkit**: Centralized, predictable state management for auth and user sessions.
- **Protected Routes**: High-order components for role-based route protection.
- **Security-First UI**: UI elements (buttons, links) adapt visibility based on user permissions.
- **Robust Error Boundaries**: Graceful degradation and error logging.

---

## Implemented Features

### 🛡️ Security & Admin
- **User Registration & Auth**: Secure flows with validation and duplicate checks.
- **Admin Dashboard**: User management (List, Promote/Demote, Delete) protected by RBAC.
- **Profile Management**: Secure viewing of user details and role status.

### 📝 Article Domain (Demo Context)
- **CRUD Operations**: Create, Read, Update, Delete articles (with permission checks).
- **Real-time Search**: Regex-based search for article titles.
- **Pagination**: Backend-enforced pagination for performance.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose (recommended)

### Quick Start (Docker)

1. **Configure Environment**:
   ```bash
   cp env.docker.example .env
   cp backend/env.example backend/.env
   ```
   *Edit `.env` files to set secure secrets (SECRET_KEY, MONGO passwords).*

2. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Swagger Docs: http://localhost:5000/api/docs

### Local Development

See `backend/README.md` and `frontend/README.md` for detailed local setup instructions.

---

## Testing

Hive maintains comprehensive test suites for both backend and frontend to ensure reliability and regression prevention.

### Backend Tests (Unittest)
```bash
cd backend
# Run all tests with coverage
coverage run --source=. -m unittest discover -s __tests__ --failfast
coverage report -m
```

### Frontend Tests (Jest + RTL)
```bash
cd frontend
npm test
# or run with coverage
npm run test:coverage
```

---

## Technology Stack

| Component | Tech Stack |
|-----------|------------|
| **Backend** | Python 3.11, Flask, PyMongo, Pydantic, JWT-Extended, Bcrypt |
| **Frontend** | React 19, Redux Toolkit, React Router v7, Axios, Tailwind CSS |
| **Database** | MongoDB (NoSQL) |
| **Infra** | Docker, Docker Compose |
| **Testing** | Unittest, Jest, React Testing Library, Cypress |

---

## License

MIT License
