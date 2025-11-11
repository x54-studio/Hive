// src/App.js
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import AdminUserManagement from './pages/AdminUserManagement'
import Articles from './pages/Articles'
import ArticleDetail from './pages/ArticleDetail'
import CreateArticle from './pages/CreateArticle'
import EditArticle from './pages/EditArticle'
import Search from './pages/Search'
import SessionManager from './components/SessionManager'
import ProtectedRoute from './components/ProtectedRoute'
import PersistLogin from './components/PersistLogin'
import Navbar from './components/Navbar'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

const App = () => {
  return (
    <Router>
      {/* SessionManager is always rendered so that token refresh logic is active */}
      <SessionManager />
      <ToastContainer data-testid="toast-container" position="bottom-right" autoClose={8000} />
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route element={<PersistLogin />}>
          <Route element={<ProtectedRoute />}>
            <Route path="/profile" element={<Profile />} />
            <Route path="/articles" element={<Articles />} />
            <Route path="/articles/create" element={<CreateArticle />} />
            <Route path="/articles/:id/edit" element={<EditArticle />} />
            <Route path="/articles/:id" element={<ArticleDetail />} />
            <Route path="/search" element={<Search />} />
            <Route path="/admin/users" element={<AdminUserManagement />} />
          </Route>
        </Route>
      </Routes>
    </Router>
  )
}

export default App
