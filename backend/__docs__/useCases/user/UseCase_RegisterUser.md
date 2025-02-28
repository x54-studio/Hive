### 3.1 UseCase_RegisterUser.md

- **Title**: Register a New User
- **Scope**: Creating a user account in the system
- **Primary Actor**: Unauthenticated visitor
- **Preconditions**:
  1. Visitor must not already have an account with the same email or username.
  2. The system is online and accessible.
- **Main Flow**:
  1. Visitor sends `POST /api/register` with `username`, `email`, `password`.
  2. System validates uniqueness of email/username, hashes password.
  3. System inserts a new user record with role = `regular`.
  4. System returns success response (`201`) with JSON `{"message": "User registered successfully!", "user_id": "<id>"}`.
- **Alternate Flows**:
  - **Missing fields**: Return `{"error": "Missing required fields"}`, HTTP 400.
  - **Duplicate email or username**: Return `{"error": "User already exists"}`, HTTP 400 or 409.
- **Postconditions**:
  - A new user record is persisted in MongoDB with a hashed password.
  - The user is now able to log in with the provided credentials.
