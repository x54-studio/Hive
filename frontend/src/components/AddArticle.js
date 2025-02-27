// src/components/AddArticle.js
import React, { useState } from "react";
import axios from "axios";
import { useQueryClient } from "@tanstack/react-query";

const AddArticle = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const queryClient = useQueryClient();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Post the new article to your API
      await axios.post(
        "http://localhost:5000/api/articles",
        { title, content },
        { withCredentials: true }
      );
      // Clear input fields
      setTitle("");
      setContent("");
      // Invalidate the articles query so the list refreshes
      queryClient.invalidateQueries(["articles"]);
    } catch (error) {
      console.error("Error adding article:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg shadow">
      <h2 className="text-lg font-bold mb-3 text-gray-900 dark:text-gray-200">Add New Article</h2>
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
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        Publish Article
      </button>
    </form>
  );
};

export default AddArticle;
