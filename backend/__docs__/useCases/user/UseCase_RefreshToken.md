### 3.3 UseCase_RefreshToken.md

- **Title**: Refresh Access Token
- **Scope**: Generating a new access token when the current one is expired/invalid
- **Primary Actor**: Authenticated user (with valid refresh token in cookie)
- **Preconditions**:
  1. User has previously logged in and received a refresh token in an HTTP-only cookie.
  2. Refresh token is still valid (not expired, not revoked).
- **Main Flow**:
  1. User sends `POST /api/refresh` (the request automatically includes the refresh token cookie).
  2. System decodes and verifies refresh token, checks stored hash in DB.
  3. System issues a new access token and sets it in HTTP-only cookie (and optionally issues a new refresh token).
  4. Returns success response with `{"access_token": "...", "refresh_token": "...", "message": "Token refreshed successfully"}` (if `TESTING` mode) or just a success message if in production.
- **Alternate Flows**:
  - **Invalid/expired token**: Return `401` with `{"error": "Invalid or expired refresh token"}`.
  - **No refresh token in cookie**: Return `401` with `{"error": "Missing refresh token"}`.
- **Postconditions**:
  - Access token is renewed so the user can continue making authenticated requests.
