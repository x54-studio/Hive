// src/pages/Login.js
import React from 'react'
import { Link } from 'react-router-dom'

const Login = () => {
  return (
    <div className="flex flex-col items-center justify-center pt-40">
      <h2 className="text-3xl font-bold mb-4">Login</h2>
      {/* Your login form implementation goes here */}
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
