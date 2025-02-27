// src/__tests__/authSlice.test.js
import axios from 'axios';
import { login } from '../../redux/authSlice';
import reducer, { setUser } from '../../redux/authSlice';

jest.mock('axios');

describe('authSlice async thunk', () => {
  const initialState = { user: null, loading: false, error: null };

  // Example user data returned from /api/protected
  const userData = {
    email: "test@example.com",
    username: "test",
    claims: { role: "admin", exp: Math.floor(Date.now() / 1000) + 3600 }
  };

  test('login async thunk dispatches fulfilled action and sets user on successful login', async () => {
    // Mock the POST call to /api/login (assumed to return an empty object)
    axios.post.mockResolvedValueOnce({ data: {} });
    // Mock the GET call to /api/protected to return userData
    axios.get.mockResolvedValueOnce({ data: userData });

    // For testing async thunks, we call the thunk with dispatch and getState.
    const dispatch = jest.fn();
    const getState = () => initialState;
    // Execute the login thunk with sample credentials.
    const actionResult = await login({ email: "test@example.com", password: "password" })(dispatch, getState, undefined);

    // The payload should be equal to the userData returned from /api/protected.
    expect(actionResult.payload).toEqual(userData);

    // Also verify that the reducer, when processing the fulfilled action, updates state correctly.
    const stateAfterFulfilled = reducer(initialState, { type: login.fulfilled.type, payload: userData });
    expect(stateAfterFulfilled.user).toEqual(userData);
  });

  test('login async thunk dispatches rejected action on login failure', async () => {
    // Simulate an error response from the login POST request.
    const errorResponse = { message: "Login failed" };
    axios.post.mockRejectedValueOnce({ response: { data: errorResponse } });

    const dispatch = jest.fn();
    const getState = () => initialState;
    const actionResult = await login({ email: "wrong@example.com", password: "wrong" })(dispatch, getState, undefined);

    // When rejected, the thunk's error should contain the error payload.
    expect(actionResult.error).toBeDefined();
    expect(actionResult.error.message).toContain("Rejected");
  });
});
