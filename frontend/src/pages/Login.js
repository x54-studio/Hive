import React, { useState, useContext } from "react";
import { AuthContext } from "../authContext";

function Login() {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login(email, password);
  };

  return (
    <div className="flex flex-col items-center">
      <h2 className="text-2xl font-bold">Login</h2>
      <form onSubmit={handleSubmit} className="w-1/3">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 w-full"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 w-full mt-2"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 mt-3">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
