# UseCase_UpdateUser.md

**Title:** Update User  
**Scope:** Modify a user's account information (such as email, role, or personal details) via the backend API. This use case covers both self-update (by the user) and admin updates (by an administrator) for user data.  

**Primary Actor:**  
- **Admin:** An administrator with privileges to update any user's data.  
- **User:** A regular user updating their own account information (if self-update is supported).

**Preconditions:**  
1. The actor (admin or user) is authenticated with a valid session.  
2. For admin updates, the RBAC system confirms that the user has Admin privileges.  
3. The system's backend is accessible and the user management API endpoints are available.  
4. The user to be updated exists in the database, identified by a unique user ID.

**Main Flow:**  
1. The actor sends a `PUT /api/users/:id` request with the updated user data (e.g., email, role, or other personal information).  
2. The system validates the input data and confirms that at least one updatable field is provided.  
3. The system verifies that the actor is authorized to update the target user (either the user updating their own data or an admin updating any user).  
4. The system updates the user document in the database, including setting a new `updated_at` timestamp.  
5. The system returns a `200 OK` response with a JSON payload containing a success message (e.g., `{"message": "User updated successfully"}`).

**Alternate Flows:**  
- **No Update Data Provided:**  
  If the request body does not contain any fields to update, the system returns a `400 Bad Request` error with a message like `"No update data provided"`.
  
- **User Not Found:**  
  If the target user does not exist, the system returns a `404 Not Found` error with a message such as `"User not found"`.
  
- **Unauthorized Update Attempt:**  
  If the actor does not have permission to update the target user, the system returns a `403 Forbidden` error with a message like `"User not authorized to update users"`.

**Postconditions:**  
- On success, the user's account is updated in the database and the actor receives confirmation of the update.  
- On failure, no changes are persisted, and the system provides an error message to the actor for corrective action.

**Additional Considerations:**  
- **Validation:**  
  Input data must be validated to ensure it meets the required formats (e.g., proper email format, acceptable role values).  
- **Audit Logging:**  
  All update operations should be logged for auditing and compliance purposes.  
- **Security:**  
  Sensitive data, such as passwords, should be hashed before storage. Role updates should be carefully controlled to prevent privilege escalation.

