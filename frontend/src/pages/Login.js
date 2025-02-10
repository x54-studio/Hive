// src/pages/Login.js
import React, { useState, useContext } from "react";
import { AuthContext } from "../AuthContext";

function Login() {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg(""); // Clear any previous error message
    try {
      await login(email, password);
    } catch (err) {
      console.error("Login error:", err.message);
      setErrorMsg("Login failed: " + err.message);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      {errorMsg && <p className="text-red-500 mb-4">{errorMsg}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 border mb-2"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 border mb-2"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="w-full bg-blue-500 text-white p-2">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
