// src/App.js
import React, { useEffect, Suspense } from "react";
import { useDispatch } from "react-redux";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Navbar from "./components/Navbar";
import { refreshTokens } from "./redux/authSlice"; // a new thunk for session check
import useTokenRefresh from "./hooks/useTokenRefresh";

const Home = React.lazy(() => import("./pages/Home"));
const Login = React.lazy(() => import("./pages/Login"));
const Register = React.lazy(() => import("./pages/Register"));
const Profile = React.lazy(() => import("./pages/Profile"));

function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    // Instead of calling GET /api/protected directly,
    // dispatch a thunk that handles session check/refresh.
    dispatch(refreshTokens());
  }, [dispatch]);

  // Start auto refresh mechanism.
  useTokenRefresh();

  return (
    <Router>
      <Layout>
        <Navbar />
        <Suspense fallback={<div className="text-center p-4">Loading...</div>}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </Suspense>
      </Layout>
    </Router>
  );
}

export default App;
