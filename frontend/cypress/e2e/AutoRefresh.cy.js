// cypress/e2e/AutoRefresh.cy.js

describe('Automatic Token Refresh', () => {
    beforeEach(() => {
      // Intercept the POST refresh endpoint.
      // This stub simulates the refresh endpoint behavior:
      // - It returns a 200 status.
      // - It sets HTTP‑only cookies via a single "set-cookie" header.
      // - It returns a JSON message.
      cy.intercept('POST', '/api/refresh', {
        statusCode: 200,
        headers: {
          'set-cookie': 'access_token=fake-renewed-token; HttpOnly; Path=/; Max-Age=600, refresh_token=fake-renewed-refresh-token; HttpOnly; Path=/; Max-Age=86400'
        },
        body: { message: "Token refreshed successfully" }
      }).as('refreshRequest');
  
      // Intercept the GET protected endpoint.
      // This stub simulates a protected endpoint returning user data with a claims object.
      cy.intercept('GET', '/api/protected', {
        statusCode: 200,
        body: {
          username: 'testUser',
          claims: { exp: Date.now() + 600000 } // Token expires 10 minutes from now.
        }
      }).as('getProtected');
    });
  
    it('refreshes the token and returns success via the refresh endpoint', () => {
      // Call the refresh endpoint using a relative URL so that Cypress prepends the baseUrl.
      cy.request({
        method: 'POST',
        url: '/api/refresh',
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.equal(200);
        expect(response.body).to.have.property('message', 'Token refreshed successfully');
        expect(response.headers).to.have.property('set-cookie');
        const setCookieHeader = response.headers['set-cookie'];
        expect(setCookieHeader).to.be.a('string');
        expect(setCookieHeader).to.include('access_token=fake-renewed-token');
        expect(setCookieHeader).to.include('refresh_token=fake-renewed-refresh-token');
      });
    });
  
    it('fetches protected user data after refresh', () => {
      // Call the protected endpoint using a relative URL.
      cy.request({
        method: 'GET',
        url: '/api/protected',
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.equal(200);
        expect(response.body).to.have.property('username', 'testUser');
        expect(response.body).to.have.property('claims');
        expect(response.body.claims).to.have.property('exp');
        // Verify that the expiration timestamp is in the future.
        expect(response.body.claims.exp).to.be.greaterThan(Date.now());
      });
    });
  });
  