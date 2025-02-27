// src/__tests__/article/ArticleList.test.js
import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import ArticleList from "../../components/ArticleList"; // Corrected path
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../../redux/authSlice";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// Preloaded state for testing
const preloadedState = {
  auth: {
    user: { username: "adminUser", claims: { role: "admin" } },
    loading: false,
    error: null,
  },
};

// Create a test Redux store
const store = configureStore({
  reducer: { auth: authReducer },
  preloadedState,
});

// Create a test QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      cacheTime: 0,
    },
  },
});

// Helper to render with both Redux and QueryClient providers
const renderWithProviders = (ui) => {
  return render(
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
    </Provider>
  );
};

describe("ArticleList Component", () => {
  test("displays articles after successful fetch", async () => {
    renderWithProviders(<ArticleList refreshSignal={0} />);
    console.log("Rendered DOM in ArticleList.test.js:", screen.debug());
    console.log("Waiting for 'Article 1' to appear...");
    await waitFor(() => {
      expect(screen.getByText("Article 1")).toBeInTheDocument();
    });
  });

  test("refetches articles when refreshSignal changes", async () => {
    const { rerender } = renderWithProviders(<ArticleList refreshSignal={0} />);
    await waitFor(() => {
      expect(screen.getByText("Article 1")).toBeInTheDocument();
    });
    // Simulate refresh by re-rendering with a changed refreshSignal
    rerender(
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <ArticleList refreshSignal={1} />
        </QueryClientProvider>
      </Provider>
    );
    console.log("Re-rendered with refreshSignal changed. Waiting for 'Article 1' again...");
    await waitFor(() => {
      expect(screen.getByText("Article 1")).toBeInTheDocument();
    });
  });
});
