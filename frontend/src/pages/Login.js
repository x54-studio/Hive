// src/pages/Login.js
import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { login } from '../redux/slices/authSlice'
import { toast } from 'react-toastify'
import AsyncButton from '../components/AsyncButton'

const Login = () => {
  const [formData, setFormData] = useState({
    username_or_email: '',
    password: '',
  })
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { user } = useSelector((state) => state.auth)

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate('/profile', { replace: true })
    }
  }, [user, navigate])

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  // onClick handler for the AsyncButton
  const handleClick = async (e) => {
    e.preventDefault()
    try {
      const resultAction = await dispatch(login(formData))
      if (login.fulfilled.match(resultAction)) {
        toast.success('Login successful', { autoClose: 1500 });
        navigate('/profile')
      } else {
        // Log the full error for debugging
        console.error('[Login] Login failed:', resultAction.payload)
        
        // Handle both object and string error payloads
        let errorMsg = 'Login failed'
        if (typeof resultAction.payload === 'string') {
          errorMsg = resultAction.payload
        } else if (resultAction.payload) {
          errorMsg = resultAction.payload.message || resultAction.payload.error || JSON.stringify(resultAction.payload)
        }
        
        toast.error(errorMsg)
      }
    } catch (error) {
      // Log the actual error
      console.error('[Login] Exception caught:', error)
      console.error('[Login] Error details:', error.response?.data || error.message || error)
      
      // Show actual error message if available
      const errorMsg = error.response?.data?.message || 
                       error.response?.data?.error || 
                       error.message || 
                       'Login failed'
      toast.error(errorMsg)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center pt-40">
      <h2 className="text-3xl font-bold mb-4">Login</h2>
      <form autoComplete="off" className="w-full max-w-sm">
        <div className="mb-4">
          <input
            name="username_or_email"
            type="text"
            placeholder="Username or Email"
            value={formData.username_or_email}
            onChange={handleChange}
            autoComplete="username"
            className="w-full p-3 border rounded focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            autoComplete="current-password"
            className="w-full p-3 border rounded focus:outline-none focus:border-blue-500"
          />
        </div>
        <AsyncButton
          type="submit"
          initialLabel="Login"
          loadingLabel="Logging in..."
          onClick={handleClick}
          className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition-colors"
        />
      </form>
      <div className="mt-4">
        Don't have an account?{' '}
        <Link to="/register" className="text-blue-600 hover:underline">
          Register
        </Link>
      </div>
    </div>
  )
}

export default Login
