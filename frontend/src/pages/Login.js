// src/pages/Login.js
import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { login } from '../redux/slices/authSlice'
import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

const Login = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { loading, error, user } = useSelector(state => state.auth)

  const [usernameOrEmail, setUsernameOrEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      // Dispatch the login thunk using username_or_email and password
      const resultAction = await dispatch(
        login({ username_or_email: usernameOrEmail, password })
      )
      if (login.fulfilled.match(resultAction)) {
        toast.success('Login successful!')
        navigate('/profile') // or any protected route
      } else {
        toast.error(resultAction.payload || 'Login failed. Please try again.')
      }
    } catch (err) {
      toast.error('An unexpected error occurred. Please try again.')
    }
  }

  return (
    <div className="flex flex-col items-center justify-center pt-40">
      <ToastContainer position="top-right" autoClose={5000} />
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <h2 className="text-3xl font-bold text-center mb-6">Login</h2>
        <form onSubmit={handleSubmit}>
          {error && (
            <p className="text-red-500 text-center mb-4">{error}</p>
          )}
          <input
            type="text"
            placeholder="Username or Email"
            value={usernameOrEmail}
            onChange={(e) => setUsernameOrEmail(e.target.value)}
            className="w-full p-3 border rounded mb-4 focus:outline-none focus:border-blue-500"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 border rounded mb-6 focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition-colors"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default Login
