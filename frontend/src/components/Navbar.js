// src/components/Navbar.js
import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { logout } from '../redux/slices/authSlice'
import { toast } from 'react-toastify'

const Navbar = () => {
  const user = useSelector((state) => state.auth.user)
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await dispatch(logout()).unwrap()
      toast.success('Logged out successfully.')
      navigate('/login')
    } catch (error) {
      toast.error('Error logging out.')
    }
  }

  return (
    <nav className="p-4 bg-gray-200">
      <ul className="flex space-x-4">
        {user ? (
          <>
            <li>
              <Link to="/profile" className="text-blue-600 hover:underline">
                Profile
              </Link>
            </li>
            <li>
              <button onClick={handleLogout} className="text-blue-600 hover:underline">
                Logout
              </button>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/register" className="text-blue-600 hover:underline">
                Register
              </Link>
            </li>
            <li>
              <Link to="/login" className="text-blue-600 hover:underline">
                Login
              </Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  )
}

export default Navbar
