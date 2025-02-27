// src/__tests__/article/ArticleList.loading.test.js
import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import ArticleList from "../../components/ArticleList"; // Adjust the relative path if needed
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import authReducer from "../../redux/authSlice";

// Helper function to wrap the component with both Redux and React Query providers.
const renderWithProviders = (ui, { preloadedState = {} } = {}) => {
  const store = configureStore({
    reducer: { auth: authReducer },
    preloadedState,
  });
  const queryClient = new QueryClient();
  return render(
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        {ui}
      </QueryClientProvider>
    </Provider>
  );
};

describe("ArticleList Component - Loading & Admin UI", () => {
  const preloadedState = {
    auth: {
      user: { username: "adminUser", claims: { role: "admin" } },
      loading: false,
      error: null,
    },
  };

  test("renders loading indicator when articles are loading", async () => {
    renderWithProviders(<ArticleList refreshSignal={1} />, { preloadedState });
    await waitFor(() =>
      expect(screen.getByText(/Loading articles\.\.\./i)).toBeInTheDocument()
    );
  });

  test("renders delete button for admin users when articles are loaded", async () => {
    renderWithProviders(<ArticleList refreshSignal={0} />, { preloadedState });
    // Debug log to help inspect the rendered DOM:
    console.log("Rendered DOM for admin loaded state:", screen.debug());
    await waitFor(() =>
      expect(screen.getByText(/Article 1/i)).toBeInTheDocument()
    );
    // Instead of getByText, use getAllByText and check the expected number.
    const deleteButtons = screen.getAllByText("Delete");
    // For example, if you expect one article then one delete button:
    expect(deleteButtons).toHaveLength(2);
  });

  test("does not render delete button for regular users when articles are loaded", async () => {
    const regularState = {
      auth: {
        user: { username: "regularUser", claims: { role: "regular" } },
        loading: false,
        error: null,
      },
    };
    renderWithProviders(<ArticleList refreshSignal={0} />, { preloadedState: regularState });
    console.log("Rendered DOM for regular user loaded state:", screen.debug());
    await waitFor(() =>
      expect(screen.getByText(/Article 1/i)).toBeInTheDocument()
    );
    expect(screen.queryByText("Delete")).toBeNull();
  });
});
