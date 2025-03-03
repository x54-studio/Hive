// cypress/e2e/AsyncButton.cy.js
describe('Async Button Component', () => {
    beforeEach(() => {
      // Visit the test page that renders the AsyncButton component.
      cy.visit('http://localhost:3000/async-button-test')
    })
  
    it('disables the button and shows loading text when clicked, then re-enables it', () => {
      // The button should initially be enabled with text "Submit"
      cy.get('button').should('contain.text', 'Submit').and('not.be.disabled')
  
      // Click the button
      cy.get('button').click()
  
      // Immediately, the button should be disabled and show "Processing..."
      cy.get('button').should('contain.text', 'Processing...').and('be.disabled')
  
      // Wait for the async operation (2 seconds) to complete
      cy.wait(2100)
  
      // After the async operation, the button should be re-enabled and show "Submit" again
      cy.get('button').should('contain.text', 'Submit').and('not.be.disabled')
    })
  
    it('prevents multiple clicks during the async operation', () => {
      // Click the button multiple times
      cy.get('button').click().click().click()
  
      // The button should only have triggered the click handler once,
      // meaning it remains disabled and its text is "Processing..."
      cy.get('button').should('be.disabled').and('contain.text', 'Processing...')
  
      // Wait for the async operation to finish
      cy.wait(2100)
  
      // After completion, the button should be enabled again with the original text.
      cy.get('button').should('contain.text', 'Submit').and('not.be.disabled')
    })
  })
  