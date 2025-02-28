# UseCase_CreateArticle.md

**Title**: Create a New Article  
**Scope**: Creating a new article via the API  
**Primary Actor**: Moderator or Admin  
**Preconditions**:
1. The user is authenticated.
2. The user’s role is either **moderator** or **admin**.
3. The system is online and connected to the database.

**Main Flow**:
1. The authenticated moderator or admin sends a `POST` request to `/api/articles` with valid fields: `title` and `content`.
2. The system validates the input and checks that the required fields are present.
3. The system creates a new article document in the database that includes:
   - The provided title and content.
   - Metadata such as the author (username), created_at, and updated_at timestamps.
4. The system returns a `201` status code with a JSON response containing:
   - A success message (e.g., `"Article created successfully"`).
   - The `article_id` of the newly created article.

**Alternate Flows**:
- **Missing Fields**:  
  If required fields (title or content) are missing, the system returns a `400` error with a message such as `"Missing title or content"`.
- **Unauthorized User**:  
  If a user with a role other than moderator or admin (e.g., a regular user) attempts to create an article, the system returns a `403 Forbidden` error.
- **Forced Failure**:  
  For testing or specific failure scenarios (e.g., title is "fail"), the system returns an error message indicating that article creation failed.

**Postconditions**:
- A new article record is inserted into the database if the operation is successful.
- The system returns appropriate error responses for invalid input or unauthorized access.
