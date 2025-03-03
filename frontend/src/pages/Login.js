// src/pages/Login.js
import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
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

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  // onClick handler for the AsyncButton
  const handleClick = async (e) => {
    e.preventDefault()
    try {
      const resultAction = await dispatch(login(formData))
      if (login.fulfilled.match(resultAction)) {
        toast.success('Login successful')
        navigate('/profile')
      } else {
        toast.error(resultAction.payload.error || 'Login failed')
      }
    } catch (error) {
      toast.error('Login failed')
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
