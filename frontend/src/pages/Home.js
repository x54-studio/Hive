// src/pages/Home.js
import React, { useState, useContext } from "react";
import { AuthContext } from "../AuthContext";
import AddArticle from "../components/AddArticle";
import ArticleList from "../components/ArticleList";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const Home = () => {
  const { user } = useContext(AuthContext);
  const [refreshSignal, setRefreshSignal] = useState(0);

  const handleArticleAdded = () => {
    setRefreshSignal((prev) => prev + 1);
    toast.success("Article added successfully!");
  };

  return (
    <div className="p-6 flex flex-col items-center justify-start">
      <ToastContainer 
        position="top-right" 
        autoClose={10000}
        style ={{ top: "80px"}} 
      />
      {/* Header Section */}
      <header className="w-full max-w-4xl mb-8">
        <h1 className="text-5xl font-bold text-center text-white drop-shadow-lg">
          Welcome to Hive
        </h1>
        <p className="mt-2 text-center text-white text-lg drop-shadow">
          Discover the latest articles and news.
        </p>
      </header>

      {/* Main Content Section */}
      <main className="w-full max-w-4xl">
        {user && user.role === "admin" && (
          <div className="mb-6">
            <AddArticle onArticleAdded={handleArticleAdded} />
          </div>
        )}
        <section className="bg-white bg-opacity-90 p-6 rounded-lg shadow-lg">
          <ArticleList refreshSignal={refreshSignal} />
        </section>
      </main>
    </div>
  );
};

export default Home;
