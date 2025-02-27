// src/__tests__/useUserRole.test.js
import React from "react";
import { renderHook } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../../redux/authSlice";
import useUserRole from "../../hooks/useUserRole";

// Provide a preloaded state for testing
const preloadedState = {
  auth: {
    user: { username: "testUser", claims: { role: "admin" } },
    loading: false,
    error: null,
  },
};

// Create a test store with the preloaded state.
const testStore = configureStore({
  reducer: { auth: authReducer },
  preloadedState,
});

// Create a wrapper component that supplies the Redux store.
const wrapper = ({ children }) => <Provider store={testStore}>{children}</Provider>;

test("should return the current user role", () => {
  const { result } = renderHook(() => useUserRole(), { wrapper });
  expect(result.current).toBe("admin");
});
