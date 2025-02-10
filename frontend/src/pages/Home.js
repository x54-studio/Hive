// src/pages/Home.js
import React, { useState, useContext } from "react";
import { AuthContext } from "../AuthContext";
import AddArticle from "../components/AddArticle";
import ArticleList from "../components/ArticleList";

const Home = () => {
  const { user } = useContext(AuthContext);
  // refreshSignal is incremented whenever an article is added to trigger a full list refresh.
  const [refreshSignal, setRefreshSignal] = useState(0);

  const handleArticleAdded = () => {
    setRefreshSignal((prev) => prev + 1);
  };

  return (
    <div>
      {user && user.role === "admin" && (
        <div className="mb-6">
          <AddArticle onArticleAdded={handleArticleAdded} />
        </div>
      )}
      <ArticleList refreshSignal={refreshSignal} />
    </div>
  );
};

export default Home;
