import React, { useState, useEffect } from "react";
import Login from "./components/Login";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch("http://localhost:5000/api/protected", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => setMessage(data.message))
        .catch(() => setMessage("Failed to authenticate."));
    }
  }, []);

  return (
    <div>
      <h1>Welcome to Hive</h1>
      {!message ? <Login /> : <p>{message}</p>}
    </div>
  );
}

export default App;

/*
function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/articles")
      .then((response) => response.json())
      .then((data) => setArticles(data));
  }, []);

  return (
    <div >
      <h1>Articles</h1>
      <ul>
        {articles.map((article) => (
          <li key={article.id}>{article.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
*/