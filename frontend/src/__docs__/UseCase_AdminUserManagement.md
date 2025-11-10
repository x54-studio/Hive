
# UseCase_AdminUserManagement.md

## 1. Title & Scope
**Title:** Admin User Management (with Infinite Scroll & Manual “Load More”)  
**Scope:** This use case enables an Admin to manage user accounts, including listing them in a paginated manner, automatically loading more users upon scrolling to the bottom, and optionally using a “Load More” button if needed. It also covers creating, updating, and deleting users, and it provides logic for re-initializing the user list after user creation.

## 2. Actors
- **Primary Actor:** Admin – A user with administrative privileges.
- **System:**  
  - **Frontend**: An Admin UI that lists and manages users.  
  - **Backend**: API endpoints (e.g., `/users` for fetching users with pagination, `/users/:id` for update/delete).

## 3. Preconditions
1. The Admin has successfully logged in with enough privileges to manage users.
2. The API endpoints (`GET /users`, `POST /users`, `PUT /users/:id`, `DELETE /users/:id`) are available and return data in a recognized format (either `response.data.data` or an array in `response.data`).
3. The environment variables and configurations (e.g., `axiosInstance` base URL) are properly set so the frontend calls the correct server.

## 4. Main Flow

### 4.1 Viewing the User List
1. **Page Load**:  
   - The Admin navigates to the Admin User Management page.  
   - The system fetches the first page of users (e.g., `page=1`, `size=5`) from the API.  
   - The system renders the user rows in a scrollable container (max height ~400px).
2. **Infinite Scroll Setup**:  
   - The system attaches an IntersectionObserver to the last real user row in the table.
   - When this row is in view and there are more pages (`hasMore === true`), the system automatically fetches the next page (e.g. `page=2`).
3. **Scroll Trigger**:  
   - As the Admin scrolls to the bottom of the container and the last row becomes visible, the IntersectionObserver callback fetches the next page, appending new users to the list.  
   - This continues until the backend returns fewer users than `pageSize`, causing `hasMore` to become `false` and preventing further pages from loading.

### 4.2 Manual “Load More” Fallback
1. **Load More Button**:  
   - At any time, a “Load More” button is displayed beneath the user table.
   - If auto-scrolling fails (e.g., IntersectionObserver not triggered), the Admin can click “Load More” to manually load the next page.
2. **Fetching Additional Pages**:  
   - Upon clicking “Load More,” if `hasMore && !loading`, the frontend increments the page counter and fetches the next page, appending the new users to the list.

### 4.3 Creating a New User
1. **Click “Create New User”**:  
   - The Admin clicks the “Create New User” button, revealing a form for username, email, role, and password.
2. **Submit Form**:  
   - The Admin fills in the required fields and submits.  
   - The system sends a `POST /users` request to create the new user.
3. **Re-initialize the List**:  
   - After a successful creation, the system optionally clears the existing list (`setUsers([])`) and resets `page` to 1, then re-fetches the first page.  
   - This ensures that the newly created user is visible (often sorted into the first page by the backend) and that the infinite scrolling logic restarts cleanly.

### 4.4 Editing a User
1. **Click “Edit”**:  
   - Next to a user, the Admin clicks “Edit,” revealing a form pre-filled with the user’s data (username, email, role).
2. **Submit Form**:  
   - The Admin updates fields and submits.  
   - The system sends a `PUT /users/:id` request to update the user.
3. **UI Update**:  
   - The system replaces that user in the existing local list.  
   - The Admin sees the updated data immediately.

### 4.5 Deleting a User
1. **Click “Delete”**:  
   - Next to a user, the Admin clicks “Delete.”
2. **Confirmation**:  
   - A confirmation prompt appears to prevent accidental deletions.
3. **Request**:  
   - The system sends a `DELETE /users/:id` request to remove the user.
4. **UI Update**:  
   - The user is removed from the local list, and a success message is shown.

## 5. Alternate Flows
- **Empty List**:  
  - If the backend returns no users, the table is empty and `hasMore` is set to `false`. The observer does not trigger further pages, and the “Load More” button is disabled or hidden.
- **Backend Errors**:  
  - If a request fails (e.g. 500 server error), the system sets `error` and shows “Failed to load users” or “Failed to create user.” The Admin can retry manually.
- **Partial or Unexpected Data**:  
  - The system uses a defensive parse of `response.data?.data` or `response.data` to handle different JSON shapes. If neither yields an array, the system assumes no users were returned.

## 6. Postconditions
- **Success**:  
  - The Admin can see and manage all users, with new pages auto-loading when scrolling or by clicking “Load More,” up until no more data (`hasMore === false`). The Admin can create, edit, and delete users successfully.
- **Failure**:  
  - If requests fail or the data is in an unexpected format, an error is displayed. The Admin can attempt to refresh or fix the issue externally.

## 7. Additional Considerations
- **Performance**:  
  - IntersectionObserver is more efficient than continuously checking scroll positions. The “Load More” fallback ensures that data can still be fetched if the observer is not triggered.
- **Re-initialization on Create**:  
  - After creating a user, the list is cleared and page 1 is fetched again so the newly created user is visible. Alternatively, we could just append the new user to the existing list.
- **UI/UX**:  
  - The table is capped at 400px for vertical scrolling, with a “Loading...” indicator when fetching. A “No more users to load” message appears if `hasMore === false`.
- **Testing**:  
  - In tests, you can override IntersectionObserver to trigger immediately, or rely on a “Load More” button for controlled pagination tests.
