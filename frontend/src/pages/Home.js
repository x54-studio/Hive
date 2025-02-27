// src/pages/Home.js
import React from "react";
import { useSelector } from "react-redux";
import AddArticle from "../components/AddArticle";
import ArticleList from "../components/ArticleList";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const Home = () => {
  // Get the authenticated user from Redux.
  const user = useSelector((state) => state.auth.user);

  const handleArticleAdded = () => {
    toast.success("Article added successfully!");
  };

  return (
    <div className="p-6">
      <header className="mb-8">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-gray-200 text-center">
          Welcome to Hive
        </h1>
        <p className="mt-2 text-center text-gray-700 dark:text-gray-300 text-lg">
          Discover the latest articles and news.
        </p>
      </header>
      <main>
        {user && user.claims && user.claims.role === "admin" && (
          <div className="mb-6">
            <AddArticle onArticleAdded={handleArticleAdded} />
          </div>
        )}
        <section className="bg-white dark:bg-gray-800 bg-opacity-90 p-6 rounded-lg shadow-lg">
          <ArticleList refreshSignal={0} />
        </section>
      </main>
      <ToastContainer position="top-right" autoClose={5000} />
    </div>
  );
};

export default Home;
