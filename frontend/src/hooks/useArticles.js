// src/hooks/useArticles.js
import { useInfiniteQuery } from "@tanstack/react-query";

const fetchArticles = async ({ pageParam = 1 }) => {
  const response = await fetch(`http://localhost:5000/api/articles?page=${pageParam}`, {
    credentials: "include",
  });
  if (!response.ok) {
    throw new Error("Failed to fetch articles.");
  }
  return response.json();
};

export const useArticles = (refreshSignal) => {
  return useInfiniteQuery({
    queryKey: ["articles", refreshSignal],
    queryFn: fetchArticles,
    getNextPageParam: (lastPage, allPages) =>
      lastPage.length === 0 ? undefined : allPages.length + 1,
    refetchOnMount: true,
    cacheTime: 0,
    enabled: true,
  });
};
