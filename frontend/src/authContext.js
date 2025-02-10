// src/AuthContext.js
import React, { createContext, useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();
const REFRESH_INTERVAL = 30000; // 30 seconds

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const fetchUserProfile = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/protected", {
        method: "GET",
        credentials: "include",
      });
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else if (response.status === 401) {
        // Attempt to refresh tokens if access token is expired
        const refreshResponse = await fetch("http://localhost:5000/api/refresh", {
          method: "POST",
          credentials: "include",
        });
        if (refreshResponse.ok) {
          // Retry fetching the profile after successful refresh
          const retryResponse = await fetch("http://localhost:5000/api/protected", {
            method: "GET",
            credentials: "include",
          });
          if (retryResponse.ok) {
            const userData = await retryResponse.json();
            setUser(userData);
          } else {
            setUser(null);
          }
        } else {
          setUser(null);
        }
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error("Error fetching profile:", error);
      setUser(null);
    }
  };


  // Logout function: call the backend to clear cookies then update local state.
  const logout = useCallback(async () => {
    try {
      await fetch("http://localhost:5000/api/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      setUser(null);
      // Broadcast logout event to other tabs
      localStorage.setItem("logout", Date.now().toString());
      navigate("/login");
    }
  }, [navigate]);

  // Refresh tokens, but only if a user is logged in.
  const refreshTokens = useCallback(async () => {
    if (!user) return;
    try {
      const response = await fetch("http://localhost:5000/api/refresh", {
        method: "POST",
        credentials: "include",
      });
      if (response.ok) {
        console.log("Tokens refreshed successfully.");
      } else {
        console.error("Failed to refresh tokens, logging out.");
        logout();
      }
    } catch (error) {
      console.error("Error refreshing tokens:", error);
      logout();
    }
  }, [logout, user]);

  // Set up a periodic token refresh only when the user is logged in.
  useEffect(() => {
    if (!user) return;
    const interval = setInterval(() => {
      refreshTokens();
    }, REFRESH_INTERVAL);
    return () => clearInterval(interval);
  }, [refreshTokens, user]);

  // On mount, fetch the user profile to update auth state.
  useEffect(() => {
    fetchUserProfile();
  }, []);

  // Listen for logout events from other tabs
  useEffect(() => {
    const handleStorageLogout = (event) => {
      if (event.key === "logout") {
        setUser(null);
        navigate("/login");
      }
    };
    window.addEventListener("storage", handleStorageLogout);
    return () => window.removeEventListener("storage", handleStorageLogout);
  }, [navigate]);

  const login = async (email, password) => {
    try {
      const response = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include",
      });
      const data = await response.json();
      if (data.message === "Login successful") {
        await fetchUserProfile();
        navigate("/profile");
      } else {
        throw new Error(data.message || "Login failed");
      }
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
