import React, { Suspense } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './AuthContext'
import Layout from './components/Layout'
import Navbar from './components/Navbar'

// Lazy load pages for code splitting
const Home = React.lazy(() => import('./pages/Home'))
const Login = React.lazy(() => import('./pages/Login'))
const Register = React.lazy(() => import('./pages/Register'))
const Profile = React.lazy(() => import('./pages/Profile'))

function App() {
  return (
    <Router>
      <AuthProvider>
        <Layout>
          <Navbar />
          <Suspense
            fallback={<div className="text-center p-4">Loading...</div>}
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/profile" element={<Profile />} />
            </Routes>
          </Suspense>
        </Layout>
      </AuthProvider>
    </Router>
  )
}

export default App
