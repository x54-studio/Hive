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
      toast.success('Logged out successfully.', { autoClose: 1500 });
      navigate('/login')
    } catch (error) {
      toast.error('Error logging out.')
    }
  }

  // Check for role in both the top-level and in the claims object.
  const role = user?.claims?.role || user?.role

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
              <Link to="/articles" className="text-blue-600 hover:underline">
                Articles
              </Link>
            </li>
            <li>
              <Link to="/search" className="text-blue-600 hover:underline">
                Search
              </Link>
            </li>
            {(role === 'admin' || role === 'moderator') && (
              <li>
                <Link to="/articles/create" className="text-blue-600 hover:underline">
                  Create Article
                </Link>
              </li>
            )}
            {role === 'admin' && (
              <li>
                <Link to="/admin/users" className="text-blue-600 hover:underline">
                  Admin User Management
                </Link>
              </li>
            )}
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
