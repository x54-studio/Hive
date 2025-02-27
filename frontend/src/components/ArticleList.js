// src/components/ArticleList.js
import React from "react";
import { useInfiniteQuery, useQueryClient } from "@tanstack/react-query";
import { useSelector } from "react-redux";
import axios from "axios";
import { fetchArticles } from "../api/articles"; // Ensure this file exports your fetchArticles function

const ArticleList = ({ refreshSignal }) => {
  // Retrieve current user from Redux
  const { user } = useSelector((state) => state.auth);
  const isAdmin = user?.claims?.role === "admin";
  const queryClient = useQueryClient();

  // Use React Query's useInfiniteQuery with the object signature (v5)
  const { data, error, status } = useInfiniteQuery({
    queryKey: ["articles", refreshSignal],
    queryFn: fetchArticles,
    // Adjust getNextPageParam based on your API response (if pagination is used)
    getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
  });

  // Function to handle deletion of an article
  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/api/articles/${id}`, {
        withCredentials: true,
      });
      // Invalidate the articles query to force a refetch
      queryClient.invalidateQueries({ queryKey: ["articles"] });
    } catch (err) {
      console.error("Error deleting article:", err);
    }
  };

  if (status === "loading" || status === "pending") {
    return <p>Loading articles...</p>;
  }

  if (error) {
    return <p>Error: {error.message}</p>;
  }

  // Ensure data.pages is an array of pages
  const pages = Array.isArray(data.pages) ? data.pages : [data];
  const allArticles = pages.flat();

  return (
    <div className="space-y-6">
      {allArticles.map((article) => (
        <div
          key={article._id}
          className="border rounded-lg shadow-lg p-4 bg-white dark:bg-gray-800"
        >
          <h3 className="font-bold text-xl text-gray-900 dark:text-gray-100">
            {article.title}
          </h3>
          <p className="mt-2 text-gray-700 dark:text-gray-300">
            {article.content}
          </p>
          {isAdmin && (
            <button
              onClick={() => handleDelete(article._id)}
              className="bg-red-500 text-white px-3 py-1 mt-2 rounded"
            >
              Delete
            </button>
          )}
        </div>
      ))}
      {/* Example "Load More" button (if using pagination) */}
      <button
        onClick={() =>
          queryClient.fetchQuery({ queryKey: ["articles"] })
        }
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Load More
      </button>
    </div>
  );
};

export default ArticleList;
