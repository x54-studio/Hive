// src/App.js
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'

const App = () => {
  return (
    <Router>
      <nav className="p-4 bg-gray-200">
        <ul className="flex space-x-4">
          <li>
            <Link to="/register" className="text-blue-600 hover:underline">Register</Link>
          </li>
          <li>
            <Link to="/login" className="text-blue-600 hover:underline">Login</Link>
          </li>
        </ul>
      </nav>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  )
}

export default App
