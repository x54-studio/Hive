// cypress/e2e/AdminUserManagement.cy.js

describe('Admin User Management - Create/Edit/Delete', () => {
  beforeEach(() => {
    // Intercept the requests for the /users API
    cy.intercept('GET', '**/users**', {
      statusCode: 200,
      body: {
        data: [
          { _id: '1', username: 'user1', email: 'user1@example.com', role: 'admin' },
          { _id: '2', username: 'user2', email: 'user2@example.com', role: 'editor' }
        ]
      }
    }).as('getInitialUsers')

    // Visit the root (or any route that returns HTML)
    cy.visit('http://localhost:3000/', { failOnStatusCode: false })

    // Now navigate within the app to /admin/users
    // e.g. if there's a nav link:
    cy.contains('Admin Users').click()

    // Wait for the initial request
    cy.wait('@getInitialUsers')
  })

  it('creates a new user and refreshes the list', () => {

    // Intercept POST for creating a new user.
    cy.intercept('POST', '**/users**', {
      statusCode: 200,
      body: { _id: '99', username: 'newUser', email: 'newuser@example.com', role: 'user' }
    }).as('createUser');

    // Intercept GET after creation that returns the new user.
    cy.intercept('GET', '**/users**', {
      statusCode: 200,
      body: {
        data: [{ _id: '99', username: 'newUser', email: 'newuser@example.com', role: 'user' }]
      }
    }).as('refetchUsers');

    // Click the "Create New User" button.
    cy.get('button').contains(/create new user/i).click();

    // Fill out the form.
    cy.get('input#username').type('newUser');
    cy.get('input#email').type('newuser@example.com');
    cy.get('select#role').select('user');
    cy.get('input#password').type('pass123');

    // Submit the form.
    cy.get('button').contains(/^create user$/i).click();

    // Wait for the re-fetch and verify that the new user appears.
    cy.wait('@refetchUsers');
    cy.contains('newUser').should('be.visible');
    cy.contains('newuser@example.com').should('be.visible');
  });

  it('edits an existing user and refreshes the list', () => {
    // Intercept GET returning the old user.
    cy.intercept('GET', '**/users**', {
      statusCode: 200,
      body: {
        data: [{ _id: '1', username: 'oldName', email: 'old@example.com', role: 'admin' }]
      }
    }).as('getOldUser');

    // Intercept PUT to update the user.
    cy.intercept('PUT', '**/users/1**', {
      statusCode: 200,
      body: { _id: '1', username: 'updatedName', email: 'updated@example.com', role: 'admin' }
    }).as('editUser');

    // Intercept GET returning the updated user.
    cy.intercept('GET', '**/users**', {
      statusCode: 200,
      body: {
        data: [{ _id: '1', username: 'updatedName', email: 'updated@example.com', role: 'admin' }]
      }
    }).as('refetchAfterEdit');

    // Re-visit to trigger the old user fetch.
    cy.visit('http://localhost:3000/admin/users', { failOnStatusCode: false });
    cy.wait('@getOldUser');
    cy.contains('oldName').should('be.visible');

    // Click the "Edit" button for the row containing "oldName".
    cy.contains('oldName').parent('tr').within(() => {
      cy.get('button').contains('Edit').click();
    });

    // Update the form fields.
    cy.get('input#username').clear().type('updatedName');
    cy.get('input#email').clear().type('updated@example.com');

    // Click the "Update User" button.
    cy.get('button').contains(/^update user$/i).click();

    cy.wait('@refetchAfterEdit');
    cy.contains('updatedName').should('be.visible');
    cy.contains('oldName').should('not.exist');
  });

  it('deletes a user', () => {
    // Intercept GET returning a user.
    cy.intercept('GET', '**/users**', {
      statusCode: 200,
      body: {
        data: [{ _id: '1', username: 'deleteMe', email: 'del@example.com', role: 'user' }]
      }
    }).as('getUser');

    // Intercept DELETE for the user.
    cy.intercept('DELETE', '**/users/1**', {
      statusCode: 200
    }).as('deleteUser');

    cy.visit('http://localhost:3000/admin/users', { failOnStatusCode: false });
    cy.wait('@getUser');
    cy.contains('deleteMe').should('be.visible');

    // In the row for "deleteMe", click the "Delete" button.
    cy.contains('deleteMe').parent('tr').within(() => {
      cy.get('button').contains('Delete').click();
    });

    // Confirm deletion.
    cy.on('window:confirm', () => true);

    // Verify that the user is no longer visible.
    cy.contains('deleteMe').should('not.exist');
  });
});
