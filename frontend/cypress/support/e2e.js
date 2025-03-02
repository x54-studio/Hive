Cypress.Commands.add('maybeIntercept', (method, url, response, alias) => {
    if (Cypress.env('USE_MOCKS')) {
      cy.intercept(method, url, response).as(alias)
    }
  })
  