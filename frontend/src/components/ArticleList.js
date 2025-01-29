import React, { useContext } from "react";
import { ArticleContext } from "../articleContext";
import { AuthContext } from "../authContext";

function ArticleList() {
  const { articles, deleteArticle } = useContext(ArticleContext);
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem("token");

  return (
    <div>
      <h2 className="text-xl font-bold">Articles</h2>
      <ul>
        {articles.map((article) => (
          <li key={article.id} className="border p-2 mt-2">
            <h3 className="font-semibold">{article.title}</h3>
            <p>{article.content}</p>
            {user && user.role === "admin" && (
              <button onClick={() => deleteArticle(article.id, token)} className="bg-red-500 text-white px-2 py-1">
                Delete
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ArticleList;
