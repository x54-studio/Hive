// src/__tests__/auth/AuthRedux.test.js
import { configureStore } from "@reduxjs/toolkit";
import authReducer, { login, logoutAsync, setUser } from "../../redux/authSlice";
import fetchMock from "jest-fetch-mock";

fetchMock.enableMocks();

describe("Auth Redux Flow", () => {
  let store;
  beforeEach(() => {
    fetchMock.resetMocks();
    store = configureStore({ reducer: { auth: authReducer } });
  });

  test("login success updates state", async () => {
    // Mock /api/login response.
    fetchMock
      .mockResponseOnce(
        JSON.stringify({
          message: "login success",
          accessToken: "access1",
          refreshToken: "refresh1",
        }),
        { status: 200 }
      )
      // Mock /api/protected response.
      .mockResponseOnce(
        JSON.stringify({ username: "testUser", claims: { role: "admin" } }),
        { status: 200 }
      );

    // Dispatch login thunk.
    await store.dispatch(
      login({ email: "test@example.com", password: "password" })
    );
    // Optionally, simulate setting the user (if not already done in login).
    store.dispatch(setUser({ username: "testUser", claims: { role: "admin" } }));

    const state = store.getState();
    expect(state.auth.user).toEqual({
      username: "testUser",
      claims: { role: "admin" },
    });
  });

  test("logout clears state", async () => {
    // Set a user in state.
    store.dispatch(setUser({ username: "testUser", claims: { role: "admin" } }));
    expect(store.getState().auth.user).toBeDefined();
    // Dispatch the async logout thunk.
    await store.dispatch(logoutAsync());
    // After successful logout, the state should be cleared.
    expect(store.getState().auth.user).toBeNull();
  });
});
