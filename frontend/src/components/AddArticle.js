import React, { useState, useContext } from "react";
import { AuthContext } from "../AuthContext";

function AddArticle({ onArticleAdded }) {
  const { user } = useContext(AuthContext);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!title || !content) {
      setError("Title and content cannot be empty!");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/articles", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ title, content }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Failed to create article.");
      }

      setTitle("");
      setContent("");
      onArticleAdded();
    } catch (err) {
      console.error("Error submitting article:", err.message);
      setError(err.message);
    }
  };

  if (!user || user.role !== "admin") return null;

  return (
    <form
      onSubmit={handleSubmit}
      className="mb-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg shadow"
    >
      <h2 className="text-lg font-bold mb-3 text-gray-900 dark:text-gray-200">
        Add New Article
      </h2>
      {error && <p className="text-red-500">{error}</p>}
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="border p-2 w-full rounded mb-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200"
      />
      <textarea
        placeholder="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        className="border p-2 w-full rounded mb-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200"
      ></textarea>
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Publish Article
      </button>
    </form>
  );
}

export default AddArticle;
