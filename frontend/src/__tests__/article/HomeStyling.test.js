// src/__tests__/HomeStyling.test.js
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Home from '../../pages/Home';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../../redux/authSlice';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Preloaded Redux state
const preloadedState = {
  auth: { user: { username: "adminUser", claims: { role: "admin" } } },
};

// Create Redux store
const store = configureStore({ reducer: { auth: authReducer }, preloadedState });

// Create a QueryClient with initialData for the "articles" query.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      initialData: {
        pages: [[{ _id: "1", title: "Article 1", content: "Content 1" }]],
        pageParams: [undefined],
      },
      refetchOnMount: false,
      retry: false,
    },
  },
});

// Helper function to render components with both Redux and QueryClient providers.
const renderWithProviders = (ui) => {
  return render(
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        {ui}
      </QueryClientProvider>
    </Provider>
  );
};

test("renders articles with proper styling", async () => {
  renderWithProviders(<Home />);
  // Wait until the article is rendered.
  await waitFor(() => {
    expect(screen.getByText("Article 1")).toBeInTheDocument();
  });
  const articleTitle = screen.getByText("Article 1");
  // Check that the nearest div (the article container) has the styling class "border"
  expect(articleTitle.closest("div")).toHaveClass("border");
});
