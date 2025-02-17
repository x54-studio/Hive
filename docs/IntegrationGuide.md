```markdown
# Integration Guide

## Overview
This guide describes how to set up and run integration tests for the Hive system using the TEST_MONGO database. It covers database seeding, running tests, and cleaning up the test environment.

## Setup

1. **Set Environment Variable**  
   Ensure the environment variable `TESTING` is set to `"true"`. This configures the application to use test-specific settings.

2. **Seed the Test Database**  
   Run the seeder script to populate the test database with initial data:
   ```bash
   python backend/tests/integrationSeeder.py
   ```
   This script will:
   - Clear existing data in the `users` and `articles` collections.
   - Insert predefined test users and test articles.

## Running Integration Tests

Execute the integration tests using:
```bash
python backend/tests/test_integration_api.py
```
These tests cover:
- The home route (GET `/`)
- User registration and login workflows
- Token refresh and protected endpoint access
- Full CRUD operations for articles

## Post-Test Cleanup

After the tests run, the test database is automatically dropped and the MongoClient is closed. This ensures that no residual data affects subsequent test runs.

## Additional Notes

- **Authentication:**  
  Some endpoints require JWT authentication. The integration tests extract cookies from the login responses and use them in subsequent requests.

- **Environment:**  
  The integration tests use the configuration defined in `Config`, specifically `TEST_MONGO_URI` and `TEST_MONGO_DB_NAME`.

- **Error Handling:**  
  Integration tests validate that error responses (e.g., 404 for non-existent resources) are returned as expected.

This Integration Guide ensures a consistent and repeatable test environment for validating the end-to-end functionality of the Hive API.
```