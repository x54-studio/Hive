import React, { useContext } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import { AuthProvider, AuthContext } from "./authContext";
//import { ArticleProvider } from "./articleContext";
import { ThemeProvider } from "./themeContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import AddArticle from "./components/AddArticle";
import ArticleList from "./components/ArticleList";
import ThemeToggle from "./components/ThemeToggle";


function Navbar() {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold">
        <Link to="/">Hive News</Link>
      </h1>
      <div className="flex items-center space-x-4">
        <Link to="/" className="hover:underline">Home</Link>
        {user ? (
          <>
            <Link to="/profile" className="hover:underline">Profile</Link>
            <button onClick={logout} className="bg-red-500 px-4 py-2 rounded">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:underline">Login</Link>
            <Link to="/register" className="hover:underline">Register</Link>
          </>
        )}
        <ThemeToggle />
      </div>
    </nav>
  );
}

function App() {
  return (
    <ThemeProvider>
      <Router>
        <AuthProvider>
          {/*}<ArticleProvider>-->*/}
            <Navbar />
            <div className="min-h-screen p-4 bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition-all">
              <Routes>
                <Route path="/" element={
                  <>
                    <AddArticle />
                    <ArticleList />
                  </>
                } />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/profile" element={<Profile />} />
              </Routes>
            </div>
          {/* </ArticleProvider> */}
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App;
