// cypress/e2e/Register.cy.js
describe('User Registration E2E with Toast Notification', () => {
  beforeEach(() => {
    // Ensure your frontend server is running at the correct URL.
    cy.visit('http://localhost:3000/register')
  })

  it('registers a new user and displays success toast on login page', () => {
    cy.intercept('POST', '/api/register', {
      statusCode: 200,
      body: { message: 'User registered successfully! Please log in.', user_id: '12345' },
    }).as('registerRequest')

    cy.get('input[placeholder="Username"]').type('newUser')
    cy.get('input[placeholder="Email"]').type('newuser@example.com')
    cy.get('input[placeholder="Password"]').type('password123')
    cy.get('input[placeholder="Confirm Password"]').type('password123')
    cy.get('button').contains(/register/i).click()

    cy.wait('@registerRequest')
    // Check that the URL now includes '/login'
    cy.url().should('include', '/login')
    // Wait for the toast element (with class Toastify__toast) to appear and verify its content
    cy.get('.Toastify__toast', { timeout: 6000 })
      .should('be.visible')
      .and('contain.text', 'User registered successfully! Please log in.')
  })

  it('shows error message on registration failure', () => {
    cy.intercept('POST', '/api/register', {
      statusCode: 400,
      body: { error: 'A user with this username or email already exists.' },
    }).as('registerFailure')

    cy.get('input[placeholder="Username"]').type('existingUser')
    cy.get('input[placeholder="Email"]').type('existing@example.com')
    cy.get('input[placeholder="Password"]').type('password123')
    cy.get('input[placeholder="Confirm Password"]').type('password123')
    cy.get('button').contains(/register/i).click()

    cy.wait('@registerFailure')
    // Check for the error toast message
    cy.get('.Toastify__toast', { timeout: 6000 })
      .should('be.visible')
      .and('contain.text', 'A user with this username or email already exists.')
  })
})
