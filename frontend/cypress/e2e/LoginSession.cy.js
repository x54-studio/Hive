// cypress/e2e/Login.cy.js
describe('Login Page - Async Button Behavior', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login')
  })

  it('disables the login button and shows loading text when clicked, then navigates to profile on success', () => {
    // Intercept the login API call with a delay to simulate async behavior.
    cy.intercept('POST', '/api/login', (req) => {
      req.reply({
        delay: 500, // 500ms delay
        statusCode: 200,
        body: { message: 'Login successful' },
      })
    }).as('loginRequest')

    // Intercept the protected endpoint call for fetching user data.
    cy.intercept('GET', '/api/protected', {
      statusCode: 200,
      body: { username: 'testUser', email: 'test@example.com' },
    }).as('protectedRequest')

    // Verify that the login button initially shows "Login" and is enabled.
    cy.get('button[type="submit"]').should('contain.text', 'Login').and('not.be.disabled')

    // Click the login button.
    cy.get('button[type="submit"]').click()

    // Immediately after clicking, the button should show "Logging in..." and be disabled.
    cy.get('button[type="submit"]').should('contain.text', 'Logging in...').and('be.disabled')

    // Wait for the API calls to complete.
    cy.wait('@loginRequest')
    cy.wait('@protectedRequest')

    // Verify that the user is navigated to the profile page.
    cy.url().should('include', '/profile')
  })

  it('displays an error toast when login fails', () => {
    // Intercept the login API call to simulate a failed login.
    cy.intercept('POST', '/api/login', {
      statusCode: 400,
      body: { error: 'Invalid credentials' },
    }).as('loginFailure')

    // Attempt login with invalid credentials.
    cy.get('input[placeholder="Username or Email"]').type('wrongUser')
    cy.get('input[placeholder="Password"]').type('wrongPass')
    cy.get('button[type="submit"]').click()

    cy.wait('@loginFailure')

    // Check that the login button still shows the loading state until failure is handled.
    // Then, verify that an error toast is displayed (assuming you use react-toastify).
    cy.get('.Toastify__toast', { timeout: 6000 })
      .should('be.visible')
      .and('contain.text', 'Invalid credentials')
  })
})
