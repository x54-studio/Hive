// src/__tests__/api/axiosInstance.test.js
import axiosInstance, { setStore } from '../../api/axiosInstance'
import MockAdapter from 'axios-mock-adapter'
import { refresh, logout } from '../../redux/slices/authSlice'

// Mock the auth actions so they return predictable action objects.
jest.mock('../../redux/slices/authSlice', () => ({
  refresh: jest.fn(() => ({ type: 'auth/refresh/pending' })),
  logout: jest.fn(() => ({ type: 'auth/logout' }))
}));

// Create a dummy store with a mocked dispatch method.
const dummyStore = {
  dispatch: jest.fn((action) => {
    // For refresh actions, by default simulate a success.
    if (action && action.type && action.type.includes('auth/refresh')) {
      return Promise.resolve({ payload: {} });
    }
    // For logout or other actions, resolve as well.
    return Promise.resolve({ payload: {} });
  }),
};

describe('axiosInstance interceptor for token refresh', () => {
  let mock;

  beforeEach(() => {
    // Set the dummy store so the interceptor uses it.
    setStore(dummyStore);
    dummyStore.dispatch.mockClear();
    mock = new MockAdapter(axiosInstance);
  });

  afterEach(() => {
    mock.restore();
  });

  test('retries the original request after a successful refresh', async () => {
    // Simulate GET /protected returns 401 once.
    mock.onGet('/protected').replyOnce(401);
    // Simulate a successful POST /refresh.
    mock.onPost('/refresh').replyOnce(200, { message: 'Token refreshed successfully' });
    // After refresh, simulate a successful GET /protected.
    mock.onGet('/protected').replyOnce(200, { data: 'success' });

    const response = await axiosInstance.get('/protected');
    expect(response.data).toEqual({ data: 'success' });

    // Verify that dispatch was called with an action whose type includes 'auth/refresh'.
    const refreshCall = dummyStore.dispatch.mock.calls.find(
      (call) => call[0].type && call[0].type.includes('auth/refresh')
    );
    expect(refreshCall).toBeDefined();
  });

  test('rejects the promise if refresh fails and dispatches logout', async () => {
    // Simulate GET /protected returns 401.
    mock.onGet('/protected').replyOnce(401);
    // Do not set up an intercept for POST /refresh so that the failure comes solely from the dummy store.
    // Override dummyStore.dispatch for refresh to simulate a failure.
    dummyStore.dispatch.mockImplementationOnce((action) => {
      if (action.type && action.type.includes('auth/refresh')) {
        return Promise.reject({ response: { data: { error: 'Refresh failed' } } });
      }
      return Promise.resolve({ payload: {} });
    });

    let caughtError;
    try {
      await axiosInstance.get('/protected');
      throw new Error('Expected request to fail');
    } catch (error) {
      caughtError = error;
    }
    // Assert that the error object is what we expect.
    expect(caughtError.response).toBeDefined();
    expect(caughtError.response.data).toEqual({ error: 'Refresh failed' });

    // Verify that the refresh action was dispatched.
    const refreshCall = dummyStore.dispatch.mock.calls.find(
      (call) => call[0].type && call[0].type.includes('auth/refresh')
    );
    expect(refreshCall).toBeDefined();

    // Verify that logout was dispatched.
    const logoutCall = dummyStore.dispatch.mock.calls.find(
      (call) => call[0].type && call[0].type.includes('auth/logout')
    );
    expect(logoutCall).toBeDefined();
  });
});
