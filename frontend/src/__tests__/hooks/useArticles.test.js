// src/__tests__/useArticles.test.js
import React from "react";
import { renderHook, waitFor, act } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useArticles } from "../../hooks/useArticles";

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        cacheTime: 0,
        refetchOnMount: true,
      },
    },
  });

const wrapper = ({ children }) => (
  <QueryClientProvider client={createTestQueryClient()}>
    {children}
  </QueryClientProvider>
);

describe("useArticles hook", () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });
  afterEach(() => {
    jest.resetAllMocks();
  });

  test("returns loading state initially", async () => {
    // Simulate a never-resolving promise to keep the hook in the "pending" state.
    global.fetch.mockImplementation(() => new Promise(() => {}));
    const { result } = renderHook(() => useArticles(0), { wrapper });
    await waitFor(() => result.current.status !== undefined, { timeout: 500 });
    // In React Query v5, the initial loading state is "pending"
    expect(result.current.status).toBe("pending");
  });

  test("returns articles on successful fetch", async () => {
    const articles = [{ _id: "1", title: "Test Article", content: "Content here" }];
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => articles,
    });
    const { result } = renderHook(() => useArticles(0), { wrapper });

    // Flush pending microtasks.
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    // Wait for the hook's status to update.
    await waitFor(() => result.current.status !== "pending", { timeout: 2000 });
    expect(result.current.status).toBe("success");
    expect(result.current.data).toBeDefined();
    expect(result.current.data.pages).toBeDefined();
    expect(Array.isArray(result.current.data.pages)).toBe(true);
    expect(result.current.data.pages.flat()).toEqual(articles);
  });

  test("returns error on fetch failure", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: "Fetch failed" }),
    });
    const { result } = renderHook(() => useArticles(0), { wrapper });

    // Flush pending microtasks.
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    // Wait for the hook's status to update.
    await waitFor(() => result.current.status !== "pending", { timeout: 2000 });
    expect(result.current.status).toBe("error");
    expect(result.current.error).toBeDefined();
    expect(result.current.error.message).toBe("Failed to fetch articles.");
  });
});
