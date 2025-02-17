// src/components/ArticleList.js
import React, { useEffect, useState, useRef, useCallback, useContext } from "react";
import { AuthContext } from "../AuthContext";

function ArticleList({ refreshSignal }) {
  const { user } = useContext(AuthContext);
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const observer = useRef();

  const fetchArticles = useCallback(async (pageNumber = 1) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/api/articles?page=${pageNumber}`, {
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error("Failed to fetch articles.");
      }
      const data = await response.json();
      if (pageNumber === 1) {
        setArticles(data);
      } else {
        setArticles((prev) => [...prev, ...data]);
      }
      setHasMore(data.length > 0);
    } catch (error) {
      console.error("Error fetching articles:", error);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    setArticles([]);
    setPage(1);
    setHasMore(true);
    fetchArticles(1);
  }, [refreshSignal, fetchArticles]);

  useEffect(() => {
    if (page > 1) {
      fetchArticles(page);
    }
  }, [page, fetchArticles]);

  const lastArticleRef = useCallback(
    (node) => {
      if (loading) return;
      if (observer.current) observer.current.disconnect();
      observer.current = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && hasMore) {
          setPage((prevPage) => prevPage + 1);
        }
      });
      if (node) observer.current.observe(node);
    },
    [loading, hasMore]
  );

  const handleDelete = async (articleId) => {
    try {
      const response = await fetch(`http://localhost:5000/api/articles/${articleId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Failed to delete article.");
      }
      setArticles((prevArticles) =>
        prevArticles.filter((article) => article._id !== articleId)
      );
    } catch (err) {
      console.error("Error deleting article:", err.message);
      alert("Failed to delete article: " + err.message);
    }
  };

  return (
    <div>
      {articles.map((article, index) => {
        const articleContent = (
          <div
            key={article._id}
            className="border p-4 rounded-lg shadow-lg bg-gray-100 dark:bg-gray-800 mb-4"
          >
            <h3 className="font-semibold text-lg text-gray-900 dark:text-white">
              {article.title}
            </h3>

            <p className="text-sm text-gray-800 dark:text-gray-200 mt-2">
              {article.content}
            </p>
            {user && user.role === "admin" && (
              <button
                onClick={() => handleDelete(article._id)}
                className="bg-red-500 text-white px-3 py-1 mt-2 rounded"
              >
                Delete
              </button>
            )}
          </div>
        );
        if (index === articles.length - 1) {
          return (
            <div ref={lastArticleRef} key={article._id}>
              {articleContent}
            </div>
          );
        }
        return articleContent;
      })}
      {loading && <p className="text-gray-800 dark:text-gray-300">Loading articles...</p>}
      {!hasMore && (<p className="text-gray-800 dark:text-gray-300">No more articles</p>)}
    </div>
  );
}

export default ArticleList;
