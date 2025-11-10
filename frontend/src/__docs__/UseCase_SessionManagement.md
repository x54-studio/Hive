# UseCase_SessionManagement.md

## 1. Title & Scope
**Title:** Session Management & Automatic Token Refresh  
**Scope:** Maintain an uninterrupted, secure session for authenticated users by automatically refreshing the access token before it expires. This includes proactive token refresh, multi‑tab coordination to avoid duplicate refresh calls, and proper error handling when the refresh fails.

## 2. Actors
- **Primary Actor:** Authenticated User – A user who has successfully logged into the Hive system.
- **System:**  
  - **Frontend:** Hive Frontend Application that manages session state and token refresh.
  - **Authentication Service:** Backend endpoints responsible for token issuance and validation, including the refresh endpoint.

## 3. Preconditions
1. The user has successfully logged into the system.
2. The backend has issued both an access token (short-lived) and a refresh token (long-lived), delivered via HTTP‑only cookies.
3. The access token contains expiration information (e.g., an `exp` claim) that can be read (typically via a protected endpoint).
4. The application is configured to use secure HTTPS communication.

## 4. Main Flow
1. **Session Initialization:**
   - After successful login, the backend sets the access and refresh tokens in HTTP‑only cookies.
   - The frontend retrieves expiration data from users claims `exp` and updates its session state.

2. **Scheduling Automatic Token Refresh:**
   - The frontend calculates the token’s remaining lifetime using the expiration (`exp`) claim.
   - A refresh timer is scheduled to trigger slightly before the access token expires (for example, 1 second or a configurable buffer before expiration).
   - This logic is encapsulated in a custom hook (e.g., `useTokenRefresh`) that is used by a top‑level SessionManager component.

3. **Proactive Refresh Workflow:**
   - When the timer fires, the frontend dispatches a refresh request via a Redux thunk to the refresh endpoint (`POST /api/refresh`).
   - The backend validates the refresh token (extracted from the HTTP‑only cookie) and, if valid, issues a new access token (and possibly rotates the refresh token). New tokens are set via HTTP‑only cookies.
   - On successful refresh, the frontend updates its session state with the new token information and re‑schedules the refresh timer based on the new expiration.

4. **Fetching Protected Resources:**
   - With the refreshed tokens, the frontend continues to access protected endpoints seamlessly.
   - The new token expiration value is used to schedule the next refresh cycle.

## 5. Alternate Flows
- **Refresh Failure:**  
  - If the refresh request fails (e.g., due to an invalid or expired refresh token), the backend returns an error (e.g., 401 Unauthorized).
  - The frontend clears the session, logs the user out, and redirects to the login page, displaying an appropriate error message.

- **Multi‑Tab Coordination:**  
  - In environments where multiple tabs are open, each tab may schedule its own refresh timer.  
  - To prevent duplicate refresh requests, a shared flag localStorage is used to ensure that only one tab performs the refresh while the others wait for the result.
  - Once the refresh is complete, all tabs update their session state accordingly.

- **401 Fallback:**  
  - Even with proactive refresh, if an API call fails with a 401 error (perhaps due to the browser being inactive or network issues), an HTTP interceptor in the frontend will trigger a one‑time refresh.  
  - If that refresh also fails, the user is logged out and prompted to log in again.

## 6. Postconditions
- **Success:**  
  The user remains continuously authenticated, and the access token is refreshed automatically before expiration. The frontend’s session state is updated, and protected resources are accessible without interruption.

- **Failure:**  
  If token refresh fails, the user is logged out, and the application displays a clear error message prompting the user to re-authenticate.

## 7. Additional Considerations
- **Security:**  
  - Tokens are stored in HTTP‑only cookies to reduce the risk of XSS attacks.
  - All communication between the frontend and backend must occur over HTTPS.
  - The refresh process should validate tokens thoroughly to prevent replay attacks or token misuse.

- **User Experience:**  
  - The token refresh process is transparent to the user.
  - In case of refresh failure, the user is provided with a clear message and seamlessly redirected to the login page.
  
- **Testing:**  
  - Unit and integration tests should ensure the refresh timer is set correctly and triggers the refresh callback at the appropriate time.
  - End‑to‑end tests (using Cypress or similar tools) should verify that, when the token is near expiration, a refresh is initiated and the session is maintained.
  - Multi‑tab coordination logic should be tested to ensure that only one refresh request is sent across tabs.

- **Scalability & Maintainability:**  
  - The refresh logic (including the buffer time before token expiration) should be configurable.
  - The use of a centralized SessionManager component helps maintain a single source of truth for session state and reduces duplication of refresh logic across the application.
