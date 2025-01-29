import React, { createContext, useState, useEffect } from "react";

const ArticleContext = createContext();

const ArticleProvider = ({ children }) => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    const response = await fetch("http://localhost:5000/api/articles");
    const data = await response.json();
    setArticles(data);
  };

  const createArticle = async (title, content, token) => {
    const response = await fetch("http://localhost:5000/api/articles", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ title, content }),
    });
    if (response.ok) fetchArticles();
  };

  const deleteArticle = async (articleId, token) => {
    await fetch(`http://localhost:5000/api/articles/${articleId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchArticles();
  };

  return (
    <ArticleContext.Provider value={{ articles, createArticle, deleteArticle }}>
      {children}
    </ArticleContext.Provider>
  );
};

export { ArticleContext, ArticleProvider };
