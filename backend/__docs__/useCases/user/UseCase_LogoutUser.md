### 3.4 UseCase_LogoutUser.md

- **Title**: Logout User
- **Scope**: Removing user’s token(s) from browser cookies and invalidating them
- **Primary Actor**: Authenticated user
- **Preconditions**:
  1. User is currently logged in (has valid cookies).
- **Main Flow**:
  1. User sends `POST /api/logout`.
  2. System sets cookies to expire (deleting `access_token` and `refresh_token` cookies).
  3. Optionally, system removes stored refresh token hash in DB or marks it as invalid.
  4. Returns `{"message": "Logged out successfully"}`.
- **Alternate Flows**:
  - If user has no valid session, it can still return success (“effectively logged out”).
- **Postconditions**:
  - User’s session is terminated, and they must log in again to obtain fresh tokens.
