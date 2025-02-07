import React, { useState, useContext } from "react";
import { AuthContext } from "../authContext";

function AddArticle() {
  console.log("AddArticle(js)");
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem("token");
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Clear previous errors

    if (!title || !content) {
      setError("Title and content cannot be empty!");
      return;
    }

    console.log("🔑 Sending Token:", token); // Debugging: Check if token is present

    try {
      const response = await fetch("http://localhost:5000/api/articles", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title, content }), // Ensure correct JSON structure
      });

      const data = await response.json();
      console.log("API Response:", data); // Debugging: Log API response

      if (!response.ok) {
        throw new Error(data.error || "Failed to create article.");
      }

      alert("✅ Article added successfully!");
      setTitle("");
      setContent("");
    } catch (err) {
      console.error("Error submitting article:", err.message);
      setError(err.message);
    }
  };

  if (!user || user.role !== "admin") return null;

  return (
    <form onSubmit={handleSubmit} className="mb-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg shadow">
      <h2 className="text-lg font-bold mb-3">Add New Article</h2>
      {error && <p className="text-red-500">{error}</p>}
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="border p-2 w-full rounded mb-2"
      />
      <textarea
        placeholder="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        className="border p-2 w-full rounded mb-2"
      ></textarea>
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Publish Article
      </button>
    </form>
  );
}

export default AddArticle;
