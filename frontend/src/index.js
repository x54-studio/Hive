import React from "react";
import ReactDOM from "react-dom/client"; // Import from "react-dom/client" for React 18+
import App from "./App";
import { AuthProvider } from "./authContext";
import "./styles/index.css"; // Tailwind CSS styles

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
