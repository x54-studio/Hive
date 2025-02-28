# UseCase_ListArticles.md

**Title**: List Articles with Pagination  
**Scope**: Retrieve a paginated list of articles from the API  
**Primary Actor**: Any user (public or authenticated)  
**Preconditions**:
1. There are at least 3 articles stored in the database.
2. The system is online and the database is accessible.

**Main Flow**:
1. The client sends a GET request to `/api/articles` with optional query parameters:
   - `page`: the page number (default is 1)
   - `limit`: the number of articles per page (default is 2)
2. The system retrieves articles from the database in a defined order (for example, sorted by creation date descending).
3. The system applies pagination (using skip and limit) to return the correct subset.
4. The system returns a 200 status code with a JSON array of articles. Each article includes:
   - `article_id`
   - `title`
   - `content`
   - `author`
   - `created_at`
   - `updated_at`

**Alternate Flows**:
- If query parameters are invalid (for example, non‑numeric values), the system returns a 400 error with a message indicating invalid pagination parameters.
- If no articles exist, the system returns an empty array with a 200 status.

**Postconditions**:
- The client receives the requested page of articles according to the pagination parameters.
