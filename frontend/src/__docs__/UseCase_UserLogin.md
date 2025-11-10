# UseCase_UserLogin.md

## 1. Title & Scope
**Title:** User Login  
**Scope:** Allow registered users to authenticate with the Hive system using a unified login form. Upon successful authentication, the system establishes a secure session by storing tokens in HTTP‑only cookies and updating the global application state. The login process supports error handling and provides user feedback.

## 2. Actors
- **Primary Actor:** Registered User – A user who has previously created an account and now wants to log in.
- **System:** Hive Frontend Application.
- **Authentication Service:** Backend endpoints responsible for validating credentials and issuing tokens (access and refresh).

## 3. Preconditions
1. The user has a registered account in the Hive system.
2. The login page (e.g., `/login`) is accessible to the user.
3. The backend API (e.g., at http://localhost:5000) is up and running.
4. Required environment variables (e.g., `BACKEND_API_URL`) are correctly configured.

## 4. Main Flow
1. **Access Login Page:**  
   The user navigates to the login page (e.g., `/login`) using a web browser.

2. **Enter Credentials:**  
   The user inputs their username or email and password.  
   - The login form includes features such as a "Show/Hide Password" toggle to enhance usability.

3. **Submit Login Form:**  
   The user clicks the "Login" button.  
   - The frontend dispatches a login action (e.g., via Redux thunk) that sends the credentials to the backend API.

4. **Backend Authentication:**  
   The backend validates the credentials:  
   - **On Success:** Returns a response that sets HTTP‑only cookies with the access and refresh tokens, and may include additional user profile data.  
   - **On Failure:** Returns an error message (e.g., "Invalid username or password").

5. **Update Frontend State & Navigation:**  
   Upon a successful response, the frontend updates the centralized state (e.g., via Redux) with the user's profile information.  
   - The user is then redirected to a protected route (e.g., their profile page).

## 5. Alternate Flows
- **Invalid Credentials:**  
  If the backend returns an error due to invalid credentials, the frontend displays a clear error message (e.g., "Invalid username or password") and remains on the login page.
  
- **Network or Server Error:**  
  If a network issue or server error occurs during the login attempt, the frontend shows a generic error message (e.g., "Login failed due to a system error. Please try again later").

## 6. Postconditions
- **Success:**  
  The user is successfully authenticated; secure tokens are stored in HTTP‑only cookies, the global application state is updated with user details, and the user is redirected to a protected area.
  
- **Failure:**  
  No session is established; the user remains on the login page and is informed of the error, prompting corrective action.

## 7. Additional Considerations
- **Security:**  
  - All communication between the client and server must occur over HTTPS.  
  - Access and refresh tokens are stored in HTTP‑only cookies to mitigate XSS risks.  
  - The login endpoint should implement proper rate limiting and monitoring to prevent brute-force attacks.

- **User Experience:**  
  - The login form should be simple, accessible, and responsive.  
  - Immediate feedback is provided via toast notifications or inline messages upon success or failure.
  
- **Testing:**  
  - Unit tests (using Jest and React Testing Library) should cover the login action and state updates.  
  - End-to-end tests (using Cypress) should verify the complete login flow, including successful redirection and error handling.
  
- **Scalability:**  
  - The system should be designed to integrate with centralized session management and automatic token refresh mechanisms to maintain continuous user sessions.
