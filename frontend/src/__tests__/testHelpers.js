// Example: src/__tests__/testHelpers.js
import React from "react";
import { render } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import authReducer from "../redux/authSlice";

export const renderWithProviders = (ui, { preloadedState, store = configureStore({
    reducer: { auth: authReducer },
    preloadedState,
  }), queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, cacheTime: 0 } },
  }) } = {}) => {
  return render(
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
    </Provider>
  );
};

// This file now contains at least one dummy test.
test("dummy test", () => {
  expect(true).toBe(true);
});
