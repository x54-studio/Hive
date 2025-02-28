# UseCase_DeleteArticle.md

**Title**: Delete an Article  
**Scope**: Remove an article from the system via the API  
**Primary Actor**: Authenticated user (typically the article's author, a moderator, or an admin)  
**Preconditions**:
1. The article exists in the database.
2. The user is authenticated and is authorized to delete the article (e.g. the user is the author, a moderator, or an admin).

**Main Flow**:
1. The authenticated user sends a DELETE request to `/api/articles/<article_id>`.
2. The system verifies the user's authorization to delete the article.
3. The system deletes the article from the database.
4. The system returns a 200 status code with a JSON response containing a success message (e.g., `"Article deleted successfully"`).

**Alternate Flows**:
- **Article Not Found**:  
  If the article does not exist, the system returns a 404 error with a message such as `"Article not found"`.
- **Unauthorized Deletion**:  
  If the user is not authorized to delete the article, the system returns a 403 error with an appropriate message.

**Postconditions**:
- On success, the article is removed from the database.
