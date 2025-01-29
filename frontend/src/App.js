import React, { useContext } from "react";
import { AuthContext } from "./authContext";
import Login from "./pages/Login";

function App() {
  const { user, logout } = useContext(AuthContext);

  return (
    <div>
      <nav className="bg-gray-800 text-white p-4 flex justify-between">
        <h1>Hive</h1>
        {user ? (
          <button onClick={logout} className="bg-red-500 px-3 py-1">
            Logout
          </button>
        ) : (
          <a href="/login">Login</a>
        )}
      </nav>
      {user ? <p>Welcome! You are logged in.</p> : <Login />}
    </div>
  );
}

export default App;
