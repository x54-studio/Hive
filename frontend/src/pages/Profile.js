// src/pages/Profile.js
import React, { useState, useEffect } from 'react'
import axiosInstance from '../api/axiosInstance'
import { toast } from 'react-toastify'

const Profile = () => {
  const [userData, setUserData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true)
      setError('')
      try {
        const response = await axiosInstance.get('/protected', { withCredentials: true })
        setUserData(response.data)
      } catch (err) {
        const errorMessage = err.response?.data?.error || 'Failed to load profile'
        setError(errorMessage)
        toast.error(errorMessage, { autoClose: 5000 })
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [])

  const formatRole = (role) => {
    if (!role) return 'Regular User'
    const roleLower = role.toLowerCase()
    if (roleLower === 'admin') return 'Admin'
    if (roleLower === 'moderator') return 'Moderator'
    return 'Regular User'
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center pt-40">
        <div className="text-gray-600">Loading profile...</div>
      </div>
    )
  }

  if (error && !userData) {
    return (
      <div className="flex flex-col items-center justify-center pt-40">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={() => window.location.reload()}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    )
  }

  if (!userData) {
    return null
  }

  const username = userData.username || userData.claims?.sub || 'N/A'
  const email = userData.claims?.email || 'N/A'
  const role = userData.claims?.role || 'regular'

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Profile</h2>
      
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <div className="text-gray-900">{username}</div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <div className="text-gray-900">{email}</div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Role
            </label>
            <div className="text-gray-900">{formatRole(role)}</div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Registration Date
            </label>
            <div className="text-gray-500 text-sm">
              Not available (requires backend endpoint)
            </div>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            Profile editing is not available yet. This feature requires backend endpoints that are not currently implemented.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Profile
