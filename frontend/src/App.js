// src/App.js
import React, { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { refreshUser } from './redux/slices/authSlice'
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
  const dispatch = useDispatch()
  const [isInitialized, setIsInitialized] = useState(false)
  const { user } = useSelector((state) => state.auth)

  useEffect(() => {
    // Attempt to restore session on app mount
    dispatch(refreshUser())
      .unwrap()
      .catch(() => {
        // Session restore failed - that's fine, user is not logged in
      })
      .finally(() => {
        setIsInitialized(true)
      })
  }, [dispatch])

  if (!isInitialized) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>
  }

  return (
    <Router>
      {/* SessionManager is always rendered so that token refresh logic is active */}
      <SessionManager />
      <ToastContainer data-testid="toast-container" position="bottom-right" autoClose={8000} />
      <Navbar />
      <Routes>
        <Route 
          path="/" 
          element={user ? <Navigate to="/profile" replace /> : <Navigate to="/login" replace />} 
        />
        <Route 
          path="/login" 
          element={user ? <Navigate to="/profile" replace /> : <Login />} 
        />
        <Route 
          path="/register" 
          element={user ? <Navigate to="/profile" replace /> : <Register />} 
        />
        
        {/* Protected routes wrapped in PersistLogin for double safety (e.g. token refresh checks) */}
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
