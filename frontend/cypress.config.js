// cypress.config.js
module.exports = {
  e2e: {
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: false,
    env: {
      USE_MOCKS: process.env.USE_MOCKS || true,  // defaults to true for local testing
    },
  },
}
