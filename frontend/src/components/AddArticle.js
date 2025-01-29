import React, { useState, useContext } from "react";
import { ArticleContext } from "../articleContext";
import { AuthContext } from "../authContext";

function AddArticle() {
  const { createArticle } = useContext(ArticleContext);
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem("token");
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    createArticle(title, content, token);
    setTitle("");
    setContent("");
  };

  if (!user || user.role !== "admin") return null;

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <input type="text" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} className="border p-2 w-full" />
      <textarea placeholder="Content" value={content} onChange={(e) => setContent(e.target.value)} className="border p-2 w-full mt-2"></textarea>
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 mt-3">Add Article</button>
    </form>
  );
}

export default AddArticle;
