### 3.5 UseCase_DeleteUser.md (Optional)

- **Title**: Delete User
- **Scope**: Removing a user account from the system (self-delete or admin delete)
- **Primary Actor**: Possibly an Admin user or the user themself
- **Preconditions**:
  1. User or admin is authenticated.
  2. If a self-delete flow, the user must confirm or pass additional validation (like re-entering password).
- **Main Flow**:
  1. Actor sends `DELETE /api/users/:id`.
  2. System verifies user has permission (admin can delete any user, or user can delete themselves).
  3. System deletes user doc from DB.
  4. Returns `{"message": "User deleted successfully"}`.
- **Alternate Flows**:
  - **User not found**: Return `404`.
  - **No permission**: Return `403`.
- **Postconditions**:
  - The user’s account is permanently removed from the database.
