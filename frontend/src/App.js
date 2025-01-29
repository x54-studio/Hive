import React from "react";
import { AuthProvider } from "./authContext";
import { ArticleProvider } from "./articleContext";
import Login from "./pages/Login";
import AddArticle from "./components/AddArticle";
import ArticleList from "./components/ArticleList";

function App() {
  return (
    <AuthProvider>
      <ArticleProvider>
        <div className="p-4">
          <Login />
          <AddArticle />
          <ArticleList />
        </div>
      </ArticleProvider>
    </AuthProvider>
  );
}

export default App;
