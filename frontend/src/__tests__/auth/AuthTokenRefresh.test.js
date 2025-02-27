// src/__tests__/auth/AuthTokenRefresh.test.js
import { configureStore } from '@reduxjs/toolkit';
import axios from 'axios';
import authReducer, { setUser } from '../../redux/authSlice';
import { refreshTokens } from '../../redux/authActions'; // Ensure this thunk is defined and exported

// Create a custom store for testing with the initial state.
let store;
const initialState = {
  auth: {
    user: {
      username: "testUser",
      accessToken: "expiredToken",
      refreshToken: "validRefreshToken",
      claims: { role: "admin" },
    },
    loading: false,
    error: null,
  },
};

// Mock axios.post for the refresh endpoint.
jest.mock('axios');

describe("Auth Token Refresh Flow", () => {
  beforeEach(() => {
    // Create a store with the initial state.
    // Note: We no longer provide a custom middleware array since thunk is included by default.
    store = configureStore({
      reducer: { auth: authReducer },
      preloadedState: initialState,
    });
  });

  test("calls refresh token endpoint and updates user with new token data", async () => {
    // Arrange: prepare the new token data.
    const newUserData = {
      username: "testUser",
      accessToken: "newAccessToken",
      refreshToken: "newRefreshToken",
      claims: { role: "admin" },
    };

    // Mock axios.post to simulate a successful refresh token call.
    axios.post.mockResolvedValueOnce({
      data: newUserData,
    });

    // Act: dispatch the refreshTokens thunk.
    const result = await store.dispatch(refreshTokens());

    // Debug log the result.
    console.log("Result from refreshTokens:", result);

    // Assert: ensure the thunk was fulfilled.
    expect(result.meta.requestStatus).toBe("fulfilled");

    // Assert: ensure the payload matches newUserData.
    expect(result.payload).toEqual(newUserData);

    // Assert: Redux state should now hold the updated user data.
    const state = store.getState();
    console.log("Updated auth state:", state.auth.user);
    expect(state.auth.user).toEqual(newUserData);

    // Also, verify that axios.post was called with the correct URL and options.
    expect(axios.post).toHaveBeenCalledWith(
      "http://localhost:5000/api/refresh",
      {},
      { withCredentials: true }
    );
  });
});
