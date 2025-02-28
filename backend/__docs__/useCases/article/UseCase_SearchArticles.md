# UseCase_SearchArticles.md

**Title**: Search and Filter Articles  
**Scope**: Retrieve articles from the database that match a given search query or filter criteria via the API  
**Primary Actor**: Any user (public or authenticated)  
**Preconditions**:
1. There are at least a few articles stored in the database.
2. The system is online and the database is accessible.

**Main Flow**:
1. The client sends a GET request to `/api/articles/search` with a query parameter, e.g., `query=keyword`.
2. The system searches the articles collection for matches in one or more fields (e.g., title, content).
3. The system returns a 200 status code with a JSON array of matching articles.  
   Each article in the response includes:
   - `article_id`
   - `title`
   - `content`
   - `author`
   - `created_at`
   - `updated_at`
4. The response is ordered according to relevance or a defined sorting rule.

**Alternate Flows**:
- If no articles match the search query, the system returns an empty array with a 200 status.
- If the query parameter is missing or invalid, the system returns a 400 error with a descriptive message.

**Postconditions**:
- The client receives a filtered list of articles that match the search criteria.
