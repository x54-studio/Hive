// src/__tests__/logUserRole.test.js
import React from "react";
import { renderHook } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../../redux/authSlice";
import useUserRole from "../../hooks/useUserRole"; // Ensure this hook exists and returns user.claims.role

// Create a test Redux store with the desired preloaded state.
const createTestStore = (preloadedState) =>
  configureStore({
    reducer: { auth: authReducer },
    preloadedState,
  });

// Create a wrapper that provides the Redux store context.
const wrapper = ({ children }) => {
  const store = createTestStore({
    auth: {
      user: { username: "testUser", claims: { role: "admin" } },
      loading: false,
      error: null,
    },
  });
  return <Provider store={store}>{children}</Provider>;
};

test("logs and returns the current user role", () => {
  const { result } = renderHook(() => useUserRole(), { wrapper });
  // Log the role for debugging.
  console.log("Current user role:", result.current);
  expect(result.current).toBe("admin");
});
