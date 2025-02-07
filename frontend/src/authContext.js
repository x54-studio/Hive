import React, { createContext, useState, useEffect } from "react";

var INITIALIZED_ONCE = 1;
const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const decodeToken = (token) => {
    try {
      const base64Url = token.split(".")[1]; // Extract payload
      const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
      const decoded = JSON.parse(atob(base64));

      console.log("Decoded Token:", decoded); // Debugging

      return {
        username: decoded.sub, // ✅ `sub` is now a plain string
        role: decoded.role, // ✅ Extract role from claims
        exp: decoded.exp, // ✅ Store expiration time
      };
    } catch (error) {
      console.error("Error decoding token:", error);
      return null;
    }
  };

  const refreshToken = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/refresh", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include", // Ensure cookies are sent with request
      });
  
      const data = await response.json();
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        return data.access_token;
      } else {
        logout();
      }
    } catch (error) {
      console.error("Failed to refresh token:", error);
      logout();
    }
  };
  
  const checkTokenExpiration = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    console.log("checkTokenExpiration");
    const decoded = decodeToken(token);
    const currentTime = Math.floor(Date.now() / 1000);

    if (decoded && decoded.exp < currentTime) {
      console.warn("Token expired, refreshing...");
      await refreshToken(); // ✅ Try refreshing the token
    }
  
  };
  
  useEffect(() => {    
    if (INITIALIZED_ONCE == 1)
    {
      INITIALIZED_ONCE = 0;
    const token = localStorage.getItem("token");
    if (token) {
      const decodedUser = decodeToken(token);
      if (decodedUser) {
        setUser(decodedUser);
      } else {
        localStorage.removeItem("token");
      }
    }

    // ✅ Check token expiration periodically
    const interval = setInterval(() => {
      checkTokenExpiration();
    }, 1 * 60 * 1000); // Every 1 minute
  }
  }, []);
  

  const login = async (email, password) => {
    const response = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      const decodedUser = decodeToken(data.access_token);
      setUser(decodedUser);
      window.location.href = "/"; // 🚀 Redirect to profile page after login
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    window.location.href = "/login"; // 🚀 Redirect to login page
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
