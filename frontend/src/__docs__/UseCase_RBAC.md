
# UseCase_RBAC.md

## Role-Based Access Control (RBAC) / Authorization

### 1. Overview
Role-Based Access Control (RBAC) restricts system access to authorized users based on their assigned roles. This model ensures that users can perform only actions relevant to their responsibilities, improving security, administration, and compliance.

### 2. Key Roles and Responsibilities

#### Admin
- **Scope:** Complete system control and management.
- **Primary Responsibilities:**
  - Create, update, and delete user accounts.
  - Assign and modify roles and permissions.
  - Access all application areas, including user management, system configuration, and audit logs.
  - Manage content and data that require elevated privileges.
- **Use Cases:**
  1. **User Management:**  
     - **Description:** Admins view all users, update user information, change roles, or delete accounts.
     - **Flow:**  
       - Navigate to "Admin User Management."
       - Display all registered users.
       - Select a user to edit and update role information.
       - Validate and apply the change.
  2. **Article Management:**  
     - **Description:** Admins can create, update, and delete any article.
     - **Flow:**  
       - Navigate to "Articles" section.
       - Create, edit, or delete articles as needed.
       - The system validates and applies changes.

#### Moderator
- **Scope:** Content and articles management.
- **Primary Responsibilities:**
  - Create, update, or delete articles.
  - Manage article content.
- **Use Cases:**
  1. **Article Management:**  
     - **Description:** A Moderator can create new articles, edit existing ones, and delete articles.
     - **Flow:**  
       - Navigate to the "Articles" section.
       - Create a new article or select an existing one for editing.
       - Submit changes.
       - The system validates the content and updates the article.

#### Regular User
- **Scope:** Standard access to personal data and public resources.
- **Primary Responsibilities:**
  - View and update their own profile.
  - Access general application content.
  - Submit requests or reports relevant to their role.
- **Use Cases:**
  1. **Profile Management:**  
     - **Description:** Users view their profile information (username, email, role).
     - **Flow:**  
       - Navigate to "Profile."
       - View personal details.
       - Note: Profile editing is not yet implemented (requires backend endpoints).
  2. **Content Interaction:**  
     - **Description:** Users can view public articles and search for articles.
     - **Flow:**  
       - Browse articles from the "Articles" page.
       - Search for articles using the search functionality.
       - View article details.
       - Note: Regular users cannot create, edit, or delete articles.

#### Guest
- **Scope:** Limited access for users who are not logged in.
- **Primary Responsibilities:**
  - View public content.
  - Access informational pages (e.g., about, contact).
- **Use Cases:**
  1. **Content Browsing:**  
     - **Description:** Guests view public articles and resources but cannot post or access restricted pages.
     - **Flow:**  
       - Visit the homepage.
       - Display public articles and resources.
       - Redirect to the login page when attempting to access restricted content.

### 3. Implementation Considerations

- **Frontend:**
  - Use route guards (e.g., ProtectedRoute components) to enforce role-based access.
  - Conditionally display UI elements based on the current user's role.
  - Store role and permission information in global state management (e.g., Redux).

- **Backend:**
  - Implement middleware to enforce permissions on API endpoints.
  - Embed role and permission claims in tokens (e.g., JWT).
  - Log all role-based access events for audit purposes.

- **Testing:**
  - Unit and integration tests should verify that:
    - Users can only access routes and perform actions according to their roles.
    - Unauthorized access attempts result in proper redirections or error messages.
    - Role changes propagate correctly to both the frontend and backend.

### 4. Future Enhancements

- **Dynamic Role Assignment:**  
  Allow real-time role updates without requiring a new login.
- **Granular Permissions:**  
  Further refine permissions for more fine-tuned access control.
- **Audit Logging:**  
  Maintain detailed logs of role-based actions for compliance and troubleshooting.

## RBAC Demo Component

A demo component (`RBACDemo`) has been implemented to visually verify role-based access control. It renders different UI based on the logged-in user's role:

- **Admin:** Displays "Admin Dashboard"
- **Moderator:** Displays "Moderator Panel"
- **Regular User:** Displays "User Profile"
- **No User:** Prompts "Please log in."
- **Unrecognized Role:** Displays "Unknown Role"

Automated tests for this component are located in the `src/__tests__/rbac` folder.

**Note:** The actual implementation uses "moderator" role, not "editor". The roles are: admin, moderator, and regular (default).
