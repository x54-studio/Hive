# UseCase_GetArticle.md

**Title**: Retrieve a Single Article  
**Scope**: Accessing the details of a specific article via the API  
**Primary Actor**: Any user (public or authenticated)  
**Preconditions**:
1. The article exists in the system.
2. The system is online and the database is accessible.

**Main Flow**:
1. A user sends a GET request to `/api/articles/<article_id>`.
2. The system retrieves the article from the database.
3. The system returns a 200 status code with a JSON response containing:
   - `article_id`
   - `title`
   - `content`
   - `author`
   - `created_at`
   - `updated_at`
4. The response format conforms to the API specification.

**Alternate Flows**:
- **Article Not Found**:  
  If no article with the given ID exists, the system returns a 404 error with a message such as `"Article not found"`.
- **Invalid Article ID**:  
  If the provided article ID is not in the correct format, the system returns a 400 error with a descriptive message.

**Postconditions**:
- On success, the client receives all relevant details of the requested article.
