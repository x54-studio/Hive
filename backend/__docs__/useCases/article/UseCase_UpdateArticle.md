# UseCase_UpdateArticle.md

**Title**: Update an Existing Article  
**Scope**: Modifying the title and/or content of an article via the API  
**Primary Actor**: Authenticated user (typically the article's author, a moderator, or an admin)  
**Preconditions**:
1. The article exists in the system.
2. The user is authenticated and is authorized to update the article (e.g. they are the original author, a moderator, or an admin).

**Main Flow**:
1. The authenticated user sends a PUT request to `/api/articles/<article_id>` with at least one updatable field (e.g. title and/or content).
2. The system validates that at least one field to update is provided.
3. The system updates the article record in the database, setting a new `updated_at` timestamp.
4. The system returns a 200 status code with a JSON response indicating success, e.g.:
   - `{"message": "Article updated successfully"}`

**Alternate Flows**:
- **No Update Fields Provided**:  
  If the request does not include any fields to update, the system returns a 400 error with a message such as `"No update fields provided"`.
- **Article Not Found**:  
  If no article with the given ID exists, the system returns a 404 error with a message like `"Article not found"`.
- **Unauthorized Update**:  
  If the user is not authorized to update the article, the system returns a 403 error with a message such as `"User not authorized to update this article"`.

**Postconditions**:
- If successful, the article record in the database reflects the updated values and a refreshed `updated_at` timestamp.
