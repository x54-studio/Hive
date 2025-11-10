# UseCase_ListUsers.md

**Title:** List Users with Pagination  
**Scope:** Retrieve a paginated list of registered users from the system via the backend API. This use case covers the functionality needed for an admin (or authorized actor) to view user records in manageable chunks.  

**Primary Actor:**  
- **Admin:** An administrator who needs to review or manage users.
- **Authorized User:** Optionally, other roles may be allowed if permissions permit.

**Preconditions:**  
1. The actor is authenticated with a valid session (e.g., has a valid JWT token stored in cookies).  
2. The actor is authorized to access user data (typically admin privileges).  
3. The backend API endpoint `/api/users` (or similar) is available.

**Main Flow:**  
1. The actor sends a GET request to `/api/users` with optional query parameters:
   - `page`: the page number to retrieve (default: 1).
   - `limit`: the number of users per page (default: a system-defined value, e.g., 10 or 20).
2. The system validates the pagination parameters.
3. The system retrieves the corresponding subset of user records from the database.
4. The system returns a JSON response containing:
   - An array of user objects (each containing at least `user_id`, `username`, `email`, `role`, etc.).
   - Pagination metadata (e.g., current page, total pages, total count).

**Alternate Flows:**  
- **Invalid Pagination Parameters:**  
  If the provided `page` or `limit` parameters are invalid (non-numeric, negative, etc.), the system returns a `400 Bad Request` with an appropriate error message.

**Postconditions:**  
- On success, the actor receives a paginated list of user records.
- On failure, no user data is returned, and the actor receives an error message indicating the problem.

**Additional Considerations:**  
- **Security:**  
  Only authorized actors (typically admins) should be allowed to access the user list.
- **Performance:**  
  The system should efficiently handle large numbers of users by using appropriate database indexes and limiting the size of returned data.
- **User Experience:**  
  The frontend can use the pagination metadata to render navigation controls for the user list.
- **Testing:**  
  Unit and integration tests should validate that pagination works correctly, including edge cases (e.g., page number out-of-range).
