// src/api/articles.js

export const fetchArticles = async () => {
  console.log("NODE_ENV: " + process.env.NODE_ENV);
  // not working
  // "start:prod": "npx cross-env NODE_ENV=production react-scripts start",
  // 
  // if (process.env.NODE_ENV === "production") {
  if (true) {
    // In production, call the real API.
    const response = await fetch("http://127.0.0.1:5000/api/articles");
    if (!response.ok) {
      throw new Error("Failed to fetch articles");
    }
    const data = await response.json();
    return data;
  } else {
    // In non-production environments, return test data.
    return [
      { _id: "1", title: "Article 1", content: "Content 1" },
      { _id: "2", title: "Article 2", content: "Content 2" }
    ];
  }
};
