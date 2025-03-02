// cypress/e2e/Register.cy.js
describe('User Registration E2E', () => {
  beforeEach(() => {
    // Ensure your frontend server is running at http://localhost:3000
    cy.visit('http://localhost:3000/register')
  })

  it('registers a new user successfully', () => {
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
    // Check that the URL includes '/login' after successful registration
    cy.url().should('include', '/login')
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
    cy.contains('A user with this username or email already exists.').should('be.visible')
  })
})
