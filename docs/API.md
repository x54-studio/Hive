```markdown
# Hive API Documentation

## Overview
This document provides details on the Hive API endpoints, request/response structures, error codes, and authentication details.

## Endpoints

### GET /
- **Description:** Returns a welcome message.
- **Response:**
  ```json
  {
    "message": "Welcome to Hive!"
  }
  ```

### POST /api/register
- **Description:** Registers a new user.
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Responses:**
  - **201 Created:** 
    ```json
    {
      "message": "User registered successfully!",
      "user_id": "string"
    }
    ```
  - **400 Bad Request:** Missing required fields.
  - **500 Internal Server Error:** Registration error.

### POST /api/login
- **Description:** Authenticates a user and returns JWT access and refresh tokens.
- **Request Body:**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Responses:**
  - **200 OK:** 
    ```json
    {
      "message": "Login successful",
      "access_token": "string",
      "refresh_token": "string"
    }
    ```
  - **401 Unauthorized:** Invalid credentials or user not found.

### POST /api/refresh
- **Description:** Refreshes JWT tokens using the refresh token (sent as a cookie).
- **Responses:**
  - **200 OK:** 
    ```json
    {
      "message": "Token refreshed successfully",
      "access_token": "string",
      "refresh_token": "string"
    }
    ```
  - **401 Unauthorized:** Missing or invalid refresh token.

### GET /api/articles
- **Description:** Retrieves a paginated list of articles.
- **Query Parameters:**
  - `page` (default: 1)
  - `limit` (default: 10)
- **Response:**
  - **200 OK:** An array of article objects.
  - **500 Internal Server Error:** Error retrieving articles.

### POST /api/articles
- **Description:** Creates a new article (requires JWT authentication).
- **Request Body:**
  ```json
  {
    "title": "string",
    "content": "string"
  }
  ```
- **Responses:**
  - **201 Created:** 
    ```json
    {
      "message": "Article created successfully",
      "article_id": "string"
    }
    ```
  - **400 Bad Request:** Missing title or content.
  - **500 Internal Server Error:** Error creating article.

### GET /api/articles/{article_id}
- **Description:** Retrieves an article by its ID.
- **Parameters:**
  - `article_id` (path parameter, type: string)
- **Responses:**
  - **200 OK:** Article object.
  - **404 Not Found:** Article not found.

### PUT /api/articles/{article_id}
- **Description:** Updates an existing article (requires JWT authentication).
- **Parameters:**
  - `article_id` (path parameter, type: string)
- **Request Body:**
  ```json
  {
    "title": "string",    // Optional
    "content": "string"   // Optional
  }
  ```
- **Responses:**
  - **200 OK:** 
    ```json
    { "message": "Article updated successfully" }
    ```
  - **400 Bad Request:** No data provided for update.
  - **404 Not Found:** Article not found or update failed.

### DELETE /api/articles/{article_id}
- **Description:** Deletes an article (requires JWT authentication).
- **Parameters:**
  - `article_id` (path parameter, type: string)
- **Responses:**
  - **200 OK:** 
    ```json
    { "message": "Article deleted successfully" }
    ```
  - **404 Not Found:** Article not found or deletion failed.

### POST /api/logout
- **Description:** Logs out the user by deleting JWT cookies.
- **Response:**
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

### GET /api/protected
- **Description:** A protected endpoint that returns user identity and JWT claims. Requires JWT authentication.
- **Responses:**
  - **200 OK:** 
    ```json
    {
      "username": "string",
      "role": "string"
    }
    ```
  - **401 Unauthorized:** Access denied.

## Authentication Details

- **JWT Tokens:**  
  - **Access Token:** A short-lived token used for API requests.
  - **Refresh Token:** Used to obtain a new access token upon expiry.
  
- **Cookie Settings:**  
  Tokens are set as HTTP-only cookies. In production, secure settings (e.g., `JWT_COOKIE_SECURE`) are enabled.

## Error Handling

- **400 Bad Request:** Returned when required fields are missing or parameters are invalid.
- **404 Not Found:** Returned when a requested resource does not exist.
- **500 Internal Server Error:** Returned when unexpected errors occur. Detailed errors are logged server-side.

---
