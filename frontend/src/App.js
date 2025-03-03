// src/App.js
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import AsyncButtonTest from './pages/AsyncButtonTest'
import ProtectedRoute from './components/ProtectedRoute'
import PersistLogin from './components/PersistLogin'
import Navbar from './components/Navbar'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

const App = () => {
  return (
    <Router>
      <ToastContainer data-testid="toast-container" position="bottom-right" autoClose={8000} />
      <Navbar />
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/async-button-test" element={<AsyncButtonTest />} />
        <Route element={<PersistLogin />}>
          <Route element={<ProtectedRoute />}>
            <Route path="/profile" element={<Profile />} />
          </Route>
        </Route>
      </Routes>
    </Router>
  )
}

export default App
