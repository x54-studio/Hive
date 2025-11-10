// cypress/e2e/AsyncButton.cy.js
describe('Async Button Component', () => {
  beforeEach(() => {
    // Visit the test page for the AsyncButton component.
    cy.visit('http://localhost:3000/async-button-test')
    // Assert that the header is visible to confirm the correct page loaded.
    cy.contains('Async Button Test').should('be.visible')
  })

  it('disables the button and shows loading text when clicked, then re-enables it', () => {
    // Verify the button exists using our data-cy attribute.
    cy.get('[data-cy="async-button"]').should('exist').and('contain.text', 'Submit').and('not.be.disabled')

    // Click the button.
    cy.get('[data-cy="async-button"]').click()

    // Immediately after clicking, the button should display "Processing..." and be disabled.
    cy.get('[data-cy="async-button"]').should('contain.text', 'Processing...').and('be.disabled')

    // Wait for the async operation to complete (2 seconds plus a small buffer).
    cy.wait(2100)

    // After the operation, the button should revert to "Submit" and be enabled.
    cy.get('[data-cy="async-button"]').should('contain.text', 'Submit').and('not.be.disabled')
  })

  it('prevents multiple clicks during the async operation', () => {
    // Click the button multiple times.
    cy.get('[data-cy="async-button"]').click().click().click()

    // The button should remain disabled and display "Processing..."
    cy.get('[data-cy="async-button"]').should('be.disabled').and('contain.text', 'Processing...')

    // Wait for the async operation to finish.
    cy.wait(2100)

    // After the operation, the button should revert to "Submit" and be enabled.
    cy.get('[data-cy="async-button"]').should('contain.text', 'Submit').and('not.be.disabled')
  })
})
