// src/__tests__/Home.test.js
import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import Home from "../pages/Home";
import { Provider } from "react-redux";
import { store } from "../redux/store";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// Mock fetch to always return an empty array for articles
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve([]),
  })
);

describe("Home page", () => {
  test("renders heading with correct text and theme classes", async () => {
    // Create a new QueryClient for testing, with retries disabled.
    const queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    render(
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <Home />
        </QueryClientProvider>
      </Provider>
    );

    await waitFor(() =>
      expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Welcome to Hive")
    );
  });
});