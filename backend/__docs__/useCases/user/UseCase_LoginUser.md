### 3.2 UseCase_LoginUser.md

- **Title**: Login User
- **Scope**: Authenticating an existing user
- **Primary Actor**: Unauthenticated visitor (who already has credentials)
- **Preconditions**:
  1. The user must have a valid account.
  2. The user’s password is properly hashed in the DB.
- **Main Flow**:
  1. User sends `POST /api/login` with `username_or_email`, `password`.
  2. System retrieves user by username **or** email.
  3. System verifies password via `bcrypt.checkpw`.
  4. If valid, system generates JWT access + refresh tokens, stores them in HTTP-only cookies, and returns success JSON.
- **Alternate Flows**:
  - **User not found**: Return `{"error": "User not found"}`, HTTP 401.
  - **Invalid password**: Return `{"error": "Invalid credentials"}`, HTTP 401.
  - **Missing fields**: Return `{"error": "Missing email or password"}`, HTTP 400.
- **Postconditions**:
  - User is “logged in,” and subsequent requests can use the issued access token (in the HTTP-only cookie).
