import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../authContext";

function ArticleList() {
  console.log("ArticleList(js)");
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem("token");
  const [articles, setArticles] = useState([]); // Ensure articles is always an array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        console.log("fetchArticles");
        const response = await fetch("http://localhost:5000/api/articles", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch articles.");
        }

        const data = await response.json();
        setArticles(data || []); // Ensure data is always an array
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, [token]);

  const handleDelete = async (articleId) => {
    if (!articleId) {
      console.error("❌ Error: Missing article ID.");
      return;
    }

    console.log(`🗑️ Attempting to delete article: ${articleId}`);

    try {
      const response = await fetch(`http://localhost:5000/api/articles/${articleId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      console.log("🗑️ Delete Response:", data);

      if (!response.ok) {
        throw new Error(data.error || "Failed to delete article.");
      }

      alert("✅ Article deleted successfully!");
      setArticles((prevArticles) => prevArticles.filter((article) => article._id !== articleId)); // Update UI after delete
    } catch (err) {
      console.error("❌ Error deleting article:", err.message);
    }
  };

  if (loading) return <p>Loading articles...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (articles.length === 0) return <p>No articles available.</p>;

  return (
    <div>
      {articles.map((article) => (
        <div key={article._id} className="border p-4 rounded-lg shadow-lg bg-gray-50 dark:bg-gray-800">
          <h3 className="font-semibold text-lg">{article.title}</h3>
          <p className="text-sm text-gray-700 dark:text-gray-300 mt-2">{article.content}</p>
          {user && user.role === "admin" && (
            <button
              onClick={() => handleDelete(article._id)}
              className="bg-red-500 text-white px-4 py-2 mt-3 rounded"
            >
              🗑️ Delete
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default ArticleList;
