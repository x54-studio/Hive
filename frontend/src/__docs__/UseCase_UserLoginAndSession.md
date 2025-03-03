# UseCase_UserLoginAndSession.md

## 1. Title & Scope
**Title:** User Login & Session Management  
**Scope:** Enable registered users to log into the Hive system using either their username or email, and maintain an active, persistent session across page navigations and browser refreshes through proper token management and backend validation.

## 2. Actors
- **Primary Actor:** Registered User – A user with an existing account who logs into the system.
- **System:** Hive Frontend Application.
- **Authentication Service:** Backend endpoints responsible for validating credentials and managing JWT tokens (access and refresh).

## 3. Preconditions
1. The user has an existing account in the Hive system.
2. The Hive frontend is accessible and the login page (e.g., `/login`) is available.
3. The backend API (e.g., at http://localhost:5000) is running and accessible for authentication.
4. Required environment variables (e.g., `BACKEND_API_URL`) are properly configured.

## 4. Main Flow
1. **Access Login Page:**  
   The user navigates to the login page (e.g., `/login`).

2. **Enter Credentials:**  
   The user enters their credentials in the login form:
   - **Username or Email** (using a unified input field labeled "Username or Email")
   - **Password**
   - The login form may provide a "Show/Hide Password" feature to improve usability.

3. **Submit Login Form:**  
   The user clicks the "Login" button.  
   The frontend dispatches an action (e.g., `login({ username_or_email, password })`) to send credentials to the backend API.

4. **Backend Authentication:**  
   The backend validates the credentials:
   - **On Success:** Returns a response that sets HTTP-only cookies containing valid JWT tokens and/or a user profile.
   - **On Failure:** Returns an error (e.g., "Invalid username or password").

5. **Update Frontend State:**  
   Upon successful login, the frontend updates its global state (e.g., in Redux) with the user’s profile information.  
   The application then navigates to a protected area (such as the user’s profile page).

6. **Session Persistence:**  
   The frontend periodically (or via 401 handling) uses the refresh token (via an endpoint like `/api/refresh`) to maintain a valid session.  
   This ensures that the user remains logged in even if the access token expires.

## 5. Alternate Flows
- **Invalid Credentials:**  
  If the credentials are invalid, the backend returns an error. The frontend displays an error message (e.g., "Invalid username or password") and remains on the login page.
  
- **Network or Server Error:**  
  If the request fails due to network or server issues, the frontend shows a generic error message (e.g., "Login failed due to a system error. Please try again later.").
  
- **Session Expiration:**  
  If the access token expires during an active session, the frontend automatically triggers a refresh token flow. If refresh fails, the user is logged out and redirected to the login page.

## 6. Postconditions
- **Success:**  
  The user is successfully authenticated; their user data is stored in the global state and the session is maintained using valid JWT tokens. The user is redirected to a protected route.
- **Failure:**  
  The user remains unauthenticated, and clear error messages are provided to prompt corrective action.

## 7. Additional Considerations
- **Security:**  
  Ensure that passwords are transmitted securely (using HTTPS) and that sensitive tokens are stored as HTTP-only cookies to mitigate XSS risks.
  
- **User Experience:**  
  Provide clear, immediate feedback (e.g., toast notifications) for both successful logins and error scenarios. Ensure that the login form is accessible and that features like "Show/Hide Password" are available.
  
- **Testing:**  
  Write unit tests for the login thunk and component using Jest and React Testing Library. Implement end-to-end tests with Cypress to verify the complete login flow and session persistence.
  
- **Scalability:**  
  Consider integrating automatic token refresh logic and proper error handling to manage session expiration seamlessly.
